# -*- coding: utf-8 -*-
__author__ = 'mario'

import cherrypy
import os
import GeneticSpace
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
    #############################################################
    # for sheer simplicity, this example does not use a json lib.
    # for anything more sophisticated than this example,
    # get a good json library from http://json.org
    ############################################################
    # read the raw POST data
        rawPost = cherrypy.request.body.read( )
    # cast to object
        obj = eval(rawPost) #MAJOR security hole! you’ve been warned...
    # process the data
        if obj["method"] == "getSample":
            result = GeneticSpace.population.get_sample(obj["params"][0])
        if obj["method"] == "sumOfSquares":
            result = sum([i*i for i in obj["params"][0]])
    # return a json response
        cherrypy.response.headers['Content-Type']= 'text/json-comment-filtered'
        return str({"result" : result})
    # start up the web server and have it listen on 8080

    @cherrypy.expose
    def index(self):
        return "Servidor Funcionando"



cherrypy.config.update({'server.socket_host': '127.0.0.1',
                        'server.socket_port': 8088
                       })
cherrypy.quickstart(Content( ), '/', config=config)