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

###log_body_measurements(self,date=None,user_id=None,**kwargs):
A date may optionally be specified in the format '%Y-%m-%d' i.e. '2012-12-25'
If no date is specified, the current date will be used. At least one measurement type 
must be specified as a keyword argument, i.e. log_body_measurements(bicep="19")
Valid measurements types are:
    ["bicep","calf","chest","fat","forearm","hips","neck","thigh","waist","weight","date"]

###log_activity(self,date=None,user_id=None,**kwargs):
Parameters:
<table>
<tr>
<td>activityId</td>
<td>optional/required</td>
<td>Activity id; id of the activity, directory activity or intensity level activity; if you pass directory activity id Fitbit will calculate and substitute it with the intensity level activity id, based on distance/duration</td>
</tr>

<tr>
<td>activityName</td>
<td>optional/required</td>
<td>Custom activity name; either activityId or activityName should be provided</td>
</tr>
<tr>
<td>manualCalories</td>
<td>optional/required</td>
<td>Manual calories; amount of calories defined manually; required with activityName parameter, otherwise optional</td>
</tr>
<tr>
<td>startTime</td>
<td>required</td>
<td>Start time; hours and minutes in the format HH:mm</td>
</tr>
<tr>
<td>durationMillis</td>
<td>required</td>
<td>Duration; in milliseconds</td>
</tr>
<tr>
<td>date</td>
<td>required</td>
<td>Log entry date; in the format yyyy-MM-dd</td>
</tr>
<tr>
<td>distance</td>
<td>optional/required</td>
<td>Distance; required for logging directory activity; in the format X.XX, in the selected distanceUnit or in the unit system that corresponds to the Accept-Language header provided</td>
</tr>
<tr>
<td>distanceUnit</td>
<td>optional</td>
<td>Distance measurement unit; steps units are available only for "Walking" and "Running" directory activities and their intensity levels</td>
</tr>
</table>
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
