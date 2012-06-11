#-*- coding: utf-8 -*-
__author__ = 'mariosky'

from pyevolve import GSimpleGA
from pyevolve import G1DBinaryString
from pyevolve import Mutators
from pyevolve import Selectors
from pyevolve import Crossovers

import jsonrpclib, json,random, time, sys

from fitness.trap import *


class Worker(object):
    """
    k: Complejidad de la funcion trap

    """
    def __init__(self,sample_size,generations_per_worker,binary_string_size,worker_id="1",k_trap = 4,
                 no_return_prob = 0.0,
                 sleep_prob = 0.0, sleep_time = 2,
                 crossover_rate=1.0,
                 mutation_rate=0.0,
                 max_evolutions=1000,
                 evospace_URL='http://localhost:8088/EvoSpace',run_number=0):
        self.sample_size = sample_size
        self.generations = generations_per_worker
        self.max_evolutions = max_evolutions
        self.binary_string_size = binary_string_size
        self.k_trap = k_trap
        self.no_return_prob = no_return_prob
        self.sleep_prob = sleep_prob
        self.sleep_time = sleep_time
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.evospace_URL = evospace_URL
        self.server = jsonrpclib.Server(self.evospace_URL)
        self.best_raw_score = 20 #binary_string_size/k_trap
        self.worker_id = worker_id
        self.sample_id = 0
        self.run_num = run_number


    def eval_func(self,chromosome):
        return trap_m(chromosome,self.k_trap)


    def get_sample(self,ga_engine):
        if ga_engine.currentGeneration == 0:
            pop = ga_engine.getPopulation()
            server = jsonrpclib.Server(self.evospace_URL)
            sample =  json.loads(server.getSample(self.sample_size))
            ga_engine.sample_id = sample["sample_id"]
            #print ga_engine.sample_id
            #self.sample_id = sample["sample_id"]
            for  i, individual  in enumerate(pop):
                individual.genomeList = sample["sample"][i]["chromosome"]
                individual.id = sample["sample"][i]["id"]
                individual.score = sample["sample"][i]["fitness"]["DefaultContext"]
        else:
            pop = ga_engine.getPopulation()
            stats = pop.getStatistics()
            print self.run_num,self.worker_id,ga_engine.sample_id, ga_engine.currentGeneration,stats["rawMax"], stats["rawMin"], stats["rawAve"]
        return False

    def put_sample(self,ga_engine):
        pop = ga_engine.getPopulation()
        sample = [ {"chromosome":individual.genomeList,"id":None,
                    "fitness":{"DefaultContext":individual.score} }
        for individual in pop]
        result =  {'sample_id':ga_engine.sample_id , 'sample':   sample}
        server = jsonrpclib.Server(self.evospace_URL)
        server.putSample(json.dumps(result))

    #def termination_criteria(ga_engine):



    def evolve(self):
    # Genome instance
        genome = G1DBinaryString.G1DBinaryString(self.binary_string_size)
        genome.evaluator.set(self.eval_func)
        genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)
        genome.setParams(bestrawscore=self.best_raw_score, rounddecimal=2)
        genome.crossover.set(Crossovers.G1DBinaryStringXSinglePoint)

        ga = GSimpleGA.GSimpleGA(genome)
        ga.selector.set(Selectors.GTournamentSelector)
        ga.setCrossoverRate(self.crossover_rate)
        ga.setMutationRate(self.mutation_rate)
        ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
        ga.setGenerations(self.generations)
        ga.setPopulationSize(self.sample_size)
        ga.stepCallback.set(self.get_sample)

        #ga.stepCallback.set(termination_criteria)

        ga.evolve(freq_stats=0)


        if random.random() >= self.no_return_prob:
            if random.random() <= self.sleep_prob:
                print self.worker_id+"- sleeping"
                time.sleep(self.sleep_time)
            self.put_sample(ga)
            best = ga.bestIndividual()
            #print self.worker_id+"-"+str(best.score)
            #print best.getBinary()
            #Se busca Maximizar el score
            #Se encontro??
            return round(self.best_raw_score, 2) <= round( best.score, 2)
        else:
            print self.worker_id+"(Not Returned)"
            return False



    def run_main(self):
        for i in range(self.max_evolutions):
            time.sleep(3)
            #if self.server.is_active(None):
            if worker.evolve():
                #print "Global Minimum Reached"
                exit()
            #else:
            #    break

if __name__ == "__main__":
    worker = Worker(
        run_number=int(sys.argv[1]),
        worker_id=sys.argv[2],
        sample_size=int(sys.argv[3]),
        generations_per_worker=int(sys.argv[4]),
        binary_string_size=int(sys.argv[5]),
        k_trap= int(sys.argv[6]),
        no_return_prob= 0.0,
        sleep_prob= 0.0,
        sleep_time= 2,
        crossover_rate=0.5,
        mutation_rate=0.06,
        max_evolutions= 1000,
        evospace_URL='http://127.0.0.1:8088/EvoSpace',

        )

    worker.run_main()
