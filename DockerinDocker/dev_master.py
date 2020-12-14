# *-* coding:utf-8 *-*
# !/usr/bin/env python3
import json
import random
from dev_tools import DevENV


instance = DevENV()


while True:
    with open('./data/dev_config.json') as f:
        data = json.load(f)
    function_dict = DevENV.show_menu()
    action_str = input("请选择操作功能: ")
    print("您选择的操作是 【{}】".format(action_str))

    if action_str in function_dict:
        if action_str == '1':
            # 新建开发环境站点
            site_str = input("请分配开发编号: ")
            while isinstance(data['SITE'].get(site_str), dict):
                site_str = input('已存在的编号,请重新输入: ')

            dev_name = input("请输入开发人员昵称: ")
            ssh_port = random.randint(10000, 65535)
            mysql_port = random.randint(10000, 65535)
            cpus = data['FREE_CPU'][:4]
            cpus = ','.join(cpus)
            while ssh_port in data['SSH_PORT']:
                ssh_port = random.randint(10000, 65535)
            while mysql_port in data['MYSQL_PORT']:
                mysql_port = random.randint(10000, 65535)

            instance.run(cpus=cpus, ssh_port=ssh_port, mysql_port=mysql_port,
                         site=site_str, dev_user=dev_name)
        elif action_str == '2':
            instance.show_container_list()
        elif action_str == '3':
            # 批量更新表结构设置
            instance.update_hosts()
        elif action_str == '4':
            # 销毁开发环境容器
            container_name = input("请输入容器名称: ")
            try:
                container_id = data['SITE'][container_name]['containerID']
            except KeyError:
                print("容器不存在!")
                continue
            while True:
                delete_bool = input("是否将挂载目录/alidata/dev_env/{}一并删除?  [yes]/[no] ").lower()
                if delete_bool == 'yes':
                    delete_bool = True
                    break
                elif delete_bool == 'no':
                    delete_bool = False
                    break
                else:
                    print("输入错误请重新输入")
            instance.terminate_container(container_name, container_id, delete_bool)
    elif action_str == '0':
        break
    else:
        print("您输入的不正确，请重新选择")
