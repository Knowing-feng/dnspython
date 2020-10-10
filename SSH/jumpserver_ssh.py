# *-* coding:utf-8 *-*
#!/usr/bin/env python3

"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/10 下午1:32
desc: 实现堡垒机模式下的远程命令执行
"""

import paramiko
import sys

blip = '192.168.1.23'       # 定义跳板机IP
bluser = 'root'
blpasswd = 'mypassword'

hostname = '192.168.1.1'        # 定义业务服务器信息
username = 'root'
password = 'mypassword'

port = 22
passinfo = "'s password:"       # 输入服务器密码的前标志串

ssh = paramiko.SSHClient()      # 创建会话，开启命令调用
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect(blip, port, bluser, blpasswd)

channel = ssh.invoke_shell()    # 创建会话，开启命令调用
channel.settimeout(10)          # 会话命令执行超时时间，单位为秒

buff = ''
resp = ''
channel.send('ssh ' + username + '@' + hostname + '\n')     # 执行ssh登入业务主机
with not buff.endswith(passinfo):       # ssh登入的提示判断，输出串尾含有"\s password:"时 退出while循环
    try:
        resp = channel.recv(9999)
    except Exception as e:
        print(f'Error info :{str(e)} connection time.')
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp
    if not buff.find('yes/no') == -1:
        channel.send('yes\n')
        buff = ''

channel.send(password + '\n')       # 发送业务主机密码
buff = ''
while not buff.endswith('# '):       # 输出串尾为'# '时说明校验通过并退出while循环
    resp = channel.recv(9999)
    if not resp.find(passinfo) == -1:       # 删除串尾含有's password: 时说明密码不正确，要求重新输入
        print('Error info : Authentication failed.')
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp

channel.send('ifconfig\n')      # 认真后通过发送ifconfig命令来查看结果
buff = ''
try:
    while buff.find('# ') == -1:
        resp = channel.recv(9999)
        buff += resp
except Exception as e:
    print(f'error info :{str(e)}')

print(buff)     # 打印输出串
channel.close
ssh.close()