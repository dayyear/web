import json

import requests

mobile, name = '060xxx', '张三'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6939'}
response_json = json.loads(requests.post(url=f'https://jhjd.ntgaj.cn/api/app/login/bind', data={'mobile': mobile, 'name': name, 'openid': 'oCiUK5dPQTPRAV4EfjKjX4OOzTaQ'}, headers=headers).text)
print('[绑定]', mobile, name, response_json['data']['token'])
