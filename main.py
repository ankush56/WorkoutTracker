######################

# Workout app - This app use Nutrition AI API to detect exercise based on human readable input
# Next we use Google sheets and sheety API to record workout data in sheets

########################
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

### Nutrition API #########
url = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_url = "https://api.sheety.co/fba4dfbb939ba81e50bb949091994b8f/myWorkoutsTracker/workouts"

GENDER = "female"
WEIGHT_KG = 72
HEIGHT_CM = 167
AGE = 32

API_KEY = os.environ.get('API_KEY')
API_ID = os.environ.get('API_ID')

user_input = input("Which exercise you did today?")
parameters = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

headers = {
    "x-app-key": API_KEY,
    "x-app-id": API_ID
}

response = requests.post(url, json=parameters, headers=headers)
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheet_inputs = {}
for x in result['exercises']:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": x["name"].title(),
            "duration": x["duration_min"],
            "calories": x["nf_calories"]
        }
    }


########################## Sheet API ###########

SHEET_USERNAME = os.environ.get('SHEET_USERNAME')
SHEET_PASSWORD = os.environ.get('SHEET_PASSWORD')

# POST request headers and parameters

#### AUTH Request #################
sheet_response = requests.post(sheet_url, json=sheet_inputs, auth=(SHEET_USERNAME, SHEET_PASSWORD))

#######  If bearer Token ##########
# bearer_headers = {
#     "Authorization": f"Bearer {os.environ['TOKEN']}"
# }

#### bearer token request ####
# sheet_response = requests.post(sheet_url, json=sheet_parameters, headers=bearer_headers)


sheet_result = sheet_response.json()

print("Workout is recorded in google sheets")
