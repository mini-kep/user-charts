"""Load test: use 'api/names' to get listing of all variables and download it.

~ 27 000 observations,  

{'a': {'len': 524, 'ts': 29},
 'd': {'len': 16259, 'ts': 13},
 'm': {'len': 7131, 'ts': 33},
 'q': {'len': 2515, 'ts': 35}}

"""

import requests 

class Frequency:
    
    def __init__(self, freq):
        self.freq = freq
        
    @property    
    def url(self):
        return f'https://minikep-db.herokuapp.com/api/names/{self.freq}'
    
    @property    
    def names(self):
        return requests.get(self.url).json()

class Datapoints:
    
    def __init__(self, freq, name):
        self.freq = freq
        self.name = name
    
    @property    
    def url(self):
        return ( 'https://minikep-db.herokuapp.com/api/datapoints'
                f'?freq={self.freq}&name={self.name}&format=json')  
    @property    
    def data(self):
        return requests.get(self.url).json()

if __name__ == '__main__':
    from time import time

    div = {'a': 1,
     'd': 1/(52*5),
     'm': 1/12,
     'q': .25}    
    
    start = time()
    
    u = {}   
    for freq in 'aqmd':    
        q = []
        for i, name in enumerate(Frequency(freq).names):
            print(freq, name)
            q.extend(Datapoints(freq, name).data)        
        u[freq] = dict(ts=i, len=len(q))    
        

    elapsed = time() - start     
 
    for freq in 'aqmd':    
        print (freq, u[freq]['len'] / u[freq]['ts'] * div[freq])
    
    print(elapsed)
    
    d = Datapoints('a', 'GDP_yoy')
    
