from rauth.service import OAuth1Service #see https://github.com/litl/rauth for more info
import shelve #for persistent caching of tokens, hashes,etc.
import time
import datetime 
#get your own consumer key and secret after registering a desktop app here: 
#https://dev.fitbit.com/apps/new
#for more details on the API: https://wiki.fitbit.com/display/API/Fitbit+Resource+Access+API

class Fitbit:
    def __init__(self,consumer_key,consumer_secret,verbose=0,cache_name='tokens.dat'):
        #cache stores tokens and hashes on disk so we avoid
        #requesting them every time.
        self.cache=shelve.open(cache_name,writeback=False)
        self.verbose=verbose        
        self.oauth=OAuth1Service(
                name='fitbit',
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                request_token_url='http://api.fitbit.com/oauth/request_token',
                access_token_url='http://api.fitbit.com/oauth/access_token',
                authorize_url='http://www.fitbit.com/oauth/authorize',
                header_auth=False)

        self.access_token = self.cache.get('fitbit_access_token',None)
        self.access_token_secret = self.cache.get('fitbit_access_token_secret',None)
        self.request_token =  self.cache.get('fitbit_request_token',None)
        self.request_token_secret =  self.cache.get('fitbit_request_token_secret',None)
        self.encoded_user_id =  self.cache.get('fitbit_encoded_user_id',None)
        self.pin= self.cache.get('fitbit_pin',None)
        
        #If this is our first time running- get new tokens 
        if (self.need_request_token()):
            self.get_request_token()
            got_access_token=self.get_access_token()
            if( not got_access_token):
                print "Error: Unable to get access token"
                    

    def dbg_print(self,txt):
        if self.verbose==1:
            print txt

    def get_request_token(self):
        self.request_token,self.request_token_secret = self.oauth.get_request_token(method='GET',params={'oauth_callback':'oob'})
        authorize_url=self.oauth.get_authorize_url(self.request_token)
        #the pin you want here is the string that appears after oauth_verifier on the page served
        #by the authorize_url
        print 'Visit this URL in your browser then login: ' + authorize_url
        self.pin = raw_input('Enter PIN from browser: ')
        self.cache['fitbit_request_token']=self.request_token
        self.cache['fitbit_request_token_secret']=self.request_token_secret
        self.cache['fitbit_pin']=self.pin
        print "fitbit_pin is ",self.cache.get('fitbit_pin')

    def need_request_token(self):
        #created this method because i'm not clear when request tokens need to be obtained, or how often
        if (self.request_token==None) or (self.request_token_secret==None) or (self.pin==None):
            return True
        else:
            return False

    def get_access_token(self):
        response=self.oauth.get_access_token('GET',
                request_token=self.request_token,
                request_token_secret=self.request_token_secret,
                params={'oauth_verifier':self.pin})
        data=response.content
        print response.content
        self.access_token=data.get('oauth_token',None)
        self.access_token_secret=data.get('oauth_token_secret',None)
        self.encoded_user_id = data.get('encoded_user_id',None)
        self.cache['fitbit_access_token']=self.access_token
        self.cache['fitbit_access_token_secret']=self.access_token_secret
        self.cache['encoded_user_id']=self.encoded_user_id
        if not(self.access_token) or not(self.access_token_secret):
            print "access token expired "
            return False
        else:
            return True

    
    def get_user_info(self,user_id=None):
        """Returns user profile info such as height, unit preference, timezone, stride length,etc. """
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        #note that regardless of what weightUnit is set to, the value of 'weight' is returned in kg
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/profile.json' % (user_id),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    def get_body_measurements(self,date=None,user_id=None):
        """Returns user's physical measurements, i.e. waist,bicep, chest, BMI,etc. """
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/body/date/%s.json' % (user_id,date),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    def get_activities(self,date=None,user_id=None):
        """Returns raw JSON of user's activities for the requested date or the current date if none is specified """
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/activities/date/%s.json' % (user_id,date),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    def get_foods(self,date=None,user_id=None):
        """Returns raw JSON of user's food for the requested date or the current date if none is specified """
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/foods/log/date/%s.json' % (user_id,date),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    def get_sleep(self,date=None,user_id=None):
        """Returns raw JSON of user's sleep for the requested date or the current date if none is specified """
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/sleep/date/%s.json' % (user_id,date),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    def get_heart_rate(self,date=None,user_id=None):
        """Returns raw JSON of user's heart rate for the requested date or the current date if none is specified """
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/heart/date/%s.json' % (user_id,date),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    def get_blood_pressure(self,date=None,user_id=None):
        """Returns raw JSON of user's blood pressure for the requested date or the current date if none is specified """
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/bp/date/%s.json' % (user_id,date),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    def get_glucose(self,date=None,user_id=None):
        """Returns raw JSON of user's blood glucose for the requested date or the current date if none is specified """
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/glucose/date/%s.json' % (user_id,date),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    #just make it take a date in the form 2012-09-01
    def get_body_weight(self,user_id=None,**kwargs):
        """Returns user's body weight"""
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if user_id is None:
            user_id='-'
        params={}
        if kwargs.get('base_date') is not None and kwargs.get('end_date') is not None:
            start_string=kwargs.get('base_date')
            end_string=kwargs.get('end_date')
            url_string='http://api.fitbit.com/1/user/%s/body/log/weight/date/%s/%s.json' % (user_id,start_string,end_string)
        elif kwargs.get('base_date') is not None and kwargs.get('period') in ['1d','7d','30d','1w','1m']:
            start_string=kwargs.get('base_date')
            url_string='http://api.fitbit.com/1/user/%s/body/log/weight/date/%s/%s.json' % (user_id,start_string,kwargs.get('period'))
        elif kwargs.get('date') is not None:
            date_string=kwargs.get('date')
            url_string='http://api.fitbit.com/1/user/%s/body/log/weight/date/%s.json' % (user_id,date_string)
        else:
            date_string=datetime.datetime.now().strftime('%Y-%m-%d')
            url_string='http://api.fitbit.com/1/user/%s/body/log/weight/date/%s.json' % (user_id,date_string)

        print "url_string is ",url_string
        response=self.oauth.get(
                url_string,
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

    def get_water(self,date=None,user_id=None):
        """Returns raw JSON of user's water log entries for the requested date or the current date if none is specified """
        #TODO API allows specifying units returned via Accept-Language header
        #set user_id=='-' to indicate the user currently authenticated via token credentials
        if date is None:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        if user_id is None:
            user_id='-'
        params={}
        response=self.oauth.get(
                'http://api.fitbit.com/1/user/%s/foods/log/water/date/%s.json' % (user_id,date),
                params=params,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                header_auth=True)
        return response.content

