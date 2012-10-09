__author__ = 'mariosky'

from pyevolve import GSimpleGA
from pyevolve import G1DBinaryString


import jsonrpclib, sys
from EvoSpace_cherry_py_server.fitness.trap import *


EvoSpaceServer = 'http://localhost:8088/EvoSpace'

k_trap = 4

def eval_func(chromosome):
    return trap_m(chromosome,k_trap)


def init_func(ga_engine):
    server = jsonrpclib.Server('http://localhost:8088/EvoSpace')
    server.initialize(None)
    pop = ga_engine.getPopulation()
    for individual in pop:
        chrome = individual.genomeList
        individual = {'id':None,'fitness':{"DefaultContext":-1.0 },'chromosome':chrome}
        server.put_individual(individual)
    return True



def init_pop(binaryStringSize,populationSize ):
    # Genome instance
    genome = G1DBinaryString.G1DBinaryString(binaryStringSize)
    genome.evaluator.set(eval_func)
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setPopulationSize(populationSize)
    ga.stepCallback.set(init_func)
    ga.evolve()


if __name__ == "__main__":
        init_pop(int(sys.argv[1]), int(sys.argv[2]))
        k_trap = int(sys.argv[3])

