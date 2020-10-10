# 1. pexpect 安装

pexpect作为Python的一个普通模块，支持pip、easy_install或源码安装方式，具体安装命令如下：

`pip install pexpect`

`easy_install pexpect`

一个简单实现SSH自动登入的实例如下:

```python
import pexpect
child = pexpect.spawn('scp foo user@example.com:.')		# spawn启动scp程序
child.expect('Password:')		# expect方法等待子程序产生的输出，判断是否匹配定义的字符串"Password:"
child.sendline(mypassword)		# 匹配后发送密码串进行验证
```

# 2. pexpect核心组件

下面介绍pexpect的几个核心组件包括spawn类、run函数、及派生类pxssh等的定义及使用方法。

## 2.1 spawn类

spawn是pexpect的主要类接口，功能是启动和控制子应用程序，以下是它的构造函数定义：

`class pexpect.spawn(command, args=[], timeout=30, maxread=2000, searchwindowsize=None, logfile=None, cwd=None, env=None, igonre_sighup=True)`

其中command参数可以是任意已知的系统命令，比如：

```python
child = pexpect.spawn('/usr/bin/ftp')		# 启动ftp客户端命令
child = pexpect.spawn('/usr/bin/ssh user@emample.com')		# 启动ssh远程连接命令
child = pexpect.spawn('ls -latr /tmp')			# 运行 ls 显示/tmp目录内容命令
```

当子程序需要参数时，还可以使用Python列表来代替参数项，如:

```python
child = pexpect.spawn('/usr/bin/ftp', [])
child = pexpect.spawn('/usr/bin/ssh', ['user@emample.com'])
child = pexpect.spawn('ls', ['-latr', '/tmp'])
```

|       参数       | 说明                                         |
| :--------------: | :------------------------------------------- |
|     timeout      | 等待结果的超时时间                           |
|     maxread      | pexpect从终端控制台一次读取的最大字节数      |
| searchwindowsize | 匹配缓冲区字符串的位置，默认是从开始位置匹配 |

**需要注意的是： pexpect不会解析shell命令当中的元字符，包括重定向 > 、管道 | 或统配符 * ，当然我们可以通过一个技巧来解决这个问题，将存在这三个特殊元字符的命令作为/bin/bash的参数进行调用，例如:** 

```python
child = pexpect.spawn('/bin/bash -c "ls -l |grep LOG > logs.txt"')
child.expect(pexpect.EOF)
```

我们可以通过将命令的参数以python列表的形式进行替换，从而使我们的语法变得更加清晰，下面的代码等价于上面的。
```python
shell_cmd = "ls -l |grep LOG > logs.txt"
child = pexpect.spawn('/bin/bash', ['-c', shell_cmd])
child.expect(pexpect.EOF)
```

有时候调试代码时，希望获取pexpect的输入与输出信息，以便了解匹配的情况。pexpect提供了两种途径，一种为写到日志文件，另一种为输出到标准输出。

写到日志的实现方法如下：

```python
child = pexpect.spawn('ssh user@emample.com')
fout = open('mylog.txt', 'wb')
child.logfile = fout
```

输出到标准输出的方法如下:

```python
child = pexpect.spawn('ssh user@emample.com')
fout = sys.stdout
child.logfile = fout
```

下面为一个完整的实例，实现远程SSH登入，登入成功后显示/home目录文件清单，并通过日志文件记录所有的输入与输出。

```python
# *-* coding:utf-8 *-*
#!/usr/bin/env python3

"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/6 下午8:27
desc: pexpect远程管理
"""

import pexpect
import sys


child = pexpect.spawn('ssh user@emample.com')
fout = open('mylog.txt', 'wb')
child.logfile = fout
child.expect("password:")
child.sendline('aa14819349+')
child.expect('#')
child.sendline('ls /home')
child.expect('#')
```

1. expect方法

   expect定义了一个子程序输出的匹配规则。

   方法定义：expect(pattern, timeout=-1, searchwindowsize=-1)

   其中，参数pattern表示字符串，pexpect.EOF(指向缓冲区尾部，无匹配项)、pexpect.TIMEOUT(匹配等待超时)、正则表达式或前面四中类型组成的列表(List)，当pattern为一个列表时，且不止一个表列元素被匹配，则返回的结果是子程序输出最先出现的那个元素，或者是列表最左边的元素(最小索引ID)，如：

   ```python
   child = pexpect.spawn('echo', ['hel1lo', 'Knowing feng'])
   print(child.expect(['hello', 'feng', 'now']))
   # 输出 : 2,即'now'被匹配, 列表的索引2对应就是'now'
   ```

   参数timeout指定等待匹配结果的超时时间，单位为秒。当超时被触发时，expect将匹配到pexpect.TIMEOUT;参数searchwindowsize为匹配缓冲区字符串的位置，默认是从开始位置匹配。

   当pexpect.EOF、pexpect.TIMEOUT作为expect的列表参数时，匹配时将返回所处列表中的索引ID

   expect方法有两个非常棒的成员: before与after。

   - **before** 保存最近匹配成功之前的内容
   - **after ** 保存最近匹配成功之后的内容

2. read相关方法

   下面这些输入方法的作用都是向子程序发送响应命令，可以理解成代替了我们的标准输入键盘。

   ```python
   send(self, s) # 发送命令,不回车
   sendline(self, s='')	# 发送命令，回车
   sendcontrol(self, char)	# 发送控制字符。如child.sendcontrol('c')等价于'ctrl + c'
   sendeof()	# 发送eof
   ```

## 2.2 run函数

run是使用pexpect进行封装的调用外部命令的函数，类似与os.system或os.popen方法，不同的是run()可以同时获得命令的输出结果及命令的退出状态，函数定义: pexpect.run(command, timeout=-1,withexitstatus=False, events=None, extra_args=None,logile=None,cwd=None,env=None)

参数command可以是系统已知的任意命令，如没有写绝对路径时将会尝试搜索命令的路径，events是一个字典，定义了expect及sendline方法的对应关系，

spawn方式的例子如下:

```python
child = pexpect.spawn('ssh user@emample.com')
fout = open('mylog.txt', 'wb')
child.logfile = fout
child.expect("password:")
child.sendline('aa14819349+')
child.expect('#')
child.sendline('ls /home')
child.expect('#')
```

使用run函数实现如下,是不是更加简洁，精炼了?

```python
child = pexpect.run('ssh user@emample.com', events={'password': 'mypassword'})
```

## 2.3 pxssh类

pxssh是pexpect的派生类，针对在ssh会话操作上再做一层封装，提供与基类更加直接的操作方法。

pxssh类定义

`class pexpect.pxssh.pxssh(timeout=30, maxread=2000, searchwindowsize=None, logfile=None, cwd=None, env=NOne)`

pxssh常用的三个方法如下:

|   方法   | 说明                                 |
| :------: | :----------------------------------- |
| login()  | 建立ssh连接                          |
| logout() | 断开连接                             |
| prompt() | 等待系统提示符，用于等待命令执行结束 |

下面使用pxssh类实现一个ssh连接远程主机并执行命令的示例。首先使用login()方法与远程主机建立连接，在通过sendline方法发送执行的命令，prompt()方法等待命令执行结束且出现系统提示符，最后使用logout()方法端口连接。

```python
from pexpect.pxssh import pxssh, ExceptionPxssh

try:
    s = pxssh()     # 创建pxssh对象s
    hostname = input('hostname: ')
    username = input('username: ')
    password = input('Please input password: ')     # 接收密码输入
    s.login(hostname, username, password)
    s.sendline('uptime')    # 运行uptime命令
    s.prompt()              # 匹配系统提示符
    print(s.before.decode())        # 打印出现系统提示符前的命令输出
    s.sendline('ls -l')
    s.prompt()
    print(s.before.decode())
    s.sendline('df -hl')
    s.prompt()
    print(s.before.decode())
    s.sendline('hostname')
    s.prompt()
    print(s.before.decode())
    s.logout()              # 断开ssh连接
except ExceptionPxssh as e:
    print('pxssh failed on login.')
    print(str(e))

```



# 3. pexpect应用示例

下面介绍两个通过pexpect实现自动化操作的示例，其中一个实现FTP协议的自动交互，另一个为SSH协议自动化操作，这些都是日常运维中经常遇到的场景。

##　3.1 实现一个自动化FTP的操作

