from assistant import Assistant

bot = Assistant()

print('小助手已上线（输入「清空记忆」可重置对话，输入 exit/quit/退出 结束）')

while True:
    user_input = input('>>> ').strip()

    if user_input in ('exit', 'quit', '退出'):
        print('再见，随时叫我。')
        break

    if user_input in ('清空', '清空记忆', '忘记我'):
        bot.clear('default')
        print('（记忆已清空，我们重新开始。）')
        continue

    print('小助手：', bot.chat('default', user_input))
