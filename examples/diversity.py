__author__ = 'mariosky'

DIRECTORY = '/Users/mariosky/Test/'

import numpy
from scipy.spatial.distance import pdist
diversity_file = open("diversity5.txt","w")


for i in range(50):
    file = open("{}it{}.txt".format(DIRECTORY,i))

    generation= 0
    current = []
    for line in file:
        t=line.split(" ")
        #print t
        if t[2] == 'Gen:': break
        if generation == int(t[1]):
            #Fill list
            current.append([int(e) for e in t[2:52]])
        else:
            #Process array, delete and new



            out = "{} {} {}\n".format(i,generation,sum( pdist(numpy.array(current) , 'hamming')))
            diversity_file.write(out)
            #print array.size
            del current[:]
            current.append([int(e) for e in t[2:52]])
            generation = int(t[1])
    file.close()
    print i

diversity_file.close()
        #break

