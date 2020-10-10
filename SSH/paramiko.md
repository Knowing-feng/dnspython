# 1. paramiko 的安装

pexpect支持pip、easy_install或源码安装方式，具体安装命令如下：

`pip install pexpect`

`easy_install pexpect`

下面介绍一个简单实现远程SSH运行命令的示例。该示例使用密码认证方式，通过exec_command()方法执行命令，源码如下:

```python
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

hostname = '192.168.1.21'
username = 'root'
password = '123456789'

paramiko.util.log_to_file('syslogin.log')       # 发送 paramiko 日志到 syslogin.log文件
ssh = paramiko.SSHClient()      # 创建一个ssh客户端client对象
ssh.load_system_host_keys()     # 获取客户端 host_keys，默认 ~/.ssh/known_hosts, 非默认路径需指定
ssh.connect(hostname=hostname, username=username, password=password)        # 创建ssh连接
stdin, stdout, stderr = ssh.exec_command('ifconfig')     # 调用远程执行命令方法exec_command()
print(stdout.read().decode())        # 打印命令执行结果，得到Python列表形式，可以使用stdout.readlines()

time.sleep(5)       # 结果缓冲释放过快未读完会报错，加sleep
ssh.close()     # 关闭连接
```

# 2. paramiko 的核心组件

paramiko包含两个核心组件，一个为SSHClient类，另一个为SFTPClient类，下面详细介绍。

## 2.1 SSHClient类
SSHClient类是SSH服务会话的高级表示，该类封装了传输(transport)、通道(channel)及SFTPClient的校验、建立的方法，通常用于执行远程命令，下面是一个简单的例子:

```python
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname=hostname, username=username, password=password)
stdin, stdout, stderr = ssh.exec_command('ifconfig') 
```

下面介绍SSHClient常用的几个方法。

**1. connect方法**

   connect方法实现了远程SSH连接并校验。

   方法定义：

   `connect(self, hostname, port=22, username=None, password=None, pkey=None, key_filename=None, timeout=None, allow_agent=True, look_for_keys=True, compress=False)`

   

|              参数              | 说明                                         |
| :----------------------------: | :------------------------------------------- |
|       hostname(str类型)        | 连接的目标主机地址                           |
|         port(int类型)          | 连接目标主机的端口，默认为22                 |
|       username(str类型)        | 校验的用户名(默认为当前的本地用户名)         |
|       password(str类型)        | 密码用与身份校验或解锁私钥                   |
|         pkey(Pkey类型)         | 私钥方式用于身份验证                         |
| key_filename(str or list 类型) | 一个文件名或文件名的列表，用于私钥的身份验证 |
|       timeout(float类型)       | 一个可选的超时时间(以秒为单位)的TCP连接      |
|     allow_agent(bool类型)      | 设置为False时用于禁用连接到SSH代理           |
|    look_for_keys(bool类型)     | 设置为False时用来禁用在~/.ssh中搜索秘钥文件  |
|       compress(bool类型)       | 设置为True时打开压缩                         |

**2. exec_command方法**

   远程命令执行方法，该命令的输入与输出流为标准输入(stdin)、输出(stdout)、错误(stderr)的Python文件对象，方法定义:

   `exec_command(self, command, bufsize=-1)`

   

|       参数       | 说明                             |
| :--------------: | :------------------------------- |
| command(str类型) | 执行的命令串                     |
| bufsize(int类型) | 文件缓冲区大小，默认为-1(不限制) |

**3. load_system_host_keys方法**

加载本地公钥校验文件，默认为 ～/.ssh/know_hosts,非默认路径需要手工指定，方法定义:

`load_system_host_keys(self, filename=None)`

参数说明:

filename(str类型)，指定远程主机公钥记录文件。

**4. set_missing_host_key_policy方法**

设置连接的远程主机没有本地主机秘钥或HostKeys对象时的策略，目前支持三种，分别是AutoAddPolicy、RejectPolicy(默认)、WarningPolicy，仅限用于SSHClient类。

分别代表的含义如下:

|     参数      | 说明                                                         |
| :-----------: | :----------------------------------------------------------- |
| AutoAddPolicy | 自动添加主机名及主机密钥到本地HostKeys对象，并将其保存，不依赖load_system_host_keys()的配置，即使~/.ssh/know_hosts不存在也不产生影响 |
| RejectPolicy  | 自动拒绝位置的主机名和密钥，以来load_system_host_keys的配置  |
| WarningPolicy | 用于记录一个位置的主机密钥的Python警告，并接受它，功能上与AutoAddPolicy相似，但位置主机会有告警 |

使用方法如下:

```python
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
```

## 2.2 SFTPClient类

SFTPClient作为一个SFTP客户端对象，根据SSH传输协议的sftp会话，实现远程文件操作，比如文件上传、下载、状态等操作，下面介绍SFTPClient类的常用方法。

### 1. from_transport方法

创建一个已连通的SFTP客户端通道，方法定义:

`from_transport(cls, t)`

参数说明:

**t(Transport)**,一个已通过验证的传输对象

例子说明:

```python
t = paramiko.Transport(("192.168.1.22", 22))
t.connect(username="root", password="123456")
sftp = paramiko.SFTPClient.from_transport(t)
```

### 2. put方法

上传本地文件到远程SFTP服务端，方法定义：

`put(self, localpath, remotepath, callback=None, confirm=True)`

|            参数             | 说明                                                         |
| :-------------------------: | :----------------------------------------------------------- |
|          localpath          | 需上传的本地文件 (源)                                        |
|         remotepath          | 远程路径(目标)                                               |
| callback(function(int,int)) | 获取已接受的字节数及总传输字节数，以便回调函数调用，默认为None |
|      confirm(bool类型)      | 文件上传完毕后是否调用stat()方法，以便确认文件的大小         |

```python
localpath = '/home/tmp.text'
remotepath= '/tmp/tmp.text'     # 目标路径不能只填写目录，需要具体化
put = sftp.put(localpath, remotepath)
```

### 3. get方法

从远程SFTP服务端下载文件到本地，方法定义:

`get(self, remotepath, localpath, callback=None)`

|            参数             | 说明                                                         |
| :-------------------------: | :----------------------------------------------------------- |
|         remotepath          | 需上传的yuancheng 文件 (源)                                  |
|          localpath          | 本地路径(目标)                                               |
| callback(function(int,int)) | 获取已接受的字节数及总传输字节数，以便回调函数调用，默认为None |

例子说明:

```python
localpath = '/home/tmp.text'
remotepath= '/tmp/tmp.text'     # 目标路径不能只填写目录，需要具体化
get = sftp.get(remotepath, localpath)
```

### 4. 其他方法

SFTPClient类其他常用方法说明:

|  参数   | 说明                                                         |
| :-----: | :----------------------------------------------------------- |
|  Mkdir  | 在SFTP服务器端创建目录，如sftp.mkdir("/home/userdir", 0755)  |
| remove  | 删除在SFTP服务器端指定目录，如sftp.remove("/home/userdir")   |
| rename  | 重命名SFTP服务器端文件或目录，如sftp.rename("/home/test.sh", "/home/testfile.sh") |
|  stat   | 远程获取SFTP服务端指定文件信息，如sftp.stat("/home/testfile.sh") |
| listdir | 获取远程SFTP服务器端指定目录列表，以Python的列表(List)形式返回，如sftp.listdir("/") **返回结果:**['boot', 'dev', 'home', 'proc', 'run', 'sys', 'etc', 'root', 'var', 'tmp', 'usr', 'bin', 'sbin', 'lib', 'lib64', 'media', 'mnt', 'opt', 'srv', '.readahead', 'alidata', 'log', 'data'] |

### 5. SFTPClient类应用示例

下面为SFTPClient类的以一个完整示例，实现了文件上传、下载、创建与删除目录等，需要注意的是，put和get方法需要指定文件名，不能省略。

代码如下:

```python
# *-* coding:utf-8 *-*
# !/usr/bin/env python3

"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/9 下午8:37
desc: 基于paramiko 的 SFTP功能，仅用于单个文件
"""

import paramiko


class ParamikoSFTP(object):
    def __init__(self, host, username, password, port=22):
        """
        初始化服务器信息
        :param host: 远程地址
        :param username: 用户名
        :param password: 密码
        :param port: 端口,默认22
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def sftp_connect(self):
        """建立sftp远程连接"""
        try:
            t = paramiko.Transport((self.host, self.port))
            t.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(t)
            return self.sftp
        except Exception as e:
            print(f'STP Connect Error: {str(e)}')
            return e

    def sftp_close(self):
        """关闭sftp连接"""
        self.sftp.close()

    def get(self, remotepath, localpath):
        """从远程目标下载文件到本地"""
        try:
            get = self.sftp.get(remotepath, localpath)
        except Exception as e:
            print(f'Get Error: {str(e)}')

    def put(self, localpath, remotepath):
        """本地文件上传至远程目录"""
        try:
            put = self.sftp.put(localpath, remotepath)
        except Exception as e:
            print(f'Put Error: {str(e)}')

    def mkdir(self, remotedir, mode=0o755):
        """在sftp目标创建目录"""
        try:
            mkdir = self.sftp.mkdir(remotedir, mode)
        except Exception as e:
            print(f'Mkdir Error: {str(e)}')

    def rmdir(self, remotedir):
        """删除sftp目标的目录"""
        try:
            rmdir = self.sftp.rmdir(remotedir)
        except Exception as e:
            print(f'Rmdir Error: {str(e)}')

    def rename(self, old_name, new_name):
        """重命名sftp服务端文件或目录"""
        try:
            rename = self.sftp.rename(old_name, new_name)
        except Exception as e:
            print(f'Rename Error: {str(e)}')
```



# 3. paramiko应用示例

## 3.1 实现密钥方式登入远程主机

实现自动密钥登入方式，第一步需要配置与目标设备的密钥认证支持，私钥文件可以存放在默认路径"~/.ssh/id_rsa",当然也可以自定义，如本示例的"/home/key/id_rsa",通过paramiko.RSAK.from_private_key_file()方法引用

代码如下:

```python
# *-* coding:utf-8 *-*
#!/usr/bin/env python3

"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/9 下午4:16
desc: 基于秘钥使用paramiko远程连接
"""

import paramiko
import time
import os

hostname = '192.168.1.21'
username = 'root'

paramiko.util.log_to_file('syslogin.log')       # 发送 paramiko 日志到 syslogin.log文件
ssh = paramiko.SSHClient()      # 创建一个ssh客户端client对象
ssh.load_system_host_keys()     # 获取客户端 host_keys，默认 ~/.ssh/known_hosts, 非默认路径需指定
privatekey = os.path.expanduser("/home/key/id_rsa")     # 定义私钥存放路径
key = paramiko.RSAKey.from_private_key_file(privatekey)     # 创建私钥对象key
ssh.connect(hostname=hostname, username=username, pkey=key, timeout=5)        # 创建ssh连接
stdin, stdout, stderr = ssh.exec_command('ifconfig')     # 调用远程执行命令方法exec_command()
print(stdout.read().decode())        # 打印命令执行结果，得到Python列表形式，可以使用stdout.readlines()

time.sleep(5)       # 结果缓冲释放过快未读完会报错，加sleep
ssh.close()     # 关闭连接

```

## 3.2 实现堡垒机模式下的远程命令执行

堡垒机环境在一定成都上提升了运营安全级别，但同时也提高了日常运营成本，作为管理的中转设备，任何针对业务服务器的管理请求都会经过此节点，比如SSH协议，首先运维人员在办公电脑通过SSH协议登入堡垒机，再通过堡垒机SSH跳转到所有的业务服务器进行维护操作。

我们可以利用paramiko的invoke_shell机制来实现通过堡垒机实现服务器操作，原理是SSHClient.connect到堡垒机后开启一个新的SSH会话(session)，通过新的会话 运行"ssh user@IP" 去实现远程执行命令的操作。

代码如下:

```python
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
```

## 3.2 实现堡垒机模式下的远程文件上传

实现堡垒机模式下的文件上传，原理是通过paramiko的SFTPClient将文件从办公设备上传至堡垒机的临时目录，如/tmp，再通过SSHClient的invoke_shell方法开启ssh会话，执行scp命令，将/tmp下的指定文件复制到目标业务服务器上。

本示例具体使用sftp.put() 方法上传文件至堡垒机临时目录，再通过send()方法执行scp命令，将堡垒机临时目录下的文件复制到目标主机

代码如下:

```python
# *-* coding:utf-8 *-*
#!/usr/bin/env python3

"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/10 下午2:19
desc: 实现堡垒机模式下的远程文件上传
"""

import paramiko
import sys

blip = '192.168.1.23'       # 定义跳板机IP
bluser = 'root'
blpasswd = 'mypassword'

hostname = '192.168.1.1'        # 定义业务服务器信息
username = 'root'
password = 'mypassword'

tmp_dir = '/tmp'
remotedir = '/data'
localpath = '/home/nginx_access.tar.gz'     # 本地源文件路径
tmppath = tmp_dir + '/nginx_access.tar.gz'      # 堡垒机临时路径
remotepath = remotedir + '/nginx_access_hd.tar.gz'      # 业务主机目标路径

port = 22
passinfo = "'s password:"       # 输入服务器密码的前标志串
t = paramiko.Transport((blip, port))
t.connect(username=blip, password=blpasswd)
sftp = paramiko.SFTPClient.from_transport(t)
sftp.put(localpath, tmppath)        # 上传本地源文件到堡垒机临时路径
sftp.close()

ssh = paramiko.SSHClient()      # 创建会话，开启命令调用
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect(blip, port, bluser, blpasswd)

channel = ssh.invoke_shell()    # 创建会话，开启命令调用
channel.settimeout(10)          # 会话命令执行超时时间，单位为秒

buff = ''
resp = ''
# scp 中转目录文件到目标主机
channel.send(f'scp {tmppath} {username}@{hostname}:{remotepath} \n')
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
    
print(buff)     # 打印输出串
channel.close
ssh.close()
```

**当然，整合以上两个示例，再引入主机清单及功能配置文件，可以实现更加灵活、强大的功能，大家可以主机动手，在实践中学习，打造适合自身业务环境的自动化运营平台**