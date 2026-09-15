"""Agent 可调用的工具集合。

每个工具都用 @tool 装饰：函数的参数签名与 docstring 就是模型判断
"这个问题该不该调工具、该调哪个工具、参数怎么填"的依据。

设计原则：只提供确定性、可校验、无副作用的工具。
不提供执行 shell、写文件、访问网络等危险能力，避免提示词注入造成实际破坏。
"""
import ast
import datetime as dt
import operator
from pathlib import Path

from langchain_core.tools import tool

# 计算器白名单：只允许四则运算、幂与取模，杜绝 eval / exec 注入
_BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _eval_node(node):
    """递归求值 AST 节点，只放行白名单内的运算符与数字常量。"""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _BINARY_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError('仅支持数字与 + - * / % ** 运算')


@tool
def get_current_time() -> str:
    """查询当前的日期、时间与星期。

    当用户询问"现在几点""今天几号""星期几""距离某天还有多久"等
    与当前时间相关的问题时调用。
    """
    now = dt.datetime.now()
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return f'{now:%Y-%m-%d %H:%M:%S} {weekdays[now.weekday()]}'


@tool
def calculate(expression: str) -> str:
    """计算一个纯数学表达式，例如 "12*8+3"、"(45+5)/2"、2**10。

    当用户需要精确的数值计算（算术、百分比、乘方）时调用。
    表达式中只能出现数字和 + - * / % ** 运算符，不能包含变量或函数。
    """
    try:
        value = _eval_node(ast.parse(expression, mode='eval').body)
    except Exception as exc:
        return f'计算失败：{exc}'
    return f'{expression} = {value}'


@tool
def search_notes(keyword: str) -> str:
    """在本地笔记目录 notes/ 中按关键词检索，返回命中的文件名、行号与片段。

    当用户询问自己的笔记、资料、学习记录、之前记过的内容时调用。
    keyword 使用要检索的关键词，例如 "LangGraph"、"记忆"。
    """
    notes_dir = Path(__file__).resolve().parent / 'notes'
    if not notes_dir.exists():
        return '笔记目录 notes/ 不存在，暂时没有可检索的资料。'

    hits: list[str] = []
    for path in sorted(notes_dir.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        for line_no, line in enumerate(text.splitlines(), 1):
            if keyword and keyword.lower() in line.lower():
                hits.append(f'{path.name}:{line_no}: {line.strip()}')

    if not hits:
        return f'没有找到与「{keyword}」相关的笔记内容。'
    return '\n'.join(hits[:20])


# 注册给模型的工具清单
TOOLS = [get_current_time, calculate, search_notes]
