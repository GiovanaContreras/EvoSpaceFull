__author__ = 'mariosky'
from pyevolve import GSimpleGA
from pyevolve import G1DBinaryString
from pyevolve import Mutators, Initializators
from pyevolve import Crossovers
from pyevolve import Selectors


def trap(u, a=0.75, b=1, z=3 , l=4):
    if (sum(u)  <= z ):
        return (a/z) * (z - sum(u))
    else:
        return (b/(l-z))*(sum(u)-z)

def trap_m(u,l):
     return sum([trap(m) for m in [u[i:i+l] for i in range(0,len(u),l)]])


def eval_func(chromosome):
   return trap_m(chromosome,4)



#print trap_m([0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],6)
print trap_m([0,0,0,0,  0,0,1,0, 0,0,0,0, 1,0,0,0],4)
print trap_m([1,1,1,1,  1,1,1,1, 1,1,1,1, 1,1,1,1],4)

# Genome instance
genome = G1DBinaryString.G1DBinaryString(40)
genome.evaluator.set(eval_func)
genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)
genome.setParams(bestrawscore=10.00, rounddecimal=2)
genome.crossover.set(Crossovers.G1DBinaryStringXSinglePoint)

ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GTournamentSelector)
ga.setCrossoverRate(1.0)
ga.setMutationRate(0.0)
ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

ga.setGenerations(1000)
ga.setPopulationSize(150)
ga.evolve(freq_stats=2)
print ga.bestIndividual()