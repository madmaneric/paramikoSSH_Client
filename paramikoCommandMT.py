import paramiko
import sys
import threading
import time
import os
import re


loginfo=[]

def is_ip(ip):
    result = re.findall("^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$", ip)
    if len(result) == 0:
        return False
    else:
        return True


def connect_client(ip, user, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=user, password=password, look_for_keys=False)
        sshShell =ssh.invoke_shell()
        for action in command:
            sshShell.send(action)
            time.sleep(0.1)
        ssh.close()
        print(ip + " DONE")
    except:
        print(ip+" Connection Failed")


if __name__ == "__main__":
#打开要刷入的命令文件
    command=[]
    commandFileName = input("Input the command file: ")
    if not os.path.exists(commandFileName):
        print("File Not Existed")
        exit(1)
    with open(commandFileName,'r') as commandFile:
        command=[line for line in commandFile]

    ips = []
    hostFilename = input("Input the ip file: ")
    if not os.path.exists(hostFilename):
        print("File Not Existed")
        exit(2)
    with open(hostFilename, 'r') as ipFile:
         ips = [line.strip() for line in ipFile]
    print(ips)
    for i in range(len(ips)):
        if not is_ip(ips[i]):
            print(ips[i] + " is not ip and has been removed")
            ips.pop(i)

    username=input("Username:")
    password=input("Password:")
    threads=[]
    for ip in ips:
        t = threading.Thread(target=connect_client,args=(ip,username,password,command))
        threads.append(t)
    for i in threads:
        i.start()
    print(loginfo)
    print("ALL DONE")


