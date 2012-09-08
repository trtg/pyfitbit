This library provides a lightweight python wrapper for the fitbit API with the goal of making it easier to visualize the data retrieved from the API. The methods provided by the API and their current state of support within this wrapper are indicated below:
    def get_body_weight

#User Profile Data
###get_user_info(self,user_id=None):
###update_user_info

#Retrieving Collection Data

###get_body_measurements(self, date=None, user_id=None):
date parameter is optional, defaults to current date. user_id parameter is optional, defaults to the currently authenticated user.

###get_activities(self, date=None, user_id=None):
date parameter is optional, defaults to current date. user_id parameter is optional, defaults to the currently authenticated user.

###get_foods
date parameter is optional, defaults to current date. user_id parameter is optional, defaults to the currently authenticated user.

###get_water
date parameter is optional, defaults to current date. user_id parameter is optional, defaults to the currently authenticated user.

###get_sleep
date parameter is optional, defaults to current date. user_id parameter is optional, defaults to the currently authenticated user.

###get_heart_rate
date parameter is optional, defaults to current date. user_id parameter is optional, defaults to the currently authenticated user.

###get_blood_pressure
date parameter is optional, defaults to current date. user_id parameter is optional, defaults to the currently authenticated user.

###get_glucose
date parameter is optional, defaults to current date. user_id parameter is optional, defaults to the currently authenticated user.

###get_body_weight(self,user_id=None,**kwargs):
Takes optional keyword arguments:
date,base_date, end_date, and period

###get_body_fat(self,user_id=None,**kwargs):
Takes optional keyword arguments:
date,base_date, end_date, and period

#Logging and Deleting Collection Data

###log_body_measurements
###log_activity
###log_food
###log_sleep
###log_heart_rate
###log_blood_pressure
###log_glucose
###log_body_weight
###log_water
###log_body_fat
###delete_body_weight_log
###delete_activity
###delete_food
###delete_sleep
###delete_heart_rate
###delete_blood_pressure
###delete_body_fat
###delete_water
