# coding: utf-8
# Project：erp_out_of_stock
# File：inventory.py
# Author：李福成
# Date ：2024-04-28 18:27
# IDE：PyCharm
# 库存
from typing import Optional
from request import Request
from utils.util import getDefaultParams, dumps, JTable1


# 查询库存
def WmsSkuStock(queryData: Optional[list] = None, page_num: int = 1, page_size: int = 500):
    '''
    查询库存(分仓)
    :param page_num:  页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''


    return Request(
        method='POST',
        url='https://www.erp321.com/app/item/SkuStock/WmsSkuStock.aspx',
        params=getDefaultParams({'defaultParams': ["ts___", "_c",'am___']}),
        data={
            '_jt_page_size': page_size,
            '__CALLBACKID': 'JTable1',
            '__CALLBACKPARAM': dumps({"Method": "LoadDataToJSON", "Args": [str(page_num), dumps(queryData), "{}"]})
        },
        callback=JTable1
    )
