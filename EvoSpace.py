__author__ = 'mario'

HOST = '127.0.0.1'
PORT = 6379
DB = 0

import redis, time , json, random

r = redis.Redis(host=HOST, port=PORT, db=DB)

class Individual:
    def __init__(self, key = None , fitness = {}  , chromosome  = None , from_dict = None):
        ## Se puede inicializar desde un diccionario
        if from_dict:
            self.key = from_dict['id']
            self.fitness = from_dict['fitness']
            self.chromosome = from_dict['chromosome']
        else:
        ## Se tiene minimo la llave
            self.key = key
            self.fitness = fitness
            self.chromosome = chromosome

    def put(self, population):
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
            #Se evalua el texto almacenado en Redis
            #Un diccionario para la aptitud y una lista para el cromosma
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
    def __init__(self, name = "population" ):
        self.name = name
        self.sample_counter = self.name+':sample_count'
        self.individual_counter = self.name+':individual_count'
        self.sample_queue = self.name+":sample_queue"

    def individual_next_key(self):
        key = r.incr(self.sample_counter)
        return self.name+":individual:%s" % key

    def initialize(self, initial_size = 1000):
        self.initial_size = initial_size
        r.flushall()
        r.setnx(self.sample_counter,0)
        r.setnx(self.individual_counter,0)

    def get_sample(self, size):
        sample_id = r.incr(self.sample_counter)
        sample = [r.spop(self.name) for i in range(size)]
        r.sadd(self.name+":sample:%s" % sample_id, *sample)
        r.lpush(self.sample_queue, self.name+":sample:%s" % sample_id)
        result =  {'sample_id': self.name+":sample:%s" % sample_id ,
                   'sample':   [Individual(key).get(as_dict=True) for key in sample]}
        return json.dumps(result)

    def read_sample(self, size):
        sample_id = r.incr(self.sample_counter)
        sample = [r.spop(self.name) for i in range(size)]
        result =  {'sample_id': self.name+":sample:%s" % sample_id ,
                   'sample':   [Individual(key).get(as_dict=True) for key in sample]}
        return json.dumps(result)

    def put_individual(self, key = None , fitness = {}  , chromosome  = None , from_dict = None ):
        ind = Individual( key, fitness = fitness , chromosome  = chromosome, from_dict = from_dict)
        ind.put(self.name)

    def put_sample(self,sample):
        if type(sample) == 'str':
            sample = json.loads(sample)

        if r.exists(sample['sample_id']):
            for member in sample['sample']:
                if member['id'] is None:
                    member['id'] = self.name+":individual:%s" % r.incr(self.individual_counter)
                put_individual( member['id'], fitness = member['fitness'] , chromosome  = member['chromosome'])
            r.delete(sample['sample_id'])
            r.lrem(self.sample_queue,sample['sample_id'])

    def respawn_sample(self, sample):
        members = r.smembers(sample)
        r.sadd(self.name, *members)
        r.delete(sample)
        r.lrem(self.sample_queue,sample,1)

    def respawn_ratio(self, ratio = .2):
        until_sample  = int(r.llen(self.sample_queue)*ratio)
        for i in range(until_sample):
            respawn_sample( r.lpop(self.sample_queue))


    def respawn(self, n = 1):
        current_size = r.llen(self.sample_queue)
        if n > current_size:
            for i in range(n):
                respawn_sample( r.lpop(self.sample_queue))
        else:
            for i in range(current_size):
                respawn_sample( r.lpop(self.sample_queue))



def init_population(population):
    PALABRA = "Hello World"
    population.initialize()
    for i in range(population.initial_size):
        chrome = [random.randint(1, 255) for i in range(len(PALABRA))]
        key = population.individual_next_key()
        population.put_individual(key, fitness={"DefaultContext":0.0 }, chromosome  = chrome )


population = Population("population")
init_population(population)

#clock_start = time.clock()
#time_start = time.time()

#time_end = time.time()
#clock_end = time.clock()
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
