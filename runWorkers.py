__author__ = 'mariosky'

import paramiko

hosts =['172.16.51.50','172.16.51.51','172.16.51.52','172.16.51.53']

for host in hosts:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host,username='user',password='masterkey')
    (stdin, stdout, stderr) = client.exec_command('nohup python TrapWorker.py > trap.out &')

client.close();
