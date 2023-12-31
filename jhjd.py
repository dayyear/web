import datetime
import json
import time

import pytz
import requests
from dateutil.relativedelta import relativedelta


# 判断本周是否跨月
def is_week_across_months(today):
    end_of_week = today + relativedelta(weekday=6)  # 利用relativedelta将日期调整到本周的最后一天end_of_week
    return today.month != end_of_week.month


# 我的月度积分, 第一名月度积分
def get_month_point(token, headers):
    url = f'https://jhjd.ntgaj.cn/api/app/actvity/rank/v1?type=1&token={token}'
    response = requests.get(url=url, headers=headers)
    response_json = json.loads(response.text)
    return int(response_json['data']['myRank']['monthPoints']), int(response_json['data']['rankList'][0]['monthPoints'])


def run(token):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6939'}

    # 个人中心
    response_json = json.loads(requests.get(url=f'https://jhjd.ntgaj.cn/api/app/member/detail?token={token}', headers=headers).text)
    print('[个人中心]', response_json['data']['nickname'], response_json['data']['deptName'], response_json['data']['postName'], '月度积分:', response_json['data']['monthPoints'], '今日得分:', response_json['data']['todayPoints'])

    # 周测
    try:
        url = f'https://jhjd.ntgaj.cn/api/app/actvity/week/list?token={token}'
        response = requests.get(url=url, headers=headers)
        week_list_json = json.loads(response.text)
        for week_json in week_list_json['page']['data']:  # 遍历周测列表
            today = datetime.datetime.now().astimezone(pytz.timezone('Asia/Shanghai'))
            if is_week_across_months(today):
                print('[周测] 本周跨月，周测暂缓', today)
                break
            if week_json['completeStatus'] == 1:
                break
            my_month_point, first_month_point = get_month_point(token, headers)
            if my_month_point > first_month_point - 5:
                break
            question_list = requests.get(f'https://jhjd.ntgaj.cn/api/app/actvity/week/detail?activityId={week_json["id"]}&token={token}')
            question_list_json = json.loads(question_list.text)
            my_answer_list = []
            for question_json in question_list_json['data']:  # 遍历题目
                if question_json['questionType'] == 1:  # 单选题
                    answer = question_json['remark'][0]
                elif question_json['questionType'] == 2:  # 多选题
                    answer = ';'.join(question_json['remark'])
                else:
                    raise Exception(f"未知的questionType：{question_json['questionType']}")
                my_answer_list.append({'questionId': question_json['id'], 'answer': answer, 'activityId': question_json['activityId']})
            time.sleep(2)
            response_json = json.loads(requests.post(url=f'https://jhjd.ntgaj.cn/api/app/actvity/day/submit?token={token}', json=my_answer_list, headers=headers).text)
            print('[周测]', my_answer_list, response_json)
            break
    except Exception as ex:
        print(f'[周测] 发生错误：{ex}')

    # 日课
    try:
        study_id_list, study_type_list = [], [1, 2, 4]
        for study_type in study_type_list:
            response_json = json.loads(requests.get(url=f'https://jhjd.ntgaj.cn/api/app/study/today?studyType={study_type}&token={token}').text)
            if response_json['data'][0]['readStatus'] == 1:  # 过滤掉已学
                continue
            study_id_list.append(response_json['data'][0]['id'])
        study_id_list.sort()
        for study_id in study_id_list:
            my_month_point, first_month_point = get_month_point(token, headers)
            if my_month_point >= first_month_point:
                break
            time.sleep(2)
            response_json = json.loads(requests.post(url=f'https://jhjd.ntgaj.cn/api/app/study/addScore?token={token}', data={'studyId': study_id}, headers=headers).text)
            print('[日课]', study_id, response_json)
    except Exception as ex:
        print(f'[日课] 发生错误：{ex}')

    # 资讯
    try:
        news_id_list = []
        response_json = json.loads(requests.get(url=f'https://jhjd.ntgaj.cn/api/app/news/recommend?token={token}').text)
        for news in response_json['data']:
            news_id_list.append(news['id'])
        response_json = json.loads(requests.get(url=f'https://jhjd.ntgaj.cn/api/app/news/list?token={token}').text)
        for news in response_json['page']['data']:
            if news['readStatus'] == 1:  # 过滤掉已读
                continue
            news_id_list.append(news['id'])
        news_id_list.sort()
        for news_id in news_id_list:
            my_month_point, first_month_point = get_month_point(token, headers)
            if my_month_point >= first_month_point:
                break
            time.sleep(2)
            response_json = json.loads(requests.post(url=f'https://jhjd.ntgaj.cn/api/app/news/addScore?token={token}', data={'newsId': news_id}, headers=headers).text)
            print('[资讯]', news_id, response_json)
    except Exception as ex:
        print(f'[资讯] 发生错误：{ex}')


if __name__ == '__main__':
    tokens = [
        '8f468c873a32bb0619eaeb2050ba45d1',  # 顾xiaojing
        '92977ae4d2ba21425a59afb269c2a14e',  # 王peipei
        'ca75910166da03ff9d4655a0338e6b09',  # 张lihua
        '4311359ed4969e8401880e3c1836fbe1',  # 张yi
        '9aa42b31882ec039965f3c4923ce901b',  # 王ning
        'c22abfa379f38b5b0411bc11fa9bf92f'  # self
    ]
    for token in tokens:
        try:
            run(token)
        except Exception as ex:
            print(f'[{token}] 发生错误：{ex}')
