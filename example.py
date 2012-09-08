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

#if no date is specified, retrieves user's measurements on the current day
user_measurements=myfb.get_body_measurements('2012-08-01')
print user_measurements

#user_weight = myfb.get_body_weight(start_date='2012-08-01',end_date='2012-09-01')
#user_weight = myfb.get_body_weight(base_date='2012-08-29',period='7d') #base_date acts as end date when period is specified
#user_weight = myfb.get_body_weight(date='2012-08-25')
user_weight = myfb.get_body_weight()#use current date when no argument is given
print "get_body_weight is ",user_weight

user_activities = myfb.get_activities() 
print "get_activities is ",user_activities
