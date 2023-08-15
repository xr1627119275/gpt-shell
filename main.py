#!/bin/python3
# -*- coding: utf-8 -*-
import requests, json, sys, time

arg = sys.argv[1:]
if len(arg) < 1:
    print('Usage: <message>')
    exit(1)

# arg 数组 转字符串
message = " ".join(arg)
# Replace this URL with the URL of your EventSource server
url = 'https://chat9.fastgpt.me/api/openai/v1/chat/completions'
payload = {
    "messages": [
        {"role": "user", "content": "You are a Command Line Interface expert and your task is to provide functioning shell commands. Return a CLI command and nothing else - do not send it in a code block, quotes, or anything else, just the pure text CONTAINING ONLY THE COMMAND. If possible, return a one-line bash command or chain many commands together. Return ONLY the command ready to run in the terminal. The command should do the following:"},
        {"role": "user", "content": message or "centos 安装docker"},
    ],
    "stream": True,
    "model": "gpt-3.5-turbo",
    "temperature": 0.5,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "top_p": 1
}

headers = {
    "Content-Type": "application/json",
    "x-requested-with": "XMLHttpRequest",
}
response = requests.post(url, stream=True, data=json.dumps(payload), headers=headers)
if response.status_code == 200:
    isStop = False
    for line in response.iter_lines():
        if line and isStop is False:
            data = line.decode('utf-8')
            # 去掉开头的data:
            data = data.replace("data: ", "")
            # to json
            data = json.loads(data)
            choices = data['choices']
            for choice in choices:
                if 'finish_reason' in choice and (choice['finish_reason'] == 'stop'):
                    isStop = True
                    pass
                if 'delta' in choice and 'content' in choice['delta']:
                    conetnt = choice['delta']['content']
                    sys.stdout.write(conetnt)
                    sys.stdout.flush() 
                    time.sleep(0.1)
else:
    print(f'Failed to connect to the EventSource server: {response.status_code}', response.status_code)
print('')