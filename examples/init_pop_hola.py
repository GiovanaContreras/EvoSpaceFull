__author__ = 'mariosky'


import jsonrpclib, json, random

def init_population(population_size):
    PALABRA = "Hello World"
    server = jsonrpclib.Server('http://localhost:8088/EvoSpace')

    if server.is_active(None):
        for i in range(population_size):
            chrome = [random.randint(1, 255) for i in range(len(PALABRA))]
            individual = {'id':None,'fitness':{"DefaultContext":0.0 },'chromosome':chrome}
            try:
                server.put_individual(individual)
            except:
                response = json.loads(jsonrpclib.history.response)
                print response["error"]["message"]
        server.deactivate(None)

    chrome = [random.randint(1, 255) for i in range(len(PALABRA))]
    individual = {'id':None,'fitness':{"DefaultContext":0.0 },'chromosome':chrome}
    try:
        server.put_individual(individual)
    except:
        response = json.loads(jsonrpclib.history.response)
        print response["error"]["message"]

    server.initialize(None)
    print server.is_active(None)


if __name__ == '__main__':
    init_population(20)
