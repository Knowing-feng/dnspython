# 1. 模式常用方法说明

安装: `pip  install  python-nmap`  `yum install -y nmap` or `apt-get install -y nmap`
python-nmap模块的两个常用类，一个为PortScanner()类，实现一个nmap工具的端口扫描功能封装；另一个为PortScannerHostDict()类，实现存储与访问主机的扫描结果,  

## 下面介绍PortScanner()类的一些常用方法。

- scan(self, hosts='127.0.0.1', ports=None, arguments='-sV')方法，实现指定主机、端口、nmap命令行参数的扫描。

   - **hosts** 为字符串类型，表示扫描的主机地址，格式可以用"scanme.nmap.org"、"198.116.0-255.1-127"、"216.163.128.20/20" 表示

   - **ports** 为字符串类型，表示扫描的端口，可以用"22,53,110,143-4564"来表示

   - **arguments** 为字符串类型，表示nmap命令行参数，格式为"-sU -sX -sC",例如:

     ```python
     nm = nmap.PortScanner()
     nm.scan('192.168.1.21-22','22,80')
     ```


   - **command_line(self)** 返回的扫描方法映射到具体nmap命令行，如:

     ```python
     >>> nm.command_line()
     'nmap -oX - -p 22,80 -sV 192.168.1.21-22'
     ```

   - **scaninfo(self)** 返回nmap扫描信息，格式为字典类型，如：

     ```python
     >>> nm.scaninfo()
     {'tcp': {'services': '22,80', 'method':'syn'}}
     ```

   - **all_hosts(self)** 返回nmap扫描的主机清单，格式为列表类型

## 以下介绍PortScannerHostDict()类的一些常用方法

- **hostname(self)** 返回扫描对象的主机名，如:

  ```python
  >>> nm['192.168.1.22'].hostname()
  'SN2013-08-022'
  ```

- **state(self)** 返回扫描对象的状态，包括4种状态(up、down、unkown、skipped)

- **all_protocols(self)** 返回扫描的协议，如：

  ```python
  >>> nm['192.168.1.22'].all_protocols()
  ['tcp']
  ```

- **all_tcp(self)** 返回TCP协议扫描的端口，如：
  
  ```python
  >>> nm['192.168.1.22'].all_tcp()
  [22,80]
  ```

- **tcp(self,port)方法** 返回扫描TCP协议port(端口)的信息，如:
  
  ```python
  >>> nm['192.168.1.22'].tcp(22)
  {'state': 'open', 'reason': 'syn-ack', 'name': 'ssh'}
  ```

# 实现高效的端口扫描

本次实践通过python-nmap实现一个高效的端口扫描工具，与定时作业crontab及邮件告警结合，可以很好地帮助我们及时发现异常开放的高危端口。当然，该工具也可以作为业务服务器端口的可用性探测，例如扫描192.168.1.20-25网段web服务端口80是否处于open状态。实践所采用的scan()方法的 argument参数指定为"-v -PE -p+端口",-v 表示启用细节模式，可以返回非up状态主机清单；-PE 表示采用TCP同步扫描(TCP SYN)方式；-p 指定扫描端口范围。程序输出部分采用三个for循环体，第一层遍历扫描主机，第二遍为遍历协议，第三层为遍历端口，最后输出主机状态。

**代码如下:**

```python
# *-* coding:utf-8 *-*
#!/usr/bin/env python3

"""
Author: Knowing Feng
Email: 756418710@qq.com

date: 2020/10/6 下午3:06
desc: 业务服务端口的可用性探测
"""

import sys
import nmap

scan_row = list()
input_data = input('Please input hosts and port: ')
scan_row = input_data.split(" ")
if len(scan_row) != 2:
    print("Input errors,example '192.168.1.0/24 80,443,22'")
    sys.exit(0)
hosts = scan_row[0]     # 接收用户输入的主机
port = scan_row[1]      # 接收用户输入的端口

try:
    nm = nmap.PortScanner()     # 创建端口扫描对象
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info())
    sys.exit(0)
except Exception as e:
    print("Unexpected error:", sys.exc_info()[0], e)
    sys.exit(0)

try:
    # 调用扫描方法，参数指定扫描主机hosts, nmap扫描命令行参数arguments
    nm.scan(hosts=hosts, arguments='-v -sS -p' + port)
except Exception as e:
    print("Scan error: " + str(e))

for host in nm.all_hosts(): # 遍历扫描主机
    print('-' * 50)
    print(f'Host : {host} ({nm[host].hostname()})')     # 输出主机以及主机名
    print(f'State: {nm[host].state()}')                 # 输出主机状态，如up down

    for proto in nm[host].all_protocols():      # 遍历扫描协议，如tcp，udp
        print('-' * 25)
        print(F'Protocol : {proto}')        # 输入协议名

        lport = nm[host][proto].keys()      # 获取协议的所有扫描端口
        # lport.sort()        # 端口列表排序
        for port in lport:      # 遍历端口及输出端口与状态
            print(f'port : {port}\t state : {nm[host][proto][port]["state"]}')
```

**其中主机输入支持所有表达式，如www.baidu.com、192.168.1.*、 192.168.1.1-20、 192.168.1.0/24等，端口输入输入格式也非常灵活，如80,443,22、 80,22-443。** 