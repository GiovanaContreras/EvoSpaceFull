#-*- coding: utf-8 -*-
from operator import itemgetter

__author__ = 'mariosky'


import numpy, random, jsonrpclib, json


def current_fitness(fitness):
    return sum([fitness[k] for k in fitness])

def calc_fitness(pop):
    for ind in pop["sample"]:
        ind['currentFitness'] = int(current_fitness(ind['fitness']))
    return pop


def order_best(pop):
    return sorted(pop["sample"], key=itemgetter('currentFitness'), reverse=True)

def init_pop( populationSize, rangemin = 0 ,rangemax = 11, listSize = 66,
              evospace_URL = 'http://localhost:8088/EvoSpace'):

    server = jsonrpclib.Server(evospace_URL)
    server.initialize(None)
    for individual in range(populationSize):
        chrome = [random.randint(rangemin,rangemax) for _ in range(listSize)]
        individual = {"id":None,"fitness":{"DefaultContext":0.0 },"chromosome":chrome}
        server.put_individual(individual)


def get_sample(sample_size, evospace_URL = 'http://localhost:8088/EvoSpace'):
    server = jsonrpclib.Server(evospace_URL)
    sample =  json.loads(server.getSample(sample_size))
    return sample

def put_sample(sample_id, sample,  evospace_URL = 'http://localhost:8088/EvoSpace'):
    result =  {'sample_id':sample_id , 'sample':   sample}
    server = jsonrpclib.Server(evospace_URL)
    server.putSample(json.dumps(result))



def crossVertical(papa,mama):
    papa["chromosome"] = numpy.array(papa["chromosome"]).reshape(11,6)
    mama["chromosome"] = numpy.array(mama["chromosome"]).reshape(11,6)

    cut = random.randint(0,10)
    if cut == 0: #Si la dimension es 1
        papa_cut1 = papa["chromosome"][cut,:]
        mama_cut1 = mama["chromosome"][cut,:]
        papa_cut2 = papa["chromosome"][cut+1:,:]
        mama_cut2 = mama["chromosome"][cut+1:,:]


        child1 = numpy.vstack( ( papa_cut1[numpy.newaxis,:], mama_cut2))
        child2 = numpy.vstack( ( papa_cut2, mama_cut1[numpy.newaxis,:] ))
    else:
        papa_cut1 = papa["chromosome"][:cut,:]
        mama_cut1 = mama["chromosome"][:cut,:]
        papa_cut2 = papa["chromosome"][cut:,:]
        mama_cut2 = mama["chromosome"][cut:,:]

        child1 = numpy.vstack( ( papa_cut1, mama_cut2))
        child2 = numpy.vstack( ( papa_cut2, mama_cut1 ))
    papa["chromosome"] = papa["chromosome"].reshape(66).tolist()
    mama["chromosome"] = mama["chromosome"].reshape(66).tolist()
    child1 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child1.reshape(66).tolist(),
              'papa': papa["id"], 'mama':mama["id"] ,
              'crossover':'crossVertical:'+str(cut) }

    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2.reshape(66).tolist(),
              'papa': papa["id"], 'mama':mama["id"],
              'crossover':'crossVertical:'+str(cut) }
    return child1,child2


def crossHorizontal(papa,mama):
    papa["chromosome"] = numpy.array(papa["chromosome"]).reshape(11,6)
    mama["chromosome"] = numpy.array(mama["chromosome"]).reshape(11,6)

    cut = random.randint(0,5)

    if cut == 0: #Si la dimension es 1
        papa_cut1 = papa["chromosome"][0:11,cut]
        mama_cut1 = mama["chromosome"][0:11,cut]
        papa_cut2 = papa["chromosome"][0:11,cut+1:]
        mama_cut2 = mama["chromosome"][0:11,cut+1:]
        child1 = numpy.hstack( ( papa_cut1[:,numpy.newaxis], mama_cut2))
        child2 = numpy.hstack( ( papa_cut2, mama_cut1[:,numpy.newaxis] ))
    else:
        papa_cut1 = papa["chromosome"][0:11,0:cut]
        mama_cut1 = mama["chromosome"][0:11,0:cut]
        papa_cut2 = papa["chromosome"][0:11,cut:]
        mama_cut2 = mama["chromosome"][0:11,cut:]
        child1 = numpy.hstack( ( papa_cut1, mama_cut2))
        child2 = numpy.hstack( ( papa_cut2, mama_cut1 ))

    papa["chromosome"] = papa["chromosome"].reshape(66).tolist()
    mama["chromosome"] = mama["chromosome"].reshape(66).tolist()
    child1 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child1.reshape(66).tolist(),
              'papa': papa["id"], 'mama':mama["id"] ,
              'crossover':'crossHorizontal:'+str(cut) }

    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2.reshape(66).tolist(),
              'papa': papa["id"], 'mama':mama["id"],
              'crossover':'crossHorizontal:'+str(cut) }

    return child1,child2

def crossMirrorH(papa,mama):
    papa["chromosome"] = numpy.array(papa["chromosome"]).reshape(11,6)
    mama["chromosome"] = numpy.array(mama["chromosome"]).reshape(11,6)

    cut = random.randint(0,2)

    papa_mirror = numpy.fliplr(papa["chromosome"])
    mama_mirror = numpy.fliplr(mama["chromosome"])

    child1 = numpy.hstack( ( papa["chromosome"][:,0:5-cut],papa_mirror[:,5-cut:6] ))
    child2 = numpy.hstack( ( mama["chromosome"][:,0:5-cut],mama_mirror[:,5-cut:6] ))

    papa["chromosome"] = papa["chromosome"].reshape(66).tolist()
    mama["chromosome"] = mama["chromosome"].reshape(66).tolist()
    child1 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child1.reshape(66).tolist(),
              'papa':papa["id"],'crossover':'crossMirrorH:'+str(cut) }

    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2.reshape(66).tolist(),
              'mama':mama["id"],'crossover':'crossMirrorH:'+str(cut) }

    return child1,child2

def crossMirrorV(papa,mama):
    papa["chromosome"] = numpy.array(papa["chromosome"]).reshape(11,6)
    mama["chromosome"] = numpy.array(mama["chromosome"]).reshape(11,6)

    cut = random.randint(0,2)

    papa_mirror = numpy.flipud(papa["chromosome"])
    mama_mirror = numpy.flipud(mama["chromosome"])

    child1 = numpy.vstack( ( papa["chromosome"][0:10-cut,:],papa_mirror[10-cut:12,:] ))
    child2 = numpy.vstack( ( mama["chromosome"][0:10-cut,:],mama_mirror[10-cut:12,:] ))


    papa["chromosome"] = papa["chromosome"].reshape(66).tolist()
    mama["chromosome"] = mama["chromosome"].reshape(66).tolist()
    child1 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child1.reshape(66).tolist(),
              'papa': papa["id"], 'crossover':'crossMirrorV:'+str(cut)}

    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2.reshape(66).tolist(),
              'mama':mama["id"],'crossover':'crossMirrorV:'+str(cut)}

    return child1,child2

def reprieve(individual):
    if len(individual["fitness"]) <= 2:
        return True
    else:
        return False

def evolve(sample_size=16, evospace_URL = 'http://localhost:8088/EvoSpace' ):
    sample = get_sample(sample_size,  evospace_URL = evospace_URL)
    pop = calc_fitness(sample)
    pop["sample"].sort(key=itemgetter('currentFitness'), reverse=True)
    offspring = pop["sample"][:sample_size/2]
    out       = pop["sample"][sample_size/2:]

    #crossFunctions = [crossVertical]
    crossFunctions = [crossVertical,crossHorizontal,crossMirrorH,crossMirrorV,crossMirrorH,crossMirrorV]
    for papa, mama in zip(offspring[::2], offspring[1::2]):
        offspring.extend(random.choice(crossFunctions)(papa,mama))

    #for individual in out:
    #    if reprieve(individual):
    #        offspring.append(individual)
    print '############################'
    print len(offspring),  sample_size
    print '############################'

    for key in offspring:
        print key['fitness']
    print '############################'

    put_sample(sample["sample_id"], offspring,  evospace_URL = evospace_URL )





if __name__ == "__main__":
    init_pop(32)
    evolve()


