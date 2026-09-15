import json
import sqlite3
from collections.abc import Sequence

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    messages_from_dict,
    messages_to_dict,
)
from langchain_core.chat_history import BaseChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """你叫「小助手」，是一个专业、中性的通用个人 AI 助手，为你的用户提供帮助。

【定位】
- 你是工具型助手，不是任何人际关系角色：不虚构身份、关系或情感，不进行角色扮演式的亲密互动。
- 用第二人称「你」称呼用户，不使用带有亲密关系色彩或过度亲昵的称呼。

【能力范围】
- 日程提醒：帮助梳理、记录、提醒待办事项与时间安排
- 笔记整理：把零散信息归纳成条理清晰的结构化笔记
- 知识问答：解释概念、拆解问题、给出步骤化的解决方案
- 情绪支持：倾听并共情，提供理性、可执行的建议

【说话风格】
- 专业、简洁、友好；短句为主，条理清晰，必要时用列表分点
- 一次回复聚焦 1 到 3 个要点，不啰嗦、不卖萌、不过度使用表情符号
- 信息不足时先提问澄清，不猜测；不确定时明确说明不确定

【安全与隐私】
- 不涉及色情、暴力、违法内容
- 不主动索要或记录身份证号、银行卡、密码等敏感信息
- 当用户提到自残、轻生等危机话题时，认真对待、表达关切，并明确建议其寻求专业帮助或联系身边可信赖的人"""

SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ('system', '你是对话摘要助手。请把下面的对话提炼成一段简洁、客观的摘要，'
               '保留关键信息：用户提到的事实、偏好、待办事项、重要时间、'
               '已确认的结论以及情绪状态等。'
               '用第三人称、平实准确，不要啰嗦，不要加入主观评价。'),
    ('user', '已有摘要：\n{summary}\n\n待总结的新对话：\n{new_messages}')
])


class SQLiteChatMessageHistory(BaseChatMessageHistory):
    """把最近的对话缓冲区持久化到 SQLite，程序重启后不丢失。"""

    def __init__(self, session_id: str, db_path: str = 'assistant.db'):
        self.session_id = session_id
        self.db_path = db_path
        self._init_db()
        self.messages: list[BaseMessage] = self._load()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    data TEXT NOT NULL
                )
                '''
            )
            conn.execute(
                'CREATE INDEX IF NOT EXISTS idx_session ON messages(session_id)'
            )

    def _load(self) -> list[BaseMessage]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                'SELECT data FROM messages WHERE session_id = ? ORDER BY id',
                (self.session_id,),
            ).fetchall()
        return messages_from_dict([json.loads(r[0]) for r in rows])

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        serialized = messages_to_dict(messages)
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(
                'INSERT INTO messages (session_id, type, data) VALUES (?, ?, ?)',
                (
                    (self.session_id, m.type, json.dumps(d, ensure_ascii=False))
                    for m, d in zip(messages, serialized)
                ),
            )
        self.messages.extend(messages)

    def keep_last(self, n: int) -> None:
        """只保留最近 n 条消息，删除更早的。"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''
                DELETE FROM messages WHERE session_id = ? AND id NOT IN (
                    SELECT id FROM messages WHERE session_id = ?
                    ORDER BY id DESC LIMIT ?
                )
                ''',
                (self.session_id, self.session_id, n),
            )
        self.messages = self._load()

    def clear(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'DELETE FROM messages WHERE session_id = ?',
                (self.session_id,),
            )
        self.messages = []


class SummaryStore:
    """把长期摘要持久化到 SQLite（每个 session 一条）。"""

    def __init__(self, db_path: str = 'assistant.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS summary (
                    session_id TEXT PRIMARY KEY,
                    content TEXT NOT NULL
                )
                '''
            )

    def get(self, session_id: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                'SELECT content FROM summary WHERE session_id = ?',
                (session_id,),
            ).fetchone()
        return row[0] if row else ''

    def set(self, session_id: str, content: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''
                INSERT INTO summary (session_id, content) VALUES (?, ?)
                ON CONFLICT(session_id) DO UPDATE SET content = excluded.content
                ''',
                (session_id, content),
            )

    def clear(self, session_id: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'DELETE FROM summary WHERE session_id = ?',
                (session_id,),
            )


def format_messages(messages: Sequence[BaseMessage]) -> str:
    """把消息列表转成一段纯文本，方便交给摘要模型。"""
    lines = []
    for m in messages:
        role = '用户' if m.type == 'human' else '小助手'
        lines.append(f'{role}: {m.content}')
    return '\n'.join(lines)


class Assistant:
    """小助手的对话大脑：人设 + 摘要记忆 + 长期持久化。

    session_id 用来区分不同用户（终端里固定 'default'，Web 端使用前端生成的会话 ID）。
    """

    def __init__(
        self,
        db_path: str = 'assistant.db',
        summary_trigger: int = 30,
        max_buffer: int = 20,
    ):
        self.db_path = db_path
        self.summary_trigger = summary_trigger
        self.max_buffer = max_buffer
        self.llm = ChatOpenAI(model='deepseek-chat', temperature=0.7)
        self.chat_chain = self.llm | StrOutputParser()
        self.summary_chain = SUMMARY_PROMPT | self.llm | StrOutputParser()

    def chat(self, session_id: str, text: str) -> str:
        history = SQLiteChatMessageHistory(session_id, self.db_path)
        summary_store = SummaryStore(self.db_path)
        summary = summary_store.get(session_id)

        # 1. 组装上下文：人设 + 长期摘要 + 最近对话 + 当前输入
        system_text = SYSTEM_PROMPT
        if summary:
            system_text += f'\n\n【之前对话的摘要（长期记忆）】\n{summary}'

        context: list[BaseMessage] = [SystemMessage(content=system_text)]
        context.extend(history.messages)
        context.append(HumanMessage(content=text))

        # 2. 调用模型
        reply = self.chat_chain.invoke(context)

        # 3. 存进缓冲区
        history.add_messages([HumanMessage(content=text), AIMessage(content=reply)])

        # 4. 缓冲区太满就做一次摘要压缩
        if len(history.messages) > self.summary_trigger:
            old_messages = history.messages[:-self.max_buffer]
            new_summary = self.summary_chain.invoke({
                'summary': summary or '（无）',
                'new_messages': format_messages(old_messages),
            })
            summary_store.set(session_id, new_summary)
            history.keep_last(self.max_buffer)

        return reply

    def clear(self, session_id: str) -> None:
        SQLiteChatMessageHistory(session_id, self.db_path).clear()
        SummaryStore(self.db_path).clear(session_id)
