__author__ = 'mariosky'


import sys,time,os

import subprocess
import ConfigParser

def run(configuration , times ):

    unique_dir_name = configuration+"-"+str(int(time.time()))
    os.mkdir(unique_dir_name)


    #Read run config file
    config = ConfigParser.ConfigParser()
    config.read("config/"+configuration+".cfg")


    #Respawn config
    sleep_interval = config.getint('respawn', 'sleep_interval')
    min_pop_size = config.getint('respawn', 'min_pop_size')

    #Worker config
    #run_number=sys.argv[1],
    #worker_id=sys.argv[2],

    #sample_size=sys.argv[3],
    #generations_per_worker=sys.argv[4],
    #binary_string_size=sys.argv[5],
    #k_trap= sys.argv[6],





    number_of_workers = config.getint('workers', 'number_of_workers')
    sample_size = config.getint('workers', 'sample_size')
    generations_per_worker = config.getint('workers', 'generations_per_worker')



    #GA Config
    k_trap = config.getint('ga', 'k_trap')
    binary_string_size = config.getint('ga', 'binary_string_size')
    base_population = config.getint('ga', 'base_population')


    for run_number in range(int(times)): # For each run
        #Run the initializer Process
        p = subprocess.Popen(
            ["python","init_trap_population.py", str(binary_string_size),
                     str(base_population),str(k_trap)])
        while p.poll() is  None: # While is still running
            time.sleep(0.8)
            print "Initializing Run {}".format(run_number) # Print which run is initializing

        #Initialice Workers
        tasks = [] #tasks list to keep track of each worker
        files = []

        for worker_id in range(number_of_workers): # For each worker
            file = open(unique_dir_name+"/"+configuration+".worker"+str(worker_id)+".txt",'a') #Open one file for append
            files.append(file)
            if run_number >= 1:            #From second time on
                file.writelines('\n')   # add a newline


            sub = subprocess.Popen(["python","trap_worker.py", str(run_number),
              str(worker_id), str(sample_size), str(generations_per_worker),
                 str(binary_string_size),str(k_trap)], stdout=file)    # Start one process for each process

            tasks.append(sub)   # Add it to the tasks list

        #Respawn Process
        respawn_process = subprocess.Popen(
            ["python","respawn_manager.py",str(sleep_interval),str(min_pop_size)],
             stdout=subprocess.PIPE)

        #Watch tasks
        start = time.time()
        while len(tasks):
            time.sleep(0.05)
            for t in tasks:
                if t.poll() is not None:

                    tasks.remove(t)
                    respawn_process.terminate()
                    for tt in tasks:
                        tt.terminate()    # Remove completed task from list
                        break
            for file in files:
                file.close()

        #Time it
        run_time= time.time()-start
        print run_time

        export = subprocess.Popen(
            ["python","pops_to_file.py", unique_dir_name+"/"+configuration+".pops.txt",
             str(run_number), str(run_time)])
        while export.poll() is  None: # While is still running
            time.sleep(2)
            print "Saving populations"











if __name__ == '__main__':
    if sys.argv[1] and sys.argv[2]:
        run(sys.argv[1],sys.argv[2] )


