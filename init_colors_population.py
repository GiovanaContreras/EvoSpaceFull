__author__ = 'mariosky'

from pyevolve import GSimpleGA
from pyevolve import G1DList


import jsonrpclib, sys



EvoSpaceServer = 'http://localhost:8088/EvoSpace'


def eval_func(chromosome):
    return 5


def init_func(ga_engine):
    server = jsonrpclib.Server('http://localhost:8088/EvoSpace')
    server.initialize(None)
    pop = ga_engine.getPopulation()
    for individual in pop:
        chrome = individual.genomeList
        individual = {'id':None,'fitness':{"DefaultContext":-1.0 },'chromosome':chrome}
        server.put_individual(individual)
    return True



def init_pop(colors,populationSize ):
    # Genome instance
    genome = G1DList.G1DList(colors);
    #genome = G1DBinaryString.G1DBinaryString(binaryStringSize)
    genome.setParams(rangemin=0, rangemax=11, gauss_mu=4, gauss_sigma=6)
    genome.evaluator.set(eval_func)
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setPopulationSize(populationSize)
    ga.stepCallback.set(init_func)
    ga.evolve()


if __name__ == "__main__":
        init_pop(int(sys.argv[1]), int(sys.argv[2]))


