# -*- coding: utf-8 -*-
"""
Задание 18.2

Создать функцию send_config_commands

Функция подключается по SSH (с помощью netmiko) к ОДНОМУ устройству и выполняет перечень команд в конфигурационном режиме на основании переданных аргументов.

Параметры функции:
* device - словарь с параметрами подключения к устройству
* config_commands - список команд, которые надо выполнить

Функция возвращает строку с результатами выполнения команды:

In [7]: r1
Out[7]:
{'device_type': 'cisco_ios',
 'ip': '192.168.100.1',
 'username': 'cisco',
 'password': 'cisco',
 'secret': 'cisco'}

In [8]: commands
Out[8]: ['logging 10.255.255.1', 'logging buffered 20010', 'no logging console']

In [9]: result = send_config_commands(r1, commands)

In [10]: result
Out[10]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#logging 10.255.255.1\nR1(config)#logging buffered 20010\nR1(config)#no logging console\nR1(config)#end\nR1#'

In [11]: print(result)
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.255.255.1
R1(config)#logging buffered 20010
R1(config)#no logging console
R1(config)#end
R1#


Скрипт должен отправлять команду command на все устройства из файла devices.yaml с помощью функции send_config_commands.
"""

import yaml

from netmiko import (
ConnectHandler,
NetmikoTimeoutException,
NetmikoAuthenticationException
)

commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]

test_commands = [
        "interface Loopback 100",
        "ip address 10.1.1.100 255.255.255.255",
    ]

def send_config_commands(device, config_commands):
#    result = send_config_set(config_commands)
    result = ''
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            output = ssh.send_config_set(config_commands)
            result = output
        return result
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    r1 = devices[0]
    print(r1)
    print(commands)
    res = send_config_commands(r1, test_commands)
    print(res)
#    for dev in devices:
#        print(dev)
#        print(send_config_commands(dev, commands))
