__author__ = 'mariosky'

import time, jsonrpclib

class RespawnManager(object):
    def __init__(self,respawnInterval = 20 , sleepInterval = 10, minPopSize = 9000,
                 numberOfSamplesToRespawn = 10,EvoSpaceURL = 'http://127.0.0.1:8088/EvoSpace'):
        self.respawnInterval = respawnInterval
        self.sleepInterval = sleepInterval
        self.minPopSize = minPopSize
        self.numberOfSamplesToRespawn =numberOfSamplesToRespawn
        self.EvoSpaceURL = EvoSpaceURL

        self.server = jsonrpclib.Server('http://localhost:8088/EvoSpace')
        self.nextRespawnTime = time.time()+self.respawnInterval

    def run(self):
        while True:

#       while self.server.is_active(None):
            time.sleep(self.sleepInterval)
            size = self.server.size(None)
            print size, time.ctime(time.time()),
            if size <= self.minPopSize or time.time() >= self.nextRespawnTime:
                self.server.respawn(self.numberOfSamplesToRespawn)
                self.nextRespawnTime+=self.respawnInterval
                print time.ctime(self.nextRespawnTime)


r = RespawnManager()
r.run()






