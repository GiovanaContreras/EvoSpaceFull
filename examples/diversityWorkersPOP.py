__author__ = 'mariosky'
__author__ = 'mariosky'

DIRECTORY = '/Users/mariosky/Google Drive/Evospace Data/k5w4s64-1337015871/'

import numpy
from scipy.spatial.distance import pdist
diversity_file = open("diversity5_WPOP.txt","w")

pop_file = open("{}k5w4s64.pops.txt".format(DIRECTORY))


generation= 10
counter = 0
current = []

for line in pop_file:
    t=line.split(" ")
    if len(t) < 4:
        print "short", t
        continue

    if generation == int(t[1]):
        #Fill list
        current.append([int(e) for e in t[2]])
    else:
        #Process array, delete and new
        print
        out = "{} {} {}\n".format(t[0],generation,sum( pdist(numpy.array(current) , 'hamming')))
        diversity_file.write(out)
        print out
        del current[:]
        current.append([int(e) for e in t[2]])
        generation = int(t[1])

pop_file.close()

diversity_file.close()
#break

