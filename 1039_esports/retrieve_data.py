# local imports
from transform_data import *

# package imports
import time

def info_collector_script():
    "this method is a script to retrieve data from the api continuously"
    "specs: 60 calls/min"
    start_time = time.time()
    transform_data()
    print("--- %s seconds ---" % (time.time() - start_time))

info_collector_script()
