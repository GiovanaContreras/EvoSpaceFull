__author__ = 'mariosky'

import time, jsonrpclib, json

class RespawnManager(object):
    def __init__(self,respawnInterval = 60 , sleepInterval = 20, minPopSize = 9000,
                 numberOfSamplesToRespawn = 20,EvoSpaceURL = 'http://172.16.51.1:8088/EvoSpace'):
        self.respawnInterval = respawnInterval
        self.sleepInterval = sleepInterval
        self.minPopSize = minPopSize
        self.numberOfSamplesToRespawn =numberOfSamplesToRespawn
        self.EvoSpaceURL = EvoSpaceURL

        self.server = jsonrpclib.Server('http://localhost:8088/EvoSpace')
        self.nextRespawnTime = time.time()+self.respawnInterval

    def run(self):
        while self.server.is_active(None):
            size = self.server.size(None)
            print size, time.ctime(time.time()),
            if size <= self.minPopSize or time.time() >= self.nextRespawnTime:
                self.server.respawn(self.numberOfSamplesToRespawn)
                self.nextRespawnTime+=self.respawnInterval
                print time.ctime(self.nextRespawnTime)
            time.sleep(self.sleepInterval)

r = RespawnManager()
r.run()






