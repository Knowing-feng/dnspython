#!/usr/bin/python3
# *-* coding:utf-8 *-*

import time
import pyclamd
from threading import Thread


class Scan(Thread):
    def __int__(self, IP, scan_type, file):
        """构建方法，参数初始化"""
        Thread.__init__(self)
        self.IP = IP
        self.scan_type = scan_type
        self.file = file
        self.connstr = ""
        self.scan_result = ""

    def run(self):
        """多进程run方法"""
        try:
            cd = pyclamd.ClamdNetworkSocket(self.IP, 3310)  # 创建网络套接字连接对象
            if cd.ping():
                self.connstr = self.IP + " connection [OK]"
                cd.reload()
                if self.scan_type == "contscan_file":        # 选择不同的扫描模式
                    self.scan_result = f"{cd.contscan_file(self.file)}\n"
                elif self.scan_type == "multiscan_file":
                    self.scan_result = f"{cd.multiscan_file(self.file)}\n"
                elif self.scan_type == "scan_file":
                    self.scan_result = f"{cd.scan_file(self.file)}\n"
                time.sleep(1)   # 线程挂起1秒
            else:
                self.connstr = self.IP + " ping error, exit"
                return False
        except Exception as e:
            self.connstr = self.IP + " " + str(e)
