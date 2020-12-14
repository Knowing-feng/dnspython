# *-* coding:utf-8 *-*
# !/usr/bin/env python3

import docker
import subprocess
import json
import shutil
import os


class DevENV(object):
    filename = './data/dev_config.json'
    client = docker.from_env()

    def write_hosts(self,*args, **kwargs):
        """写入/etc/hosts文件 更新iptables文件 添加转发规则
        :param args: 容器ID
        :param kwargs: 容器信息
        :return: 返回inspect查询到的IP
        """
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        my_c = client.inspect_container(args[0])
        ipaddress = my_c['NetworkSettings']['Networks']['bridge']['IPAddress']
        write_hosts = "sed -i '/{}/d' /etc/hosts && echo '{} {}' >> /etc/hosts".format(kwargs['site'], ipaddress,
                                                                                       kwargs['site'])  # 写入hosts文件
        subprocess.run(write_hosts, shell=True, stdout=subprocess.PIPE)

        # 添加路由转发
        rule = "-A PREROUTING -s 520201.800ug.com -p tcp -m tcp  -m comment --comment {} --dport {} -j DNAT " \
               "--to-destination {}:5202".format(kwargs['site'], kwargs['ssh_port'], ipaddress)
        subprocess.run("sed -i '/{}/d' /etc/sysconfig/iptables  && "
                       "sed -i '10a {}' /etc/sysconfig/iptables".format(kwargs['site'], rule),
                       shell=True, stdout=subprocess.PIPE)

        print("{} hosts文件 写入完成!".format(kwargs['site']))
        return ipaddress

    def get_json(self):
        """获取json数据
        :return: 格式化后的json数据
        """
        with open(self.filename) as f:
            data = json.load(f)
        return data

    def run(self, **kwargs):
        """启动容器"""
        template = "/alidata/dev_env/dev_template"  # 模板目录
        site_dir = "/alidata/dev_env/{}".format(kwargs['site'])  # 新建站点目录
        if not os.path.exists(site_dir):
            copy_dir = "cp -r " + template + ' ' + site_dir  # copy模板 作为一个新站点的目录
            subprocess.run(copy_dir, shell=True, stdout=subprocess.PIPE)

        try:
            # 创建容器
            container = self.client.containers.run("hub.fhptbet.net/ug/dev_env:latest", "/opt/run.sh",
                                                   detach=True, cpuset_cpus=kwargs['cpus'],
                                                   hostname=kwargs['site'],restart_policy={'Name': "always"},
                                                   mem_limit='8G', name=kwargs['site'],
                                                   volumes={'/alidata/dev_env/{}'.format(kwargs['site']): {
                                                       'bind': '/alidata',
                                                       'mode': 'rw'
                                                   }}, privileged=True, environment={'TEST_USER': kwargs['site']}
                                                   )

            contianerid = str(container.id)  # 获取容器ID
            kwargs['containerID'] = contianerid  # 写入容器ID

            container.exec_run("/var/backups/deploy_script.sh")  # 执行初始化环境脚本

            ip = self.write_hosts(contianerid, **kwargs)  # 写入host
            subprocess.run("systemctl restart iptables", shell=True, stdout=subprocess.PIPE)

            kwargs['ipaddress'] = ip  # 写入容器IP

            # 创建成功后提示手动创建项
            print("容器创建成功 容器ID:{}".format(contianerid))
            print("请手动在jumpserver 上新建资产, 主机IP为当前执行脚本的主机IP, SSH端口: {}".format(kwargs['ssh_port']))
            print("请在cdnbest后台 kf-test 站点中添加 目标地址:")
            print("前台地址: {}\n后台地址: {}\nPhpmyadmin地址: {}".format(kwargs['site'] + ':8080',
                                                                kwargs['site'] + ':8081',
                                                                kwargs['site'] + ':5909'))

            data = self.get_json()  # 获取json数据

            with open(self.filename, 'w') as f:
                data['SITE'][kwargs['site']] = kwargs
                data['SSH_PORT'].append(kwargs['ssh_port'])
                data['MYSQL_PORT'].append(kwargs['mysql_port'])
                data['FREE_CPU'] = data['FREE_CPU'][4:]  # 切割剩余IP且更新到json
                json.dump(data, f, indent=4)
        except docker.errors.APIError as e:
            print('容器启动失败 \n{}'.format(e))

    def show_container_list(self):
        """显示容器列表"""
        data = self.get_json()  # 获取json数据

        print("=" * 75)
        print("CPU(s):{}\tidle CPU:{}".format(data['CPUS'], len(data['FREE_CPU'])))
        print("-" * 75)
        print("env_name\tuser\t\tssh port\tmysql port\tipaddress")
        print("-" * 75)
        for detail in data['SITE'].values():
            print('{}\t\t{}\t\t{}\t\t{}\t\t{}'.format(detail['site'], detail['dev_user'], detail['ssh_port'],
                                                      detail['mysql_port'], detail['ipaddress']))
        print("=" * 75)

    def update_hosts(self):
        """批量更新hosts"""
        data = self.get_json()  # 获取json数据
        for detail in data['SITE'].values():
            ip = self.write_hosts(detail['containerID'], **detail)
            detail['ipaddress'] = ip
        else:
            subprocess.run("systemctl restart iptables", shell=True, stdout=subprocess.PIPE)
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def terminate_container(self, site, containerid, y=False):
        """zho
        :param site: 容器名称
        :param contianerid: 容器ID
        :param y: Bool类型 True为删除挂载目录 False保留挂载目录
        """
        try:
            data = self.get_json()  # 获取json数据
            container = self.client.containers.get(containerid)
            container.stop()
            print("容器已停止!")
            container.remove()
            print("容器已销毁!")
            if y:
                dev_dir = '/alidata/dev_env/{}'.format(site)
                shutil.rmtree(dev_dir)
                print(dev_dir + " 挂载目录已删除!")

            # 清空数据记录
            ide_cpu = data['SITE'][site]['cpus'].split(',')
            data['FREE_CPU'] += ide_cpu
            data['FREE_CPU'].sort(key=lambda info: int(info))
            data['SSH_PORT'].remove(data['SITE'][site]['ssh_port'])
            data['MYSQL_PORT'].remove(data['SITE'][site]['mysql_port'])
            del data['SITE'][site]

            clear_hosts_rule = "sed -i '/{site}/d' /etc/sysconfig/iptables && " \
                          "sed -i '/{site}/d' /etc/hosts".format(site=site)      # 删除hosts
            subprocess.run(clear_hosts_rule, shell=True, stdout=subprocess.PIPE)
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
        except docker.errors.NotFound as e:
            print(e)


    @staticmethod
    def show_menu():
        """显示菜单"""
        function_dict = {
            '1': '新建开发环境容器',
            '2': '显示容器列表信息',
            '3': '批量更新HOSTS文件',
            '4': '销毁开发环境容器'
        }
        exit_system = {
            '0': '退出系统'
        }
        welcome = "欢迎使用 【开发环境控制器】 v1.0"
        main_dict = {**function_dict, **exit_system}
        print()
        print()
        print("*" * 75)
        print(welcome)
        for index, value in main_dict.items():
            print('{index}. {functions}'.format(index=index, functions=value))
        print("*" * 75)
        return function_dict
