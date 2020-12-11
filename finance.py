#!/usr/bin/env python
# encoding: utf-8
"""
@author: tx
@File    : finance.py
@Time    : 2020-12-10 17:02
@desc    :
"""
import requests
import json
from hashlib import md5
import time

APP_KEY = '7b441be2cea345cxxxxxxx'
app_secret = '7994e6f10e6xxxxxxx'

refresh_token_1 = 'http://xx.xx.xx.xx:80/gateway/app/refreshTokenByKey.htm'
refresh_token_2 = 'http://xx.xx.xx.xx:80/gateway/app/refreshTokenBySec.htm'


def calcute_dead_time(request_time, over_time):
    """
    根据请求时间戳，计算过期时间戳
    :param request_time: 时间戳
    :param over_time: 分钟
    :return: 时间戳
    """
    # request_time 1607501225287
    seconds_over_time = over_time * 60
    return request_time + seconds_over_time * 1000


def request_finance_token(url, params, req_type='get'):
    if req_type == 'get':
        response = requests.get(url, params)
    else:
        response = requests.post(url, params)
    return response


def check_token(request_time):
    """
    检查 token 是否超时  刷新秘钥有效时间为48小时，请求秘钥有效时间为15分钟
    :param request_time:
    :return: 刷新密钥
    """

    with open('refresh_token.json', 'r', encoding='utf-8') as fp:
        line = fp.readline()
    if not line:
        print('未读取到数据， 需要写入')
        sign = encrypt_sign(request_time, app_secret)
        params = {
            'appKey': APP_KEY,
            'sign': sign,
            'requestTime': request_time
        }
        # TODO 获取更新与请求 token 写入文件
        response = request_finance_token(refresh_token_1, params, req_type='get')
        print('response', response.text)
        js_response = json.loads(response.text)
        # {"code": "00", "msg": "成功", "data": "",
        #  "datas": {"refreshSecret": "e47be6e19707410b8337d5f05ef581a6", "refreshSecretEndTime": 1607765957938,
        #            "requestSecret": "4240021840844ba0b428914612982dba", "requestSecretEndTime": 1607594057938},
        #  "dataCount": 0, "totalDataCount": 0, "totalPage": 1, "requestId": null, "interfaces": null}
        if js_response['code'] == "00":
            w_dict = {
                'refresh_key': js_response['datas']['refreshSecret'],
                'request_key': js_response['datas']['requestSecret'],
                'update_time': request_time,
                'refresh_dead_time': js_response['datas']['refreshSecretEndTime'],  # 刷新密钥过期时间
                'request_dead_time': js_response['datas']['requestSecretEndTime']  # 请求密钥过期时间
            }
            with open('refresh_token.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(w_dict))
                print('写入 token 完成')

    else:
        token_json_data = json.loads(line)

        if request_time > token_json_data['request_dead_time']:
            print('更新请求 token')
            # 请求密钥15min失效  请使用APP_KEY、刷新秘钥获取刷新秘钥和请求秘钥
            sign = encrypt_sign(request_time, token_json_data['refresh_key'])
            params = {
                'appKey': APP_KEY,
                'sign': sign,
                'requestTime': request_time
            }
            response = request_finance_token(refresh_token_2, params, req_type='get')
            print('更新请求 token返回结果', response.text)

            js_response = json.loads(response.text)
            if js_response['code'] == "00":
                w_dict = {
                    'refresh_key': js_response['datas']['refreshSecret'],
                    'request_key': js_response['datas']['requestSecret'],
                    'update_time': request_time,
                    'refresh_dead_time': js_response['datas']['refreshSecretEndTime'],  # 刷新密钥过期时间
                    'request_dead_time': js_response['datas']['requestSecretEndTime']  # 请求密钥过期时间
                }

        elif request_time > token_json_data['refresh_dead_time']:
            print('更新刷新 token')
            # 刷新密钥48h失效 请使用APP_KEY、APP秘钥获取刷新秘钥与请求秘钥。
            sign = encrypt_sign(request_time, app_secret)
            params = {
                'appKey': APP_KEY,
                'sign': sign,
                'requestTime': request_time
            }
            # TODO 获取更新与请求 token 写入文件
            response = request_finance_token(refresh_token_2, params, req_type='get')
            print('response', response.text)
            js_response = json.loads(response.text)
            if js_response['code'] == "00":
                w_dict = {
                    'refresh_key': js_response['datas']['refreshSecret'],
                    'request_key': js_response['datas']['requestSecret'],
                    'update_time': request_time,
                    'refresh_dead_time': js_response['datas']['refreshSecretEndTime'],  # 刷新密钥过期时间
                    'request_dead_time': js_response['datas']['requestSecretEndTime']  # 请求密钥过期时间
                }
        else:
            return token_json_data['request_key']

        with open('refresh_token.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(w_dict))

    return w_dict['request_key']


def encrypt_sign(long_time, app_secret):
    """
    md5 加密
    :param long_time:
    :param app_secret:
    :return:
    """
    s = md5()
    encrypt_string = APP_KEY + app_secret + str(long_time)
    s.update(encrypt_string.encode('utf-8'))
    return s.hexdigest()


def ucn_code_to_company(ucncode):
    """
    通过信用社代码调用接口查询公司名称
    :param kwargs:
    :return:
    """

    print('统一信用社代码', ucncode)

    request_time = int(round(time.time() * 1000))
    request_key = check_token(request_time)

    # TODO: 通过接口获取相关公司名称
    print('放入接口的请求密钥', request_key)
    # url = 'http://xx.xx.xx.xx:80/gateway/app/refreshTokenByKey.htm'
    # response = requests.post(url, params)

    company_name = '测试科技公司'
    return company_name


ucncode = '91330683MA2BHN2683'

company_name = ucn_code_to_company(ucncode)
print('公司名:', company_name)


