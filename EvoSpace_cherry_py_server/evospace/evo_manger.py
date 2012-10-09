__author__ = 'mariosky'


import ast


import redis, time



class EvoSpaceManager(object):
    def __init__(self, pop_name = "pop", HOST = '127.0.0.1',PORT = 6379,DB = 0):
        self.pop_name = pop_name
        self.r = redis.Redis(host=HOST, port=PORT, db=DB)

    def run(self):
        #maxFitness = 0.0
        while True:
        #    print time.clock(), "smembers!"
            inds = self.r.smembers(self.pop_name)
        #    print time.clock(),"pop"
            #pop =  [ eval(d)["fitness"]["DefaultContext"]  for d in self.r.mget(*inds)]
            pop =   self.r.mget(*inds)
            fitnessList = [ast.literal_eval(d)["fitness"]["DefaultContext"]   for d in pop]
            print "PopSize:",len(pop) ,"MAX:", max(*fitnessList),"MIN:",min(*fitnessList),"AVG:",float(sum(fitnessList)) / len(fitnessList)

            print time.clock(), "diversidad"
            #print max([ ast.literal_eval(d)["fitness"]["DefaultContext"]   for d in pop])

            #diversidad = sum(distance.pdist([i["chromosome"] for i in pop],'hamming')*len(pop[0]["chromosome"]))
            #maxFitness = max(k for k in sample)
            #pop = numpy.array(pop)

            #print "Diversidad: " + str(diversidad) + " Fitness:"  +str(maxFitness )
            #print pop[0]
            #print diversidad
        #    print time.clock()






if __name__ == "__main__":
    ESM = EvoSpaceManager()
    ESM.run()

