#   注册入口 https://www.rainyun.com/NDYxOTUz_
#   注册登录后在‘账户设置’获得api key值
#   创建环境变量 s_yuyun,将上面获取的api_key值填入 
#   cron: 0 8 * * *
#   const $ = new Env('雨云签到');
import requests
import json
import os  

# 从青龙面板的环境变量中获取API密钥
api_key = os.getenv('s_yuyun')  # 使用您设置的环境变量名

if api_key is None:
    print("环境变量 's_yuyun' 未设置或无法获取")
    exit(1)  # 如果环境变量未设置，退出脚本

# 定义API端点URL
url = 'https://api.v2.rainyun.com/user/reward/tasks'

# 定义请求头部
headers = {
    'x-api-key': api_key,  # 使用环境变量中的API密钥
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Content-Type': 'application/json'
}

# 定义请求体
data = {
    "task_name": "每日签到"
}

# 发送POST请求
response = requests.post(url, headers=headers, json=data)  # 使用json参数直接发送JSON数据

# 检查请求是否成功
if response.ok:
    print('请求成功，响应内容：')
    print(response.text)
else:
    print('请求失败，状态码：', response.status_code)
