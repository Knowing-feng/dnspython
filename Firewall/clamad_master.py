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


IPs = ["103.9.231.221"]         # 扫描主机列表
scan_type = "multiscan_file"    # 传输扫描Scan类线程对象列表
scan_file = '/root'              # 指定扫描路径
i = 1

threadnum = 2   # 指定启动的线程数
scan_list = list()  # 存储扫描Scan类线程对象列表

for ip in IPs:
    currp = Scan(ip, scan_type, scan_file)     # 创建扫描Scan类对象，参数(IP, 扫描模式, 扫描路径)
    scan_list.append(currp)     # 追加对象到列表
    
    if i % threadnum == 0 or i == len(IPs):     # 当达到指定线程数 或 IP列表数后启动 ，退出线程
        for task in scan_list:
            task.start()    # 启动线程
        for task in scan_list:
            task.join()     # 等待所有子线程退出，并输出扫描结果
            print(task.connstr)     # 打印服务器连接信息
            print(task.scan_result) # 打印扫描结果

