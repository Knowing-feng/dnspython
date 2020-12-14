# *-* coding:utf-8 *-*
#!/usr/bin/env python3
"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/8 下午4:26
desc: 自动化FTP操作
"""
from __future__ import unicode_literals         # 使用unicode 编码

import pexpect
import sys

child = pexpect.spawn('ftp ftp.openbsd.org')        # 运行ftp命令
child.expect('(?i)name.*:')    # (i?)表示后面的字符串正则匹配忽略大小写
child.sendline('anonymous')     # 输入ftp账号信息
child.expect('(?i)password')    # 匹配密码输入提示
child.sendline('pexpect@sourceforge.net')   # 输入ftp密码
child.expect('ftp> ')
child.sendline('bin')       # 启用二进制传输模式
child.expect('ftp> ')
child.sendline('get robots.txt')        # 下载rebots.txt文件
child.expect('ftp> ')
sys.stdout.write(child.before)  # 输出匹配ftp> 之前的输入与输出
print("Escape character is '^]'.\n")
sys.stdout.write(child.after)
sys.stdout.flush()
# 调用interact()让出控制权,用户可以继续当前的会话手工控制子程序,默认输入"^]"字符跳出
child.interact()
child.sendline('bye')
child.close()
