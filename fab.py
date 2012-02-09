from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm


env.hosts =['172.16.51.140', '172.16.51.136', '172.16.51.137','172.16.51.135',
            '172.16.51.138', '172.16.51.139']

vm_names = ["Ubuntu","Ubuntu01","Ubuntu02","Ubuntu03","Ubuntu04","Ubuntu05"]

VMRUN= "/Applications/VMware\ Fusion.app/Contents/Library/vmrun -T fusion "
VMACHINES_PATH = "~/Documents/Virtual\ Machines.localized/"

def vm( action, gui = "" ):
    for vm_name in vm_names:
        local(VMRUN +" "+ action+" "+ VMACHINES_PATH + vm_name + ".vmwarevm/Ubuntu.vmx" + " "+gui)

def vm_list():
    local(VMRUN +"list")


vm("start","nogui")
vm_list()
#vm("stop","nogui")
run("ls")