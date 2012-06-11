#-*- coding: utf-8 -*-
from operator import itemgetter

__author__ = 'mariosky'





import numpy, random, jsonrpclib, json


evospace_URL = 'http://localhost:8088/EvoSpace'


def current_fitness(fitness):
    return sum([fitness[k] for k in fitness])

def calc_fitness(pop):
    for ind in pop["sample"]:
        ind['currentFitness'] = int(current_fitness(ind['fitness']))
    return pop


def sel_best(pop, k):
    return sorted(pop["sample"], key=itemgetter('currentFitness'), reverse=True)[:k]

def init_pop( rangemin,rangemax, listSize, populationSize ):
    server = jsonrpclib.Server(evospace_URL)
    server.initialize(None)
    for individual in range(populationSize):
        chrome = [random.randint(rangemin,rangemax) for _ in range(listSize)]
        individual = {"id":None,"fitness":{"DefaultContext":0.0 },"chromosome":chrome}
        server.put_individual(individual)
    return True

def get_sample(sample_size):
    server = jsonrpclib.Server(evospace_URL)
    sample =  json.loads(server.getSample(sample_size))
    return sample

def put_sample(sample_id, sample):
    result =  {'sample_id':sample_id , 'sample':   sample}
    server = jsonrpclib.Server(evospace_URL)
    server.putSample(json.dumps(result))


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
              'papa': papa["id"], 'mama':papa["id"] ,
              'crossover':'crossHorizontal' }

    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2.reshape(66).tolist(),
              'papa': papa["id"], 'mama':papa["id"],
              'crossover':'crossHorizontal' }

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
              'mama':papa["id"],'crossover':'crossMirrorH' }

    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2.reshape(66).tolist(),
              'mama':mama["id"],'crossover':'crossMirrorH' }

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
              'papa': papa["id"], 'crossover':'crossMirrorV'}

    child2 = {'id':None,'fitness':{"DefaultContext":0.0 },
              'chromosome':child2.reshape(66).tolist(),
              'mama':mama["id"],'crossover':'crossMirrorV'}

    return child1,child2

def evolve():
    sample = get_sample(8)
    pop = calc_fitness(sample)
    offspring = sel_best(pop,4)

    crossFunctions = [crossHorizontal,crossMirrorH,crossMirrorV]
    for papa, mama in zip(offspring[::2], offspring[1::2]):
        offspring.extend(random.choice(crossFunctions)(papa,mama))

    put_sample(sample["sample_id"], offspring)




if __name__ == "__main__":

    #init_pop(0,11, 66,32)
    evolve()


