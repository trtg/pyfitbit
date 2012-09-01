import fitbit_api as fb 
import matplotlib.pyplot as plt #for plotting data
from datetime import *
from pandas import * #for dataframe
import json #for manipulating API responses
from credentials import *#credentials.py should define consumer_secret and consumer_key
#-----------------------------------
#get your own consumer key and secret after registering a desktop app here: 
#https://dev.fitbit.com/apps/new

myfb=fb.Fitbit(consumer_key,consumer_secret)
user_info = myfb.get_user_info()
print user_info
user_measurements=myfb.get_body_measurements()
print user_measurements
