# coding: utf-8
# Project：erp_sdk_python
# File：itemtool.py
# Author：李福成
# Date ：2024/5/7 上午10:42
# IDE：PyCharm
from typing import Optional

from request import Request
from utils.util import getDefaultParams, JTable1, dumps


def ItemtoolRequest(
        data: dict,
        method: str = 'LoadDataToJSON',
        url: str = '/app/item/itemtool/itemContrast.aspx', **kwargs
) -> Request:
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

def ItemList(queryData: Optional[list] = None, page_num: int = 1, page_size: int = 500):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []
    return ItemtoolRequest({
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

# itemContrast