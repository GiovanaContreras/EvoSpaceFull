#-*- coding: utf-8 -*-
__author__ = 'mariosky'

from pyevolve import GSimpleGA
from pyevolve import G1DBinaryString
from pyevolve import Mutators
from pyevolve import Selectors
from pyevolve import Crossovers

import jsonrpclib, json,random, time, sys

from trap import *


class Worker(object):
    """
    k: Complejidad de la funcion trap

    """
    def __init__(self,sampleSize,generations,binaryStringSize,kTrap = 4,
                 returnProb = 0.1,
                 sleepProb = 0.3, sleepTime = 120,
                 crossoverRate=1.0,
                 mutationRate=0.0,
                 maxEvolutions=1000,
                 EvoSpaceURL='http://localhost:8088/EvoSpace'):
        self.sampleSize = sampleSize
        self.generations = generations
        self.maxEvolutions = maxEvolutions
        self.binaryStringSize = binaryStringSize
        self.kTrap = kTrap
        self.returnProb = returnProb
        self.sleepProb = sleepProb
        self.sleepTime = sleepTime
        self.crossoverRate = crossoverRate
        self.mutationRate = mutationRate
        self.EvoSpaceURL = EvoSpaceURL
        self.server = jsonrpclib.Server(self.EvoSpaceURL)
        self.bestRawScore = binaryStringSize/kTrap



    def eval_func(self,chromosome):
        return trap_m(chromosome,self.kTrap)


    def get_sample(self,ga_engine):
        if ga_engine.currentGeneration == 0:
            pop = ga_engine.getPopulation()
            server = jsonrpclib.Server(self.EvoSpaceURL)
            sample =  json.loads(server.getSample(self.sampleSize))
            ga_engine.sample_id = sample["sample_id"]
            for  i, individual  in enumerate(pop):
                individual.genomeList = sample["sample"][i]["chromosome"]
                individual.id = sample["sample"][i]["id"]
                individual.score = sample["sample"][i]["fitness"]["DefaultContext"]
        return False

    def put_sample(self,ga_engine):
        pop = ga_engine.getPopulation()
        sample = [ {"chromosome":individual.genomeList,"id":None,
                    "fitness":{"DefaultContext":individual.score} }
        for individual in pop]
        result =  {'sample_id':ga_engine.sample_id , 'sample':   sample}
        server = jsonrpclib.Server(self.EvoSpaceURL)
        server.putSample(json.dumps(result))

    #def termination_criteria(ga_engine):



    def evolve(self):
    # Genome instance
        genome = G1DBinaryString.G1DBinaryString(self.binaryStringSize)
        genome.evaluator.set(self.eval_func)
        genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)
        genome.setParams(bestrawscore=self.bestRawScore, rounddecimal=2)
        genome.crossover.set(Crossovers.G1DBinaryStringXSinglePoint)

        ga = GSimpleGA.GSimpleGA(genome)
        ga.selector.set(Selectors.GTournamentSelector)
        ga.setCrossoverRate(self.crossoverRate)
        ga.setMutationRate(self.mutationRate)
        ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
        ga.setGenerations(self.generations)
        ga.setPopulationSize(self.sampleSize)
        ga.stepCallback.set(self.get_sample)

        #ga.stepCallback.set(termination_criteria)

        ga.evolve(freq_stats=10000)


        if random.random() >= self.returnProb:
            if random.random() <= self.sleepProb:
                time.sleep(self.sleepTime)
            self.put_sample(ga)
            best = ga.bestIndividual()
            print best.getBinary()
            #Se busca Maximizar el score
            #Se encontro??
            return round(self.bestRawScore, 2) <= round( best.score, 2)
        else:
            print u"Not Returned"
            return False



    def run_main(self):
        for i in range(self.maxEvolutions):
            if self.server.is_active(None):
                if worker.evolve():
                    print "Global Minimum Reached"
                    break
            else:
                break

if __name__ == "__main__":
    worker = Worker(sampleSize=50,generations=100,
        binaryStringSize=40,kTrap = 4,returnProb = 0.1,sleepProb = 0.05, sleepTime = 40,
        crossoverRate=0.8,
        mutationRate=0.06,
        maxEvolutions = 1000,
        EvoSpaceURL='http://172.16.51.1:8088/EvoSpace')
    worker.run_main()
