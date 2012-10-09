__author__ = 'mariosky'

import redis, sys

class LogExporter(object):
    def __init__(self,   file_name ,run_num=0, run_time =0  ,  pop_name = "pop", HOST = '127.0.0.1',PORT = 6379,DB = 0):
        self.pop_name = pop_name
        self.r = redis.Redis(host=HOST, port=PORT, db=DB)
        self.run_num = run_num
        self.file_name = file_name
        self.run_time = run_time

    def run(self):
        file = open(self.file_name,'a')
        populations = self.r.keys(pattern="log:*")
        pops = [int (p[4:]) for p in  populations]
        pops.sort()

        for pop_key in pops:  #Por cada poblacion en las poblaciones almacenadas
            inds = self.r.smembers("log:{}".format(pop_key)) #Extrae las claves de los individuos
            pop =   self.r.mget(*inds) #Se extrae el hash completo de todos los individuos
                                       #pop tiene el string que representa a los individuos
            for individual in pop:
                individual_dict = eval(individual)
                file.write(str(self.run_num)+" "+str(pop_key)+" "+
                                "".join([str(bit) for bit in individual_dict["chromosome"]])
                                + " "+str(individual_dict["fitness"]["DefaultContext"]) + '\n' )
        ### Last POP
        last = self.r.get("pop:returned_count")
        inds = self.r.smembers("pop")
        pop =   self.r.mget(*inds)
        for individual in pop:
            individual_dict = eval(individual)
            file.write(str(self.run_num)+" "+str(last)+" "+
                            "".join([str(bit) for bit in individual_dict["chromosome"]])
                       + " "+   str(individual_dict["fitness"]["DefaultContext"]) + '\n')
        file.write(self.run_time+ '\n')
        file.close()


if __name__ == "__main__":
    LE = LogExporter(sys.argv[1],int(sys.argv[2]),sys.argv[3])
    LE.run()

