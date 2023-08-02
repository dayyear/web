import datetime

import pytz


today = datetime.datetime.now().astimezone(pytz.timezone('Asia/Shanghai'))
print(today)
