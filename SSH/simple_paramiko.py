# *-* coding:utf-8 *-*
#!/usr/bin/env python3

"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/9 下午4:16
desc: 基于密码使用paramiko远程连接
"""

import paramiko
import time
import os

hostname = '192.168.1.21'
username = 'root'
password = '123456789'

paramiko.util.log_to_file('syslogin.log')       # 发送 paramiko 日志到 syslogin.log文件
ssh = paramiko.SSHClient()      # 创建一个ssh客户端client对象
ssh.load_system_host_keys()     # 获取客户端 host_keys，默认 ~/.ssh/known_hosts, 非默认路径需指定

# 使用秘钥代码块
# privatekey = os.path.expanduser("/home/key/id_rsa")     # 定义私钥存放路径
# key = paramiko.RSAKey.from_private_key_file(privatekey)     # 创建私钥对象key
# ssh.connect(hostname=hostname, username=username, pkey=key, timeout=5)        # 创建ssh连接

ssh.connect(hostname=hostname, username=username, password=password, timeout=5)        # 创建ssh连接
stdin, stdout, stderr = ssh.exec_command('ifconfig')     # 调用远程执行命令方法exec_command()
print(stdout.read().decode())        # 打印命令执行结果，得到Python列表形式，可以使用stdout.readlines()

time.sleep(5)       # 结果缓冲释放过快未读完会报错，加sleep
ssh.close()     # 关闭连接
