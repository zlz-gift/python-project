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
    ToolMessage,
    messages_from_dict,
    messages_to_dict,
)
from langchain_core.chat_history import BaseChatMessageHistory
from dotenv import load_dotenv

from tools import TOOLS

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

【工具使用】
- 当需要当前时间、精确计算或检索本地笔记时，调用对应工具获取真实结果，不要凭猜测回答
- 一次可以按需调用多个工具；工具返回错误时换一种方式重试或如实说明，不要编造结果

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
        max_tool_rounds: int = 5,
    ):
        self.db_path = db_path
        self.summary_trigger = summary_trigger
        self.max_buffer = max_buffer
        self.max_tool_rounds = max_tool_rounds
        self.llm = ChatOpenAI(model='deepseek-chat', temperature=0.7)
        self.chat_chain = self.llm | StrOutputParser()
        self.summary_chain = SUMMARY_PROMPT | self.llm | StrOutputParser()
        self._llm_with_tools = None

    # ---------- 工具调用 ----------

    def _agent_llm(self):
        """懒加载绑定工具的模型；模型或网关不支持工具调用时会抛异常，由上层降级。"""
        if self._llm_with_tools is None:
            self._llm_with_tools = self.llm.bind_tools(TOOLS)
        return self._llm_with_tools

    def _run_tool(self, name: str, args: dict) -> str:
        """执行模型选定的工具，异常统一转成可读文本回填，避免整轮对话失败。"""
        tool = next((t for t in TOOLS if t.name == name), None)
        if tool is None:
            return f'未知工具：{name}'
        try:
            return str(tool.invoke(args or {}))
        except Exception as exc:
            return f'工具 {name} 执行出错：{exc}'

    @staticmethod
    def _system_text(summary: str) -> str:
        """人设 + 长期摘要，拼成最终的系统指令。"""
        if not summary:
            return SYSTEM_PROMPT
        return f'{SYSTEM_PROMPT}\n\n【之前对话的摘要（长期记忆）】\n{summary}'

    # ---------- 对话主流程 ----------

    def chat(self, session_id: str, text: str) -> str:
        """只返回回复文本，保持向后兼容。"""
        reply, _ = self.chat_with_trace(session_id, text)
        return reply

    def chat_with_trace(self, session_id: str, text: str) -> tuple[str, list[str]]:
        """执行一轮 Agent 对话，返回 (回复文本, 本轮调用的工具名列表)。

        流程：组装上下文 → 模型判断是否调工具 → 执行工具并回填结果 → 循环，
        直到模型给出最终回答，或达到 max_tool_rounds 上限。
        """
        history = SQLiteChatMessageHistory(session_id, self.db_path)
        summary_store = SummaryStore(self.db_path)
        summary = summary_store.get(session_id)

        # 1. 组装上下文：人设（含长期摘要）+ 最近对话 + 当前输入
        context: list[BaseMessage] = [SystemMessage(content=self._system_text(summary))]
        context.extend(history.messages)
        context.append(HumanMessage(content=text))

        # 2. Agent 循环：由模型自主决定是否调工具、调几次
        used_tools: list[str] = []
        reply = ''
        try:
            llm_with_tools = self._agent_llm()
            for _ in range(self.max_tool_rounds):
                ai_message = llm_with_tools.invoke(context)
                context.append(ai_message)
                tool_calls = getattr(ai_message, 'tool_calls', None) or []
                if not tool_calls:
                    reply = ai_message.content or ''
                    break
                for call in tool_calls:
                    used_tools.append(call['name'])
                    result = self._run_tool(call['name'], call.get('args') or {})
                    context.append(ToolMessage(content=result, tool_call_id=call['id']))
            else:
                # 跑满上限仍未给出最终回答，兜底收尾
                reply = '（这个问题需要多步工具调用，已达到本轮上限，请补充更具体的信息。）'
        except Exception as exc:
            # 降级：模型或网关不支持工具调用时退回纯对话链，保证服务可用
            print(f'[warn] 工具调用不可用，降级为普通对话：{exc}')
            fallback: list[BaseMessage] = [
                SystemMessage(content=self._system_text(summary)),
                *history.messages,
                HumanMessage(content=text),
            ]
            reply = self.chat_chain.invoke(fallback)
            used_tools = []

        # 3. 只把最终问答写入短期缓冲，工具中间步骤不入库，避免污染摘要
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

        return reply, used_tools

    def clear(self, session_id: str) -> None:
        SQLiteChatMessageHistory(session_id, self.db_path).clear()
        SummaryStore(self.db_path).clear(session_id)
