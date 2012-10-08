__author__ = 'mariosky'
from scipy import *
from itertools import groupby

import matplotlib.pyplot as plt


file=open('/Users/mariosky/Work/EvoSpace/examples/diversity5_WPOP.txt')
#file=open('/Users/mariosky/Work/EvoSpace/examples/diversity5.txt')
data = [map(float,l[:-1].split(' ')) for l in file if len(l) > 9]
file.close()

fig, ax = plt.subplots()
for k, g in groupby(data, lambda x : x[0]):
    data= [v for v in g if not v[1]%10 or v[1] < 10  ]
    #print data
    a = array(data)
    #print a[:,1]
    ax.plot(a[:,1]*100*64,a[:,2]/4096,'b+')

file=open('/Users/mariosky/Work/EvoSpace/examples/diversity5.txt')
data = [map(float,l[:-1].split(' ')) for l in file if len(l) > 9]
file.close()

for k, g in groupby(data, lambda x : x[0]):
    data= [v for v in g  ]
    #print data
    a = array(data)
    ax.plot(a[:,1]*4096,a[:,2]/4096,'r+')
    #print a[:,1]

ax.set_xlabel('Function Evaluations', fontsize=16)
ax.set_ylabel('Diversity', fontsize=16)
ax.ticklabel_format(style='sci', axis='y')
ax.yaxis.major.formatter.set_powerlimits((0,4))
ax.xaxis.major.formatter.set_powerlimits((0,4))
plt.savefig('/Users/mariosky/Desktop/myGX.eps')