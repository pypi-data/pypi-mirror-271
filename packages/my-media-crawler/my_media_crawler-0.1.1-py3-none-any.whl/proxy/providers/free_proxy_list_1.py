# -*- coding: utf-8 -*-
# @Author  : relakkes@gmail.com
# @Time    : 2024/4/5 09:32
# @Desc    : 极速HTTP代理提供类实现,官网地址：https://www.jisuhttp.com?pl=zG3Jna
from ctypes import util
import os
import re
from shlex import join
from typing import Dict, List
from urllib.parse import urlencode

from fastapi.background import P
import httpx
from bs4 import BeautifulSoup

from proxy import IpGetError, ProxyProvider, RedisDbIpCache
from proxy.types import IpInfoModel
from tools import utils


class FreeProxyList1(ProxyProvider):
    def __init__(self, time_validity_period: int):
        """
        https://www.proxy-list.download/api/v1 socks 代理IP实现
        :param key: 提取key值 (去官网注册后获取)
        :param crypto: 加密签名 (去官网注册后获取)
        """
        self.proxy_brand_name = "FREE_PROXY_LIST_PROVIDER_1ST"
        self.api_path = "https://www.proxy-list.download/api/v1/get"
        self.my_proxy = httpx.URL("http://127.0.0.1:8889")
        # type=http&anon=elite&country=US
        self.params = {
            "type": "http",
            "anon": "elite",
            "country": "US",
        }
        self.time_validity_period = time_validity_period
        self.proxy_protocol = 'http://' if 'http' == self.params['type'] else 'https://'
        self.ip_cache = RedisDbIpCache()

    def _generate_ips_from_rows(self, rows: List[str]) -> List[Dict[str, str]]:
        ip_port_list = []

        for row in rows:
            match = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', row)
            if match:
                ip_port_dict = {}
                ip_port_dict["ip"] = match.group(1)
                ip_port_dict["port"] = match.group(2)
                ip_port_dict["expire"] = utils.increase_timestamp_by_minutes(utils.get_current_timestamp(), self.time_validity_period)
                ip_port_list.append(ip_port_dict)
                
        return ip_port_list

    def _extract_ip_port_from_html(self, raw_html: str) -> List[Dict[str, str]]:
        ip_port_list = []

        if not raw_html:
            return ip_port_list

        soup = BeautifulSoup(raw_html)
        elements = soup.find_all('p', 'tprinc')
        innerStrings = [ item.replace('\n', '').strip() for element in elements for item in element if isinstance(item, str)] if elements else None

        if not innerStrings:
            return ip_port_list

        return self._generate_ips_from_rows(innerStrings)

    def _extract_ip_port_form_text(self, raw_text: str) -> List[Dict[str, str]]:
        ip_port_list = []

        rows = raw_text.split('\r\n') if raw_text else None

        if not rows:
            return ip_port_list

        return self._generate_ips_from_rows(rows)

    async def get_proxies(self, num: int) -> List[IpInfoModel]:
        """
        :param num:
        :return:
        """

        # 优先从缓存中拿 IP
        ip_cache_list = self.ip_cache.load_all_ip(proxy_brand_name=self.proxy_brand_name)
        if len(ip_cache_list) >= num:
            return ip_cache_list[:num]

        # 如果缓存中的数量不够，从IP代理商获取补上，再存入缓存中
        need_get_count = num - len(ip_cache_list)
        self.params.update({"num": need_get_count})
        ip_infos = []
        async with httpx.AsyncClient(proxies=self.my_proxy) as client:
            url = self.api_path + '?' + urlencode(self.params)
            utils.logger.info(f"[FreeProxyList1.get_proxies] get ip proxy url:{url}")
            # https://www.proxy-list.download/api/v1/get?type=http&anon=elite&country=US
            response = await client.get(url, headers={
                "User-Agent": "FakeUserAgent eli"})
            res_text = response.text
            ip_list: Dict = self._extract_ip_port_form_text(res_text)
            if bool(ip_list):
                current_ts = utils.get_unix_timestamp()
                for ip_item in ip_list:
                    ip_info_model = IpInfoModel(
                        ip=ip_item.get("ip"),
                        port=ip_item.get("port"),
                        user='',
                        password='',
                        protocol=self.proxy_protocol,
                        expired_time_ts=current_ts + (5 * 60)
                    )
                    ip_key = f"{self.proxy_brand_name}_{self.params['type']}_{ip_info_model.ip}_{ip_info_model.port}_{ip_info_model.user}_{ip_info_model.password}"
                    ip_value = ip_info_model.json()
                    ip_infos.append(ip_info_model)
                    self.ip_cache.set_ip(ip_key, ip_value, ex=ip_info_model.expired_time_ts - current_ts)
            else:
                raise IpGetError(response.status_code)
        return ip_cache_list + ip_infos


def new_free_proxy_1() -> FreeProxyList1:
    """
    构造极速HTTP实例
    Returns:

    """
    return FreeProxyList1(
        time_validity_period=5  # 30分钟（最长时效）
    )

if __name__ == '__main__':
    proxies = new_free_proxy_1()
    print(proxies)