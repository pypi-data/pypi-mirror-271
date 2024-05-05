import re
import asyncio
from typing import Dict, List
from urllib.parse import urlencode
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import httpx

from tools import utils
from proxy import IpGetError
from proxy.types import IpInfoModel

def _extract_ip_port(raw_ips: str) -> List[Dict[str, str]]:
    rows = raw_ips.split('\n')
    ip_port_list = []

    time_validity_period = 3

    for row in rows:
        match = re.match(r'(\d+\.\d+\.\d+\.\d+\.\d+):(\d+)', row)
        if match:
            ip_port_dict = {}
            ip_port_dict["ip"] = match.group(1)
            ip_port_dict["port"] = match.group(2)
            ip_port_dict["_expire"] = int(utils.get_unix_timestamp()) + int(time_validity_period)
            ip_port_dict["expire"] = utils.increase_timestamp_by_minutes(utils.get_current_timestamp(), time_validity_period)
            ip_port_list.append(ip_port_dict)
            
    return ip_port_list

async def get_ips(num: int) -> List[Dict[str, str]]:
    """
    get the fuck out
    """
    params = {
        "type": "http",
        "anon": "elite",
        "country": "US",
    }
    api_path = "https://www.proxy-list.download/api/v1"
    ip_infos = []

    async with httpx.AsyncClient(proxies=httpx.URL('http://127.0.0.1:8889')) as client:
        url = api_path + '?' + urlencode(params)
        utils.logger.info(f"[FreeProxyList1.get_proxies] get ip proxy url:{url}")
        response = await client.get(url, headers={
            "User-Agent": "FakeUserAgent eli"})
        res_text = response.text
        res_dict: Dict = _extract_ip_port(res_text)
        if bool(res_dict):
            for ip_item in res_dict:
                ip_info_model = IpInfoModel(
                    ip=ip_item.get("ip"),
                    port=ip_item.get("port"),
                    user='default',
                    password='default',
                    expired_time_ts=utils.get_unix_time_from_time_str(ip_item.get("expire"))
                )
                ip_infos.append(ip_info_model)
        else:
            raise IpGetError(response.status_code)
    return ip_infos

if __name__ == '__main__':
    ips = asyncio.get_event_loop().run_until_complete(get_ips(5))
    print(ips)