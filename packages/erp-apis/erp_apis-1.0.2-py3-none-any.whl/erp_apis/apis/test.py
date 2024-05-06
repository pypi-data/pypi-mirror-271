# coding: utf-8
# Project：erp_out_of_stock
# File：test.py
# Author：李福成
# Date ：2024-04-28 18:24
# IDE：PyCharm
from apis.inventory import WmsSkuStock
from apis.order import OrderList, ChangeBatchItems
from apis.user import login
from apis.afterSales import aftersaleList, aftersaleCommon, clearException

from request import Session

if __name__ == '__main__':
    session = Session()
    session.erpSend(login(
        username="",
        password=""
    ))
    # 获取分仓库存
    # order = session.erpSend(OrderList(queryData=[{"k": "o_id", "v": "39104496", "c": "@="}])).json()['ReturnValue']['datas'][0]
    # print(order)
    # res = session.erpSend(ChangeBatchItems(
    #     oid = order['o_id'],
    #     items = order['items'],
    #     newBatchItems = [
    #         {
    #             "sku_id": "M-男女宽松T-福袋",
    #             "oi_id": order['items'][0]['oi_id'],
    #         }
    #     ]
    # ))
    # res = session.erpSend(aftersaleList([{
    #     "k": "shop_id",
    #     "v": "15429635,14421166,14129300,14409794,13077664,11288284,12151690,12391281,11288291,10341596,15581347,13116222,14242518,14163461,14163558,15517378,15297892,15513593,14420990,14699171,15982786,15748932,14699049,13530518,13445299,14421297,11700009,11725757,14484991,13168313,14418703,13168328",
    #     "c": "@="}, {"k": "status", "v": "waitconfirm", "c": "@="}, {"k": "type", "v": "换货", "c": "@="},
    #     {"k": "shop_type", "v": "换货", "c": "@="}, {"k": "as_date", "v": "30天前", "c": ">=", "t": "date"},
    #     {"k": "as_date", "v": "今天 23:59:59.999", "c": "<=", "t": "date"}])
    # )
    # res = session.erpSend(aftersaleCommon(1452451077))
    res = session.erpSend(clearException(1452451077))
    print(res.json())
