import json

import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
refresh_token = '1d4095b6bff94bd39b135425f6ad32d7'

# 登录
response = requests.post(url=f'https://auth.aliyundrive.com/v2/account/token', json={'grant_type': 'refresh_token', 'refresh_token': refresh_token}, headers=headers)
response_json = json.loads(response.text)
print(response_json)
access_token, user_name = response_json['access_token'], response_json['user_name']
headers_copy = headers.copy()
headers_copy['Authorization'] = 'Bearer ' + access_token

# 签到
response = requests.post(url=f'https://member.aliyundrive.com/v1/activity/sign_in_list', json={'_rx-s': 'mobile'}, headers=headers_copy)
response_json = json.loads(response.text)
print(response_json)
signInCount = response_json['result']['signInCount']

# 领取奖励
response = requests.post(url=f'https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile', json={'signInDay': signInCount}, headers=headers_copy)
response_json = json.loads(response.text)
print(response_json)



