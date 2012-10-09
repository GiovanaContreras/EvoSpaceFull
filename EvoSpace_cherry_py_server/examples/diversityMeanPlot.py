__author__ = 'mariosky'


__author__ = 'mariosky'
from scipy import *
from itertools import groupby

import matplotlib.pyplot as plt


file=open('/Users/mariosky/Work/EvoSpace/examples/diversity5_WPOP.txt')

#file=open('/Users/mariosky/Work/EvoSpace/examples/diversity5.txt')
data = [map(float,l[:-1].split(' ')) for l in file if len(l) > 9]
file.close()

data.sort(key = lambda x : x[1])

mean_list = []

for k, g in groupby(data, lambda x : x[1]):
    data= [v for v in g if not v[1]%10]
#   data= [v for v in g]
    if data:
        mean_list.append( [ k, sum(data)/float(len(data)) , len(data) ]   )
    else:
        pass

a = array(mean_list)
fig, ax1 = plt.subplots()
ax1.plot(a[:,0],a[:,1]/4096,'b-')
ax1.set_xlabel('Generations', fontsize=16)
ax1.set_ylabel('Mean Diversity', color='b', fontsize=16)

for tl in ax1.get_yticklabels():
    tl.set_color('b')
ax1.ticklabel_format(style='sci', axis='y')
ax1.yaxis.major.formatter.set_powerlimits((0,4))
ax1.set_ylim([600,1100])


ax2 = ax1.twinx()
ax2.plot(a[:,0],a[:,2],'r-')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
ax2.set_ylabel('N of Mean', fontsize=16, color='r')
ax2.set_ylim([0,55])
#
#file=open('/Users/mariosky/Work/EvoSpace/examples/diversity5.txt')
#data = [map(float,l[:-1].split(' ')) for l in file if len(l) > 9]
#file.close()
#
#for k, g in groupby(data, lambda x : x[0]):
#    data= [v for v in g  ]
#    print data
#    a = array(data)
#    ax.plot(a[:,1],a[:,2]/4096,'r+')
#





plt.savefig('/Users/mariosky/Desktop/myfigXx.eps')