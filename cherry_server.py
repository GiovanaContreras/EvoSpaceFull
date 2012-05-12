#-*- coding: utf-8 -*-
__author__ = 'mario'

import cherrypy
import os, json
import sys
from evospace import evospace

current_dir = os.getcwd()
config = {'/static' :
    {
    'tools.staticdir.on' : True,
    'tools.staticdir.dir' :os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

              }
    }


class Content:
    def __init__(self, popName = "pop" ):
        self.population = evospace.Population(popName)
        self.population.initialize()
        self.population.is_active = True


    @cherrypy.expose
    def EvoSpace(self):
    # read the raw POST data
        rawPost = cherrypy.request.body.read( )
    # cast to object
        obj = json.loads(rawPost)
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
                result = self.population.get_sample(*params)
            if method == "readSample":
                result = self.population.read_sample()
            if method == "respawn":
                result = self.population.respawn(params[0])
            if method == "putSample":
                result = self.population.put_sample(params[0])
            if method == "put_individual":
                result = self.population.put_individual(from_dict = params[0])
            if method == "deactivate":
                result = self.population.deactivate()
            if method == "size":
                result = self.population.size()

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

