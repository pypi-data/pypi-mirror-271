from socket import AF_INET
from typing import Dict

import psutil
from rich.console import RenderableType

from elegantmotd.sysinfo import SysInfo


class Network(SysInfo):
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        infos = {"Network": ""}

        addrs = psutil.net_if_addrs()
        for intf, addr_list in addrs.items():
            if intf != "lo":
                for addr in addr_list:
                    if addr.family == AF_INET:
                        infos[f"  - {intf}"] = addr.address

        return infos
