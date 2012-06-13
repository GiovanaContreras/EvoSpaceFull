__author__ = 'mario'

HOST = '127.0.0.1'
PORT = 6379
DB = 0

LOGGING = True
LOG_INTERVAL = 10

import redis, json

r = redis.Redis(host=HOST, port=PORT, db=DB)

class Individual:
    def __init__(self, **kwargs):
        ## Se puede inicializar desde un diccionario

        self.id = kwargs['id']
        self.fitness = kwargs.get('fitness',{})
        self.chromosome = kwargs.get('chromosome',[])
        self.__dict__.update(kwargs)

    def put(self, population):
        pipe = r.pipeline()
        if pipe.sadd( population, self.id ):
            pipe.set( self.id , self.__dict__ )
            pipe.execute()
            return True
        else:
            return False

        
    def get(self, as_dict = False):
            #Se evalua el texto almacenado en Redis
            #Esto crea el tipo de dato correspondiente en python
            #fitness es un diccionario y chromosome una lista
        dict = eval(r.get(self.id))
        self.__dict__.update(dict)

        if as_dict:
            return self.__dict__
        else:
            return self

    def __repr__(self):
        return self.id +":"+ str(self.fitness) +":" + str( self.chromosome)

    def as_dict(self):
        return self.__dict__


class Population:
    def __init__(self, name = "pop" ):
        self.name = name
        self.sample_counter = self.name+':sample_count'
        self.individual_counter = self.name+':individual_count'
        self.sample_queue = self.name+":sample_queue"
        self.returned_counter = self.name+":returned_count"
        self.log_queue = self.name+":log_queue"
        #Esta es una propiedad del EvoSpaceServer NO de la poblacion
        self.is_active = False

    ##NOOO Aqui
    def deactivate(self):
        self.is_active = False

    def individual_next_key(self):
        key = r.incr(self.individual_counter)
        return self.name+":individual:%s" % key

    def size(self):
        return r.scard(self.name)

    def initialize(self):
        r.flushall()
        r.setnx(self.sample_counter,0)
        r.setnx(self.individual_counter,0)
        r.setnx(self.returned_counter,0)

        ##NOOO Aqui
        self.is_active = True

    def get_sample(self, size):
        sample_id = r.incr(self.sample_counter)
        sample = [r.spop(self.name) for i in range(size)]
        r.sadd(self.name+":sample:%s" % sample_id, *sample)
        r.rpush(self.sample_queue, self.name+":sample:%s" % sample_id)
        try:
            result =  {'sample_id': self.name+":sample:%s" % sample_id ,
                   'sample':   [Individual(id=key).get(as_dict=True) for key in sample]}
        except:
            return None
        return json.dumps(result)

    def read_sample_queue(self):
        result = r.lrange(self.sample_queue,0,-1)
        return json.dumps(result)
#####
##### Read Sample es ReadALL Pop
#####
#    def read_sample(self, size):
#        sample_id = r.incr(self.sample_counter)
#        sample = [r.spop(self.name) for i in range(size)]
#        result =  {'sample_id': self.name+":sample:%s" % sample_id ,
#                   'sample':   [Individual(key).get(as_dict=True) for key in sample]}
#        return json.dumps(result)

    def read_sample(self):
        sample = r.smembers(self.name)
        result =  { 'sample':   [Individual(id=key).get(as_dict=True) for key in sample]}
        return json.dumps(result)

    def put_individual(self, **kwargs ):

        #Esto debe hacerse fueran, recibe un diccionario y punto.
        #if isinstance(from_dict,str):
        #    from_dict = json.loads(from_dict)

        if kwargs['id'] is None:
            kwargs['id'] = self.name+":individual:%s" % r.incr(self.individual_counter)
        ind = Individual(**kwargs)
        ind.put(self.name)

    def put_sample(self,sample):
        if not isinstance(sample,dict):
            sample = json.loads(sample)

        if r.exists(sample['sample_id']):
            if LOGGING:
                count = r.incr(self.returned_counter)
                if count % LOG_INTERVAL == 0 :
                    r.sunionstore("log:"+str(count),"pop")



            for member in sample['sample']:
                if member['id'] is None:
                    member['id'] = self.name+":individual:%s" % r.incr(self.individual_counter)
                self.put_individual(**member)
               # self.put_individual( member['id'], fitness = member['fitness'] , chromosome  = member['chromosome'])
            r.delete(sample['sample_id'])
            r.lrem(self.sample_queue,sample['sample_id'])

    def respawn_sample(self, sample):
        if r.exists(sample):
            members = r.smembers(sample)
            r.sadd(self.name, *members)
            r.delete(sample)
            r.lrem(self.sample_queue,sample,1)

    def respawn_ratio(self, ratio = .2):
        until_sample  = int(r.llen(self.sample_queue)*ratio)
        for i in range(until_sample):
            self.respawn_sample( r.lpop(self.sample_queue))


    def respawn(self, n = 1):
        current_size = r.llen(self.sample_queue)
        if n > current_size:
            for i in range(current_size):
                self.respawn_sample( r.lpop(self.sample_queue))
        else:
            for i in range(n):
                self.respawn_sample( r.lpop(self.sample_queue))



if __name__ == "__main__":
    p = Population("pop")
    p.initialize()
    k = p.individual_next_key()
    i = Individual(id=k)
    i.test = "Hola"
    i.put("pop")

    print i.get(True)



#for i in range(4):
#    population.get_sample(5)


#s = population.get_sample(5)

#print type(s)
#print s

#population.put_sample(s)

#clock_start = time.clock()
#time_start = time.time()

#time_end = time.time()
#clock_end = time.clock()
#
#
#sample1 = {'sample_id':'sample:69' ,
#          'sample':   [
#                      {'id':'chromosome:','fitness':{ "DefaultContext": 0.0, "User1":0.3,  },'chromosome':[12,12,12,12,312,23,23,23,21,23]},
#                      {'id':'chromosome:','fitness':0.0,'chromosome':[33,13,12,12,312,23,23,23,21,23]}
#                      ],
#         
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
#  test =  """{"sample": [{"id": "population:individual:55", "chromosome": [29, 91, 94, 111, 242, 115, 55, 96, 144, 43, 198], "fitness": {"DefaultContext": 0.0}}, {"id": "population:individual:102", "chromosome": [111, 249, 171, 208, 165, 213, 61, 231, 34, 84, 4], "fitness": {"DefaultContext": 0.0}}, {"id": "population:individual:33", "chromosome": [200, 249, 124, 95, 25, 71, 185, 112, 84, 84, 18], "fitness": {"DefaultContext": 0.0}}], "sample_id": "population:sample:1004"}"""