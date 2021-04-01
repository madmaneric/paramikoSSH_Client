# paramikoSSH_Client
基于paramiko端批量刷入设备命令<br>
建议使用python 3.6或3.8版本<br>
需要通过pip3 安装paramiko库<br>
centos下环境初始化<br>
依次输入以下命令<br>
yum upgrade<br>
yum install python36 -y<br>
pip3 install pip --upgrade<br>
pip3 install paramiko<br>

将python脚本复制或上传至centos并运行即可<br>

后期目标<br>
1 Windows环境下getpass函数调用失败修正<br>
2 ssh连接失败的异常捕捉不完善，程序会异常退出<br>
3 识别设备的出错反馈，每条命令识别执行成功后再执行下一条，若出错则不继续执行，直接略过设备<br>
4 添加尝试多用户名登录设备，若一个失败则尝试另外一个用户名登录。<br>
5 添加多线程执行，多台设备同步执行<br>
6 命令检测工具，若为保存的命令则多sleep 2秒，并检查配置文件的保存日期是否为近期执行，确保配置保存成功<br>
