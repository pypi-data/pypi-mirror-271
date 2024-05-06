# coding: utf-8
# Project：erp_out_of_stock
# File：order.py
# Author：李福成
# Date ：2024-04-28 18:23
# IDE：PyCharm
# 订单API
from typing import Optional, Union
from request import Request
from utils.util import dumps, getDefaultParams, JTable1, generateChangeBatchItems


def OrderRequest(data: dict, method: str = 'LoadDataToJSON',
                 url: str = '/app/Service/aftersale/aftersale.aspx', **kwargs) -> Request:
    params = getDefaultParams({'defaultParams': ["ts___"], 'am___': method})
    if kwargs.get('params'):
        params.update(kwargs.get('params'))
    return Request(
        method='POST',
        url=url,
        params=params,
        data={
            **data
        },
        callback=JTable1
    )


# 获取售后退货退款订单
def aftersaleList(queryData: Optional[list] = None, page_num: int = 1, page_size: int = 500):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []
    return OrderRequest({
        '_jt_page_size': page_size,
        "__CALLBACKID": "JTable1",
        '__CALLBACKPARAM': dumps(
            {
                "Method": "LoadDataToJSON",
                "Args": [
                    page_num,
                    dumps(queryData),
                    "{}"
                ]
            }
        ),
    },
        method='LoadDataToJSON',
        params={'archive': 'false'}
    )


# 确认售后订单
def aftersaleCommon(afterId: Union[str, int]):
    '''
    确认售后订单
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return OrderRequest({
        'isCB': '0',
        '__CALLBACKID': 'ACall1',
        '__CALLBACKPARAM': dumps(
            {
                "Method": "Confirms",
                "Args": [str(afterId), "false", "true", "false", "false", "false"],
             "CallControl": "{page}"
            }
        ),
    },
        method='Confirms',
        url='/app/Service/aftersale/aftersale_common.aspx'
    )


# 售后单转转成
def clearException(afterId: Union[str, int]):
    '''
    售后单转转成
    :param oid:  内部订单号
    :return: 执行结果
    '''
    return OrderRequest({
        '__CALLBACKID': 'JTable1',
        '__CALLBACKPARAM': dumps({"Method":"ClearException","Args":[afterId],"CallControl":"{page}"}),
    },
        method='ClearException')