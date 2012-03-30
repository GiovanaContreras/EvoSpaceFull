__author__ = 'mariosky'


import scipy.spatial.distance as d


## Hamming Distance de una lista de vectores binarios
data = [[1,1,1],[0,0,0],[1,1,0],[1,0,0],[0,1,0],[1,0,1]]
print sum(d.pdist(data,'hamming')*len(data[0]))


import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('172.16.51.51',username='user',password='masterkey')
(stdin, stdout, stderr) = client.exec_command('nohup python TrapWorker.py > trap.out &')

client.close();
