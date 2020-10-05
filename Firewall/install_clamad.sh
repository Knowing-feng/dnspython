#!/bin/bash
yum install -y clamav clamd clamav-update         # 安装clamavp相关程序包
setenforce 0                            # 关闭SELINUX, 避免远程扫描时提示无权限的问题
ln -s /usr/sbin/clamd /etc/init.d/clamd
chkconfig --levels 235 clamd on         # 添加扫描守护进程clamd系统服务
/usr/bin/freshclam                      # 更新病毒库， 建议配置到crontab 中定时更新

sed -i 's/#TCPSocket/TCPSocket/g' /etc/clamd.d/scan.conf
# 更新守护进程监听IP配置文件，根据不同环境自行修改监听的IP，“0.0.0.0”为监听所有主机IPIP
/usr/sbin/clamd start         # 启动扫描守护进程
