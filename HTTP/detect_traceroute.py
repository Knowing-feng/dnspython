import os
import sys
import time
import subprocess
import logging
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.layers.inet import traceroute

domains = input('Please input one or more IP/domain: ')     # 接受输入的域名或IP
target = domains.strip()
dport = [80]    # 扫面的端口列表

if len(target) >= 1 and all([target]):
    res, unans = traceroute(target, dport=dport, retry=-2)  # 启动路由跟踪
    res.graph(target="> test.svg")
    time.sleep(1)
    subprocess.Popen("/usr/bin/convert test.svg test.png", shell=True)  # SVG转PNG格式
else:
    print("IP/domain number of errors, exit")
