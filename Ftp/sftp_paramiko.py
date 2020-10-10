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