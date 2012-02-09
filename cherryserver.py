#-*- coding: utf-8 -*-
__author__ = 'mario'

import cherrypy
import os, json
import EvoSpace




# a foo.html file will contain our Dojo code performing the XHR request
# and that's all the following config directive is doing


population = EvoSpace.Population("pop")
#EvoSpace.init_population(population)


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
        method = obj["method"]
        params = obj["params"]
        id     = obj["id"]
    # process the data
        if method == "getSample":
            result = population.get_sample(*params)
        if method == "readSample":
            result = population.read_sample()
        if method == "respawn":
            result = population.respawn(params[0])
        if method == "putSample":
            result = population.put_sample(params[0])

    # return a json response
        cherrypy.response.headers['Content-Type']= 'text/json-comment-filtered'
        return json.dumps({"result" : result,"error": None, "id": id})

    @cherrypy.expose
    def index(self):
        return "Servidor Funcionando"


# start up the web server and have it listen on 8088
cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8088
                       })
cherrypy.quickstart(Content( ), '/', config=config)