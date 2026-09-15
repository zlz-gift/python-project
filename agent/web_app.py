from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from assistant import Assistant

bot = Assistant()
app = FastAPI()


class ChatRequest(BaseModel):
    session_id: str
    text: str


HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#5b6cff">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>小助手</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🤖</text></svg>">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  :root {
    --brand: #5b6cff;
    --brand-deep: #4453e8;
    --bg: #f4f5ff;
    --bubble-bot: #ffffff;
    --bubble-me: #5b6cff;
  }
  html, body { height: 100%; }
  body {
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    height: 100dvh;
    overflow: hidden;
  }
  header {
    background: linear-gradient(135deg, var(--brand), var(--brand-deep));
    color: #fff;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(91,108,255,.25);
  }
  header .avatar {
    font-size: 28px;
    line-height: 1;
  }
  header .title { font-size: 17px; font-weight: 700; }
  header .sub { font-size: 11px; opacity: .9; }
  header .spacer { flex: 1; }
  header button {
    background: rgba(255,255,255,.2);
    color: #fff;
    border: none;
    border-radius: 14px;
    padding: 6px 12px;
    font-size: 13px;
    cursor: pointer;
  }
  #chat {
    flex: 1;
    overflow-y: auto;
    padding: 16px 12px 8px;
    -webkit-overflow-scrolling: touch;
  }
  .msg { display: flex; margin-bottom: 14px; align-items: flex-end; }
  .msg.me { justify-content: flex-end; }
  .msg .bubble {
    max-width: 74%;
    padding: 10px 14px;
    border-radius: 18px;
    font-size: 15px;
    line-height: 1.5;
    word-break: break-word;
    white-space: pre-wrap;
  }
  .msg.bot { flex-direction: column; align-items: flex-start; }
  .msg.bot .bubble {
    background: var(--bubble-bot);
    border-bottom-left-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
  }
  .tools {
    margin: 4px 0 0 6px;
    font-size: 11px;
    color: #7a86b8;
  }
  .msg.me .bubble {
    background: var(--bubble-me);
    color: #fff;
    border-bottom-right-radius: 4px;
  }
  .msg.typing .bubble { color: #999; }
  .dot { animation: blink 1.4s infinite both; display: inline-block; }
  .dot:nth-child(2) { animation-delay: .2s; }
  .dot:nth-child(3) { animation-delay: .4s; }
  @keyframes blink { 0%,80%,100% { opacity: .2; } 40% { opacity: 1; } }
  footer {
    flex-shrink: 0;
    display: flex;
    gap: 8px;
    padding: 10px 12px;
    background: #fff;
    border-top: 1px solid #e6e8f5;
  }
  footer input {
    flex: 1;
    border: 1px solid #e6e8f5;
    border-radius: 20px;
    padding: 10px 16px;
    font-size: 15px;
    outline: none;
  }
  footer input:focus { border-color: var(--brand); }
  footer button {
    background: var(--brand);
    color: #fff;
    border: none;
    border-radius: 20px;
    padding: 0 20px;
    font-size: 15px;
    cursor: pointer;
  }
  footer button:disabled { opacity: .5; }
</style>
</head>
<body>
  <header>
    <div class="avatar">🤖</div>
    <div>
      <div class="title">小助手</div>
      <div class="sub">日程 · 笔记 · 问答 · 在线</div>
    </div>
    <div class="spacer"></div>
    <button id="clearBtn" title="清空记忆，重新开始">清空记忆</button>
  </header>

  <div id="chat"></div>

  <footer>
    <input id="input" type="text" placeholder="说点什么，比如：帮我整理今天的待办…" autocomplete="off">
    <button id="sendBtn">发送</button>
  </footer>

<script>
  // 单机自用：用 localStorage 存一个固定 session_id，记忆跨刷新保留
  let sessionId = localStorage.getItem('assistant_session');
  if (!sessionId) {
    sessionId = 'web-' + Math.random().toString(36).slice(2, 10);
    localStorage.setItem('assistant_session', sessionId);
  }

  const chatEl = document.getElementById('chat');
  const inputEl = document.getElementById('input');
  const sendBtn = document.getElementById('sendBtn');
  const clearBtn = document.getElementById('clearBtn');

  function scrollBottom() { chatEl.scrollTop = chatEl.scrollHeight; }

  const TOOL_LABELS = {
    get_current_time: '时间查询',
    calculate: '计算器',
    search_notes: '笔记检索',
  };

  function addBubble(text, who, tools) {
    const wrap = document.createElement('div');
    wrap.className = 'msg ' + who;
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = text;
    wrap.appendChild(bubble);
    if (tools && tools.length) {
      const trace = document.createElement('div');
      trace.className = 'tools';
      trace.textContent = '调用工具：' + tools.map((t) => TOOL_LABELS[t] || t).join(' · ');
      wrap.appendChild(trace);
    }
    chatEl.appendChild(wrap);
    scrollBottom();
    return bubble;
  }

  function typingBubble() {
    const wrap = document.createElement('div');
    wrap.className = 'msg bot typing';
    wrap.id = 'typing';
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.innerHTML = '<span class="dot">●</span><span class="dot">●</span><span class="dot">●</span>';
    wrap.appendChild(bubble);
    chatEl.appendChild(wrap);
    scrollBottom();
  }

  function removeTyping() {
    const t = document.getElementById('typing');
    if (t) t.remove();
  }

  async function send() {
    const text = inputEl.value.trim();
    if (!text) return;
    inputEl.value = '';
    addBubble(text, 'me');
    sendBtn.disabled = true;
    typingBubble();
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, text: text }),
      });
      const data = await res.json();
      removeTyping();
      addBubble(data.reply || '（暂时没有获取到回复，请稍后重试）', 'bot', data.tools);
    } catch (e) {
      removeTyping();
      addBubble('（网络出错了，稍后再试）', 'bot');
    } finally {
      sendBtn.disabled = false;
      inputEl.focus();
    }
  }

  sendBtn.addEventListener('click', send);
  inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') send();
  });

  clearBtn.addEventListener('click', async () => {
    if (!confirm('确定要清空记忆吗？清空后将开启全新对话。')) return;
    try {
      await fetch('/api/clear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId }),
      });
      chatEl.innerHTML = '';
      addBubble('记忆已清空，我们重新开始。我是小助手，可以帮你梳理日程、整理笔记、解答问题。', 'bot');
    } catch (e) {
      alert('清空失败，稍后再试');
    }
  });

  // 开场白
  addBubble('你好，我是小助手。可以帮你梳理日程、整理笔记、解答问题，也可以陪你聊聊近况。', 'bot');
</script>
</body>
</html>"""


@app.get('/')
def index():
    return HTMLResponse(HTML)


@app.post('/api/chat')
def chat(req: ChatRequest):
    reply, tools = bot.chat_with_trace(req.session_id, req.text)
    return {'reply': reply, 'tools': tools}


@app.post('/api/clear')
def clear(req: ChatRequest):
    bot.clear(req.session_id)
    return {'ok': True}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
