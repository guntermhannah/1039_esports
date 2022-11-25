# local imports
from transform_data import *

# package imports
import time

def info_collector_script():
    "this method is a script to retrieve data from the api continuously"
    "specs: 60 calls/min"
    
    while True:
        try: 
            transform_data()
            
        except:
            continue
    

info_collector_script()
