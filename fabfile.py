from __future__ import with_statement
from fabric.api import *



env.hosts =['172.16.51.50','172.16.51.51','172.16.51.52','172.16.51.53']
env.user = 'user'
env.password = 'masterkey'

vm_names = ["Ubuntu","Ubuntu00","Ubuntu01","Ubuntu02"]

VMRUN= "/Applications/VMware\ Fusion.app/Contents/Library/vmrun -T fusion "
VMACHINES_PATH = "~/Documents/Virtual\ Machines.localized/"

def vm( action, gui = "" ):
    for vm_name in vm_names:
        local(VMRUN +" "+ action+" "+ VMACHINES_PATH + vm_name + ".vmwarevm/Ubuntu.vmx" + " "+gui)

def vm_list():
    local(VMRUN +"list")



#vm("start","nogui")
@parallel
def setupWorkers():
    #vm("stop","nogui")
    put('examples/TrapWorker.py')
    put('examples/trap.py')
    # Mejor con panamiko aunque sin nice output
    #out = run('nohup python TrapWorker.py > trap.out &')

    #print out

def setupMachines():
    vm("start")
    vm_list()


def setupServers():
    local('redis-server')
    local('python cherryserver.py')


