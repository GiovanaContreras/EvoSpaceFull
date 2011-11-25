#-*- coding: utf-8 -*-
__author__ = 'mario'

import cherrypy
import os, json
import EvoSpace



#EvoSpace.init_population("pop")
# a foo.html file will contain our Dojo code performing the XHR request
# and that's all the following config directive is doing

current_dir = os.getcwd()
config = {'/static' :
    {
    'tools.staticdir.on' : True,
    'tools.staticdir.dir' :os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    }
    }

class Content:
    @cherrypy.expose
    def EvoSpace(self):
    # read the raw POST data
        rawPost = cherrypy.request.body.read( )
    # cast to object
        obj = json.loads(rawPost)
    # process the data
        if obj["method"] == "getSample":
            result = EvoSpace.population.get_sample(obj["params"][0])
        if obj["method"] == "readSample":
            result = EvoSpace.population.read_sample()
        if obj["method"] == "respawn":
            result = EvoSpace.population.respawn(obj["params"][0])
        if obj["method"] == "putSample":
            result = EvoSpace.population.put_sample(obj["params"][0])

    # return a json response
        cherrypy.response.headers['Content-Type']= 'text/json-comment-filtered'
        return str({"result" : result})

    @cherrypy.expose
    def index(self):
        return "Servidor Funcionando"


# start up the web server and have it listen on 8088
cherrypy.config.update({'server.socket_host': '127.0.0.1',
                        'server.socket_port': 8088
                       })
cherrypy.quickstart(Content( ), '/', config=config)