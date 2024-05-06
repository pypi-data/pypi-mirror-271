# coding: utf-8
# Project：erp_out_of_stock
# File：user.py
# Author：李福成
# Date ：2024-04-28 18:23
# IDE：PyCharm
# 用户API

from request import Request

def login(username: str, password: str):
    '''
    登录
    :param username: 账号
    :param password: 密码
    :return:
    '''
    return Request(
        method='post',
        url='https://api.erp321.com/erp/webapi/UserApi/WebLogin/Passport',
        json={
            "data": {
                "account": username,
                "password": password,
                "j_d_3": "",
                "v_d_144": "",
                "isApp": False
            },
            "ipAddress": ""
        },
        callback='login',
        hostType='erpApi'
    )



