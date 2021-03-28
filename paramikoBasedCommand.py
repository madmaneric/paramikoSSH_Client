# -*- coding: utf-8 -*-
# A little work for madmaneric
import paramiko
import re
import socket
from getpass import getpass
from time import sleep
# A Function to judge is string an ip
def is_ip(ip):
    result = re.findall("^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$", ip)
    if len(result) == 0:
        return False
    else:
        return True

if __name__ == "__main__":
    #打开要刷入的命令文件
    commandFileName = input("Input the command file: ")
    try:
        localCommandFile = open(commandFileName, 'r')
        commandLines = localCommandFile.readlines()
        localCommandFile.close()
    except FileNotFoundError:
        print("The command file does Not Exist")
        print("The Process END!")
        quit()

    #打开要批量刷入命令的主机列表
    deviceListFile = input("Input your device list filename: ")
    try:
        localDeviceFileName = open(deviceListFile,'r')
        devices = localDeviceFileName.readlines()
        deviceList = []
        localDeviceFileName.close()
        for device in devices:
            if is_ip(device):
                deviceList.append(device.replace('\n', ''))
            else:
                print(device+' is not an IP and has removed')
    except FileNotFoundError:
        print("The device list file does Not Exist")
        print("The Process END!")
        quit()
    deviceUserName = input('Input the device Username:')
    devicePassword = getpass('Input the device Password:')
    try:
        logFile = open('logfile', 'a')
        deviceFailed = []
        for ip in deviceList:
            deviceSSHshell = paramiko.SSHClient()
            deviceSSHshell.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            deviceSSHshell.connect(hostname=ip, username=deviceUserName, password=devicePassword, look_for_keys=False)
            deviceShell = deviceSSHshell.invoke_shell()
            print(ip+' starting')
            for command in commandLines:
                deviceShell.send(command)
                sleep(0.5)
                output = deviceShell.recv(65535).decode('ASCII')
                print('sending ' + command)
                logFile.write(output)
    except socket.error:
        print(ip+' connection Error,check if ssh server has been enabled in device or the network')
        deviceFailed.append(ip)
    except paramiko.ssh_exception.AuthenticationException:
        print(ip + 'Login failed, Check the username and password')
        deviceFailed.append(ip)
logFile.close()
print('These HOSTS HAVE BEEN FAILED:\n')
print(deviceFailed)
print("Operations has been Done")
