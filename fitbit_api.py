from rauth.service import OAuth1Service #see https://github.com/litl/rauth for more info
import shelve #for persistent caching of tokens, hashes,etc.
import time
import datetime 
#get your own consumer key and secret after registering a desktop app here: 
#https://dev.fitbit.com/apps/new

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


