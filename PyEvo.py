from pyevolve import GSimpleGA
from pyevolve import G1DList
from pyevolve import Mutators, Initializators
from pyevolve import Selectors
from pyevolve import Consts


from EvoSpace import Population
import jsonrpclib, json

import math

# This is the Rastrigin Function, a deception function
def rastrigin(genome):
   n = len(genome)
   total = 0
   for i in xrange(n):
      total += genome[i]**2 - 10*math.cos(2*math.pi*genome[i])
   return (10*n) + total

def init_func(ga_engine):
        population = Population("pop")
        pop = ga_engine.getPopulation()
        population.initialize(pop.popSize)
        for individual in pop:
            chrome = individual.genomeList
            key = population.individual_next_key()
            population.put_individual(key, fitness={"DefaultContext":individual.fitness }, chromosome  = chrome )
        return True



def init_pop():
   # Genome instance
   genome = G1DList.G1DList(20)
   genome.setParams(rangemin=-5.2, rangemax=5.30, bestrawscore=0.00, rounddecimal=2)
   genome.initializator.set(Initializators.G1DListInitializatorReal)
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

   genome.evaluator.set(rastrigin)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setPopulationSize(1000)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.stepCallback.set(init_func)
   ga.evolve(freq_stats=50)



def get_sample(ga_engine):
        if ga_engine.currentGeneration == 0:
            pop = ga_engine.getPopulation()
            server = jsonrpclib.Server('http://localhost:8088/EvoSpace')
            sample =  json.loads(server.getSample(pop.popSize))
            ga_engine.sample_id = sample["sample_id"]
            for  i, individual  in enumerate(pop):
                individual.genomeList = sample["sample"][i]["chromosome"]
                individual.id = sample["sample"][i]["id"]
                individual.fitness = sample["sample"][i]["fitness"]["DefaultContext"]
        return False

def put_sample(ga_engine):
            pop = ga_engine.getPopulation()

            #server = jsonrpclib.Server('http://localhost:8088/EvoSpace')
            #sample =  json.loads(server.getSample(pop.popSize))

            sample = [ {"chromosome":individual.genomeList,"id":None,"fitness":{"DefaultContext":individual.fitness} }
                        for individual in pop]
            result =  {'sample_id':ga_engine.sample_id ,
                   'sample':   sample}
            print json.dumps(result)

            server = jsonrpclib.Server('http://localhost:8088/EvoSpace')
            server.putSample(json.dumps(result))

def run_main():
   # Genome instance
   genome = G1DList.G1DList(20)
   genome.setParams(rangemin=-5.2, rangemax=5.30, bestrawscore=0.00, rounddecimal=2)
   genome.initializator.set(Initializators.G1DListInitializatorReal)
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

   genome.evaluator.set(rastrigin)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
   ga.setMinimax(Consts.minimaxType["minimize"])

   ga.setGenerations(3000)
   ga.setCrossoverRate(0.8)
   ga.setPopulationSize(100)
   ga.setMutationRate(0.06)

   ga.stepCallback.set(get_sample)
   ga.evolve(freq_stats=100)
   print ga.sample_id
   best = ga.bestIndividual()
   put_sample(ga)

if __name__ == "__main__":
    init_pop()
    for i in range(100): 
        run_main()

  