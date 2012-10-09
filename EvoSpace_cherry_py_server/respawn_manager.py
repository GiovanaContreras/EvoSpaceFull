from EvoSpace_cherry_py_server import evospace

__author__ = 'mariosky'


import time, sys

class RespawnManager(object):
    def __init__(self,respawn_interval = 100 , sleep_interval = 3, min_pop_size = 900,
                 number_samples_to_respawn = 10, popName ="pop"):
        self.respawn_interval = respawn_interval
        self.sleep_interval = sleep_interval
        self.min_pop_size = min_pop_size
        self.number_samples_to_respawn =number_samples_to_respawn
        self.server =  evospace.Population(popName)
        self.next_respawn_time = time.time()+self.respawn_interval

    def run(self):
        while True:
        #       while self.server.is_active(None):
            time.sleep(self.sleep_interval)
            size = self.server.size()
            print size, time.ctime(time.time()),
            if size <= self.min_pop_size or time.time() >= self.next_respawn_time:
                self.server.respawn(self.number_samples_to_respawn)
                self.next_respawn_time+=self.respawn_interval
                print time.ctime(self.next_respawn_time)



if __name__ == '__main__':
    if sys.argv[1] and sys.argv[2]:
        sleep_interval = sys.argv[1]
        min_pop_size = sys.argv[2]

        r = RespawnManager(int(sys.argv[1]),int(sys.argv[2]) )
        r.run()
