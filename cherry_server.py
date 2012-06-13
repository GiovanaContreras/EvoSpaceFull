#-*- coding: utf-8 -*-
__author__ = 'mario'

import cherrypy
from cherrypy._cpcompat import ntou

import os, json
import sys
from evospace import evospace
from evoArt.colors import init_pop, evolve


current_dir = os.getcwd()
config = {
    '/static' :
    {
    'tools.staticdir.on' : True,
    'tools.staticdir.dir' :os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

              },
    '/prototype' :
            {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' :os.path.abspath(os.path.join(os.path.dirname(__file__), 'prototype'))

        }


    }

class Content:
    def __init__(self, popName = "pop" ):
        self.population = evospace.Population(popName)
        self.population.initialize()
        self.population.is_active = True


    @cherrypy.expose
    @cherrypy.tools.json_in(content_type=[ntou('application/json'),
                                          ntou('text/javascript'),
                                          ntou('application/json-rpc')
                                          ])
    def EvoSpace(self):
        # if cherrypy.request.json ??
        obj = cherrypy.request.json
        method = obj["method"]
        params = obj["params"]
        id     = obj["id"]
    # process the data
        cherrypy.response.headers['Content-Type']= 'text/json-comment-filtered'

        if method == "is_active":
            result = self.population.is_active
            return json.dumps({"result" : result,"error": None, "id": id})

        if method == "initialize":
            result = self.population.initialize()
            return json.dumps({"result" : result,"error": None, "id": id})

        if self.population.is_active:
            if method == "getSample":
                result = self.population.get_sample(params[0])
                if result:
                    return json.dumps({"result" : result,"error": None, "id": id})
                else:
                    return json.dumps({"result" : None,"error":
                            {"code": -32601, "message": "EvoSpace empty"}, "id": id})
            elif method == "readSample":
                result = self.population.read_sample()
            elif method == "respawn":
                result = self.population.respawn(params[0])
            elif method == "putSample":
                result = self.population.put_sample(params[0])
            elif method == "put_individual":
                result = self.population.put_individual(**params[0])
            elif method == "deactivate":
                result = self.population.deactivate()
            elif method == "size":
                result = self.population.size()
            ###evoArt App
            elif method == "init_pop":
                result = init_pop(populationSize=params[0])
            elif method == "evolve":
                result = evolve(sample_size=params[0])


            return json.dumps({"result" : result,"error": None, "id": id})

        else:
            return json.dumps({"result" : None,"error":
                {"code": -32601, "message": "EvoSpace Not Available"}, "id": id})



    # return a json response

    @cherrypy.expose
    def index(self):
        return "Servidor Funcionando"

if __name__ == '__main__':
    # start up the web server and have it listen on 8088
    if len(sys.argv) == 2:
        popName = sys.argv[1]
    else:
        popName = "pop"

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8088
        ,'server.environment':  'production'
    ,'server.thread_pool':   200
    ,'tools.sessions.on':    False
                           })
    cherrypy.quickstart(Content(popName), '/', config=config)

