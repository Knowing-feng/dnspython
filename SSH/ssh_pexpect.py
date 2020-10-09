# *-* coding:utf-8 *-*
#!/usr/bin/env python3

"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/8 下午7:51
desc: 远程文件自动打包并下载
"""
import pexpect

IP = '127.0.0.1'            # 定义目标主机
USER = 'root'               # 目标主机用户
PASSWORD = '123456789'      # 目标主机密码
target_file = '/root/get-pip.py'     # 目标主机文件

child = pexpect.spawn('/usr/bin/ssh', [USER + '@' + IP])    # 运行ssh命令
fout = open('mylog.txt', 'wb')                  # 输入,输出日志写入mylog.txt文件
child.logfile = fout

try:
    child.expect('(?i)password')        # 匹配password字符串,(?i)表示不区分大小写
    child.sendline(PASSWORD)
    child.expect('#')
    child.sendline('tar zcf /opt/test.tar.gz ' + target_file)       # 打包文件
    child.expect('#')
    child.sendline('exit')
    child.close()
except EOFError:    # 定义EOF异常处理
    print('expect EOF')
except TimeoutError:    # 定义TIMEOUT异常处理
    print('expect TIMEOUT')

child = pexpect.spawn('/usr/bin/scp', [USER+ '@' + IP + ':/opt/test.tar.gz', '/home/smoker'])   # 将打包好的文件,复制到本地
fout = open('mylog.txt', 'ab')
child.logfile = fout

try:
    child.expect('(?i)password')
    child.sendline(PASSWORD)
    child.expect(pexpect.EOF)       # 匹配缓冲区EOF(结尾), 保证文件复制正常完成
    child.close()
except EOFError:
    print('expect EOF')
except TimeoutError:
    print('expect TIMEOUT')
