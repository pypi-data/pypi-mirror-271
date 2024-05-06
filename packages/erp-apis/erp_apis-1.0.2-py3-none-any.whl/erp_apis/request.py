# coding: utf-8
# Project：invoices
# File：request.py
# Author：李福成
# Date ：2024-04-09 11:20
# IDE：PyCharm
import os
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

from lxml import etree
from requests import Session as S, Request as R
import time, json as j
from config import DEFAULT_HEADERS, Erp321BaseUrl, ErpApiBaseUrl


@dataclass
class UserInfoType:
    u_cid: Optional[str]
    u_co_id: Optional[str]
    u_co_name: Optional[str]
    u_id: Optional[str]
    u_name: Optional[str]
    u_lid: Optional[str]
    def __init__(self, **kwargs):pass



class Session(S):
    def __init__(self):
        super().__init__()
        self.headers.update(DEFAULT_HEADERS)
        self.proxies = {'http': "", 'https': ""}
        self.viewstateItems = dict()
        self.userInfo : Optional[UserInfoType]



    def erpSend(self, request:R, **kwargs):
        if not request.headers: request.headers = self.headers
        hostType = getattr(request, 'hostType', None)
        if hostType:
            resp = getattr(self, hostType + "Send", None)(request, **kwargs)
            if resp is None:
                raise Exception(f"{hostType}没有这个域的send方法")
            return resp
        raise Exception('hostType is None')


    def erp321Send(self, request, **kwargs):
        request.url = urljoin(Erp321BaseUrl, request.url)
        if request.method == 'POST':
            request.headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
            request.data.update({k: v for k, v in self.get_viewstate(request.url).items() if k and k != "updateTime"})
        res = super().send(self.prepare_request(request), **kwargs)
        if request.callback:
            return request.callback(res)
        return res

    def erpApiSend(self, request, **kwargs):
        request.url = urljoin(ErpApiBaseUrl, request.url)
        res = super().send(self.prepare_request(request), **kwargs)
        if request.callback:
            if request.callback == 'login':
                self.userInfo = UserInfoType(**res.json().get('cookie'))
            else:
                return request.callback(res)
        return res

    def get_viewstate(self, url):
        if self.viewstateItems.get(url) and self.viewstateItems.get(url).get("updateTime") > time.time() - 60 * 5:
            return self.viewstateItems.get(url)
        if not self.viewstateItems.get(url):
            self.viewstateItems.update({url: {"updateTime": time.time()}})
        res = self.get(url)
        etree_xpath = etree.HTML(res.text)

        def extract_first(xpath):
            r = etree_xpath.xpath(xpath)
            return r[0] if r else None

        self.viewstateItems.get(url).update(
            {
                "__VIEWSTATE": extract_first("//*[@id='__VIEWSTATE']/@value"),
                "__VIEWSTATEGENERATOR": extract_first("//*[@id='__VIEWSTATEGENERATOR']/@value"),
                "__EVENTVALIDATION": extract_first("//*[@id='__EVENTVALIDATION']/@value"),
            }
        )
        return self.viewstateItems.get(url)


class Request(R):

    def __init__(self,
                 hostType: str = 'erp321',
                 callback: callable=None,
                 **kwargs
        ):
        self.hostType = hostType
        self.callback = callback
        super().__init__(**kwargs)