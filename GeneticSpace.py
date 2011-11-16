__author__ = 'mario'

HOST = '127.0.0.1'
PORT = 6379
DB = 0
SERVER_LIST = ['protoboard.com/population']

import redis, time , json, random

r = redis.Redis(host=HOST, port=PORT, db=DB)

class Individual:
    def __init__(self, key = None , fitness = {}  , chromosome  = None , from_dict = None):
        ## Debe de existir o Key o from_dict
        if from_dict:
            self.key = from_dict['id']
            self.fitness = from_dict['fitness']
            self.chromosome = from_dict['chromosome']
        else:
            self.key = key
            self.fitness = fitness
            self.chromosome = chromosome

    def put(self, population= 'population'):
        pipe = r.pipeline()
        if pipe.sadd( population, self.key ):
            pipe.hset( self.key ,'fitness' , self.fitness )
            pipe.hset( self.key ,'chromosome', self.chromosome)
            pipe.execute()
            return True
        else:
            return False

        
    def get(self, as_dict = False):
        if r.exists( self.key ):
            self.fitness =  eval(r.hget(self.key ,'fitness'))
            self.chromosome = eval (r.hget( self.key ,'chromosome'))
        if as_dict:
            return {'id':self.key,'fitness':self.fitness,'chromosome':self.chromosome}
        else:
            return self


    def __repr__(self):
        return self.key +":"+ str(self.fitness) +":" + str( self.chromosome)

    def as_dict(self):
        return {'id':self.key , 'fitness':self.fitness ,'chromosome':self.chromosome}


class Population:
    def __init__(self, initial_size = 10000, flush = True ):
        self.initial_size = initial_size
        self.flush = flush
        if self.flush:
            r.flushall()
            r.setnx('sample',0)
            r.setnx('individual',0)

    def get_sample(self, size):
        sample_id = r.incr('sample')
        sample = [r.spop('population') for i in range(size)]
        r.sadd("sample:%s" % sample_id, *sample)
        result =  {'sample_id':"sample:%s" % sample_id ,
                   'sample':   [Individual(key).get(as_dict=True) for key in sample],
                   'server':SERVER_LIST }
        return json.dumps(result)

    def read_sample(self, size):
        sample_id = r.incr('sample')
        sample = [r.srandmember('population') for i in range(size)]
        return {'sample_id':"sample:%s" % sample_id ,
                'sample':   [Individual(key).get(as_dict=True) for key in sample],
                'server':SERVER_LIST }

    def put_sample(self,sample):
        if type(sample) == 'str':
            sample = json.loads(sample)

        if r.exists(sample['sample_id']):
            for member in sample['sample']:
                if member['id'] is None:
                    member['id'] = "individual:%s" % r.incr('individual')
                new = Individual( member['id'], fitness = member['fitness'] , chromosome  = member['chromosome'])
                new.put()
            r.delete(sample['sample_id'])


    def respawn_sample(self, sample):
        members = r.smembers(sample)
        r.sadd('population',*members)
        r.delete(sample)

PALABRA = "Hello World"
population = Population()
#Se incializa, ya que esto no es responsabilidad de la poblacion
for i in range(population.initial_size):
    key = r.incr('individual')
    chrome = [random.randint(1, 255) for i in range(len(PALABRA))]
    new = Individual("individual:%s" % key, fitness={"DefaultContext":0.0 }, chromosome  = chrome )
    new.put()

#clock_start = time.clock()
#time_start = time.time()
#
#
#
##Se crea la poblacion y se borran los datos anteriores
#population = Population()
##Para el caso de Hello World
#PALABRA = "Hello World"
#
##Se incializa, ya que esto no es responsabilidad de la poblacion
#for i in range(population.initial_size):
#    key = r.incr('chromosome')
#    chrome = [random.randint(1, 255) for i in range(len(PALABRA))]
#    new = Chromosome("chromosome:%s" % key, chromosome  = chrome )
#    new.put()
#
#
#time_end = time.time()
#clock_end = time.clock()
#
#print 'TOTAL CLOCK', clock_end-clock_start
#print 'TOTAL TIME', time_end-time_start
#
#print '*'
#
#clock_start = time.clock()
#time_start = time.time()
#
##for i in range(100):
#sample = population.get_sample(3)
#print json.dumps(sample)
#
#print sample["sample"][0]["chromosome"]
#sample["sample"][0]["chromosome"] = [60, 190, 223, 121, 24, 67, 139, 68, 252, 217, 172]
#sample["sample"][0]["id"] = None
#sample["sample"][1]["id"] = None
#sample["sample"][0]["fitness"]= 0.5
#print sample["sample_id"]
#
#print sample["sample"][0]
#population.read_sample(3)
#population.put_sample(sample)
##population.respawn(sample_id)
#
#
#time_end = time.time()
#clock_end = time.clock()
#
#
#
#sample1 = {'sample_id':'sample:69' ,
#          'sample':   [
#                      {'id':'chromosome:','fitness':{ "DefaultContex": 0.0, "User1":0.3,  },'chromosome':[12,12,12,12,312,23,23,23,21,23]},
#                      {'id':'chromosome:','fitness':0.0,'chromosome':[33,13,12,12,312,23,23,23,21,23]}
#                      ],
#          'server':['server1.protoboard.com']
#         }
#
#population1 = {'population_id':'population' ,
#              'chromosomes':   [
#                      {'id':'chromosome:3465','fitness':0.0,'chromosome':[12,12,12,12,312,23,23,23,21,23]},
#                      {'id':'chromosome:3365','fitness':0.0,'chromosome':[33,13,12,12,312,23,23,23,21,23]}
#                      ],
#              'server':['server1.protoboard.com']
#             }
#
#
#print 'TOTAL CLOCK', clock_end-clock_start
#print 'TOTAL TIME', time_end-time_start
#
