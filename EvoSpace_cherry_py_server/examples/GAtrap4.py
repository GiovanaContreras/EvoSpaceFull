__author__ = 'mariosky'
from pyevolve import GSimpleGA
from pyevolve import G1DBinaryString
from pyevolve import Mutators
from pyevolve import Crossovers
from pyevolve import Selectors


RUNS = 50
POP_SIZE = 100
GENERATIONS = 40000
DIRECTORY = ''

def trap(u, a=0.75, b=1, z=3 , l=4):
    if (sum(u)  <= z ):
        return (a/z) * (z - sum(u))
    else:
        return (b/(l-z))*(sum(u)-z)

def trap_m(u,l):
     return sum([trap(m) for m in [u[i:i+l] for i in range(0,len(u),l)]])


def eval_func(chromosome):
   return trap_m(chromosome,4)

def print_pop(ga_engine):
    if not ga_engine.currentGeneration % 10:
        pop = ga_engine.getPopulation()
        for  i, individual  in enumerate(pop):
            out = "{} {} {} {}\n".format( ga_engine.iteration, ga_engine.currentGeneration,
                " ".join([str(bit) for bit in individual.genomeList ]) ,individual.score)
            ga_engine.file.write(out)
#print trap_m([0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],6)
#print trap_m([0,0,0,0,  0,0,1,0, 0,0,0,0, 1,0,0,0],4)
#print trap_m([1,1,1,1,  1,1,1,1, 1,1,1,1, 1,1,1,1],4)



def iteration(i):

    file = open('{}/it{}.txt'.format(DIRECTORY,i),'w')
    # Genome instance
    genome = G1DBinaryString.G1DBinaryString(40)
    genome.evaluator.set(eval_func)
    genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)
    genome.setParams(bestrawscore=10.00, rounddecimal=2)
    genome.crossover.set(Crossovers.G1DBinaryStringXSinglePoint)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.file = file
    ga.iteration = i
    ga.selector.set(Selectors.GTournamentSelector)
    ga.setCrossoverRate(0.5)
    ga.setMutationRate(0.06)

    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
    ga.setGenerations(GENERATIONS)
    ga.setPopulationSize(POP_SIZE)
    ga.stepCallback.set(print_pop)
    ga.evolve(freq_stats=0)
    best = ga.bestIndividual( )
    out ="{} Gen: {}\n".format(round( best.score, 2),ga.currentGeneration)
    file.write(out)
    file.close()
    print out



for i in range(RUNS):
    iteration(i)

