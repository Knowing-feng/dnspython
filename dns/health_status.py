#!/usr/bin/env python
# *-* coding:utf-8 *-*

import dns.resolver
import requests

ip_list = list()  # 定义域名IP列表变量
appdomain = "baidu.com"  # 定义业务域名


def get_iplist(domain=""):  # 域名解析函数，解析成功IP将追加到ip_list
    try:
        A = dns.resolver.resolve(domain, 'A')
    except Exception as e:
        print('dns resolve error: {}'.format(e))
        return False
    for i in A.response.answer:
        for j in i.items:
            ip_list.append(j.address)
    return True


def check_ip(ip):
    checkurl = 'http://' + ip
    try:
        response = requests.get(checkurl)
        if '<html>' in response.text:
            print(ip + " [OK]")
        else:
            print(ip + " [Error]")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print(ip + " [Error]")


if __name__ == '__main__':
    if get_iplist(appdomain) and len(ip_list) > 0:
        for ip in ip_list:
            check_ip(ip)
    else:
        print("dns resolver error.")
