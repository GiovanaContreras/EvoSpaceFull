__author__ = 'mariosky'

best = []
for i in range(32):
    file = open('/Users/mariosky/Google Drive/Evospace Data/k4w32s32-1336976815/k4w32s32.worker{}.txt'.format(i))
    data = [ line.split(' ') for line in file if len(line.split(' ')) == 7 and len(line.split(' ')[6]) > 2 ]
    best.extend([ (  int(line[0]),line[1],line[2],line[4])  for line in data if float(line[4]) == 10.0])
best.sort()
for l in best:
    print l
