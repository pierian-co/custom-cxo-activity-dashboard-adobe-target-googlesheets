## High Level Steps: 
## 1. Get the Adobe IO Project details to connect to an Adobe Target account
## 2. Generate JWT
## 3. Generate Access Token
## 4. Extract the list of activities and put those in Google Sheet

#---------------------------------------------------------------------------------------------------------------
## Difference between GoogleSheets and WorkSheets
## GoogleSheet: The file within GoogleDrive which may contain one or multiple worksheets/tabs
## Worksheet: Tab/Sheet equivalent of Excel - contains actual data
#---------------------------------------------------------------------------------------------------------------

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import jwt
from jwt.algorithms import RSAAlgorithm
import time
from datetime import datetime
import requests
from urllib.parse import urlencode
import json
import pandas as pd

#---------------------------------------------------------------------------------------------------------------
## Constants
#---------------------------------------------------------------------------------------------------------------

# Names of the two GoogleSheets
ACTIVITIESDATA_GOOGLESHEET_NAME = "YOUR-ACTIVITIES-DATA-GOOGLESHEET-NAME"
CREDENTIALS_GOOGLESHEET_NAME = "YOUR-CREDENTIALS-GOOGLESHEET-NAME"

# Names of worksheets/tabs within GoogleSheets
# Change these if you have different names
WORKSHEET_ACTIVITIESDATA_NAME = "ActivitiesData"
WORKSHEET_CREDENTIALS_NAME = "Credentials"

# Indexes of Worksheets/Tabs. Index starts from 0 so first sheet as index 0
WORKSHEET_ACTIVITIESDATA_INDEX = 0
WORKSHEET_CREDENTIALS_INDEX = 0

# Last column in ActivitiesData sheet
# Need to find a way to get last column in a sheet using gspread
ACTIVITIESDATA_LAST_COLUMN = "U"

# Name of Google Service Account JSON Keypair File Name
SERVICE_ACCOUNT_CREDENTIALS_KEYFILE_NAME = "YOUR GOOGLE SERVICE ACCOUNT CREDENTIALS.json"

# Hosts and Endpoints for Adobe IO APIs
IMS_HOST = 'ims-na1.adobelogin.com'
IMS_ENDPOINT_JWT = '/ims/exchange/jwt/'

# Keys for dictionary with Adobe IO Project Credentials
IOPROJECT_API_KEY = 'X-Api-Key'
IOPROJECT_CLIENT_SECRET = 'Client-Secret'
IOPROJECT_ORG_ID = 'Adobe-Org-Id'
IOPROJECT_ACCOUNT_ID = 'Tech-Account_Id'
IOPROJECT_PRIAVTE_KEY_PATH = 'Private-Key-Path'

# Dictionary to map Fields of AT Activity Details API to GoogleSheet Column indices
DICT_TARGETAPI_SHEETCOLUMNS_MAPPING = {
    "id": 0,
    "name": 1,
    "type": 2,
    "state": 3,
    "priority": 4,
    "modifiedAt": 5,
    "start": 6,
    "end": 7,
    "thirdPartyId": 8,
    "workspace": 9
}

# Constant to define whether logs should be  printed. 
# Set the value to False if logs are not needed
DEBUG_LOGS_FLAG = True

#---------------------------------------------------------------------------------------------------------------
## Configurations
#---------------------------------------------------------------------------------------------------------------

# Adobe Target Tenant you want to extract activities for
# This must be present in Credentials sheet
ADOBE_TARGET_TENANT = "YOUR-ADOBE-TARGET-TENANT"
   
#---------------------------------------------------------------------------------------------------------------
## Common Variables
#---------------------------------------------------------------------------------------------------------------

dict_ioproject_credentials = {}

#---------------------------------------------------------------------------------------------------------------
## Custom Functions
#---------------------------------------------------------------------------------------------------------------

# Function-name: next_available_row
# This function returns the row number of the next empty row of a Google Worksheet
# Input: Google Worksheet
# Output: Integer
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list)+1

# A custom print function for debugging purposes
# it takes string as param
# checks whether DEBUG_LOGS is true; if yes prints the function
def myprint(str_to_print, end = "\n"):
    if DEBUG_LOGS_FLAG == True:
        print(str_to_print, end)

# Function-name: generate_jwt
# This function generates JWT for the Adobe IO Project with Adobe Target APIs
# Input: Google Worksheet with credentials
# Output: String - JWT token 
def generate_jwt():
    # expiry time as 24 hours
    expiry_time_jwt = int(time.time()) + 60*60*24
    
    # create payload
    payload = {
        'exp' : expiry_time_jwt,
        'iss' : dict_ioproject_credentials[IOPROJECT_ORG_ID],
        'sub' : dict_ioproject_credentials[IOPROJECT_ACCOUNT_ID],
        'https://ims-na1.adobelogin.com/s/ent_marketing_sdk': True,    
        'aud' : "https://" + IMS_HOST + "/c/" + dict_ioproject_credentials[IOPROJECT_API_KEY]
    }

    # read the private key we will use to sign the JWT.
    priv_key_file = open(dict_ioproject_credentials[IOPROJECT_PRIAVTE_KEY_PATH])
    priv_key = priv_key_file.read()
    priv_key_file.close()

    # create JSON Web Token, signing it with the private key.
    jwt_token = jwt.encode(payload, priv_key, algorithm='RS256')

    # decode bytes into string
    # jwt_token = jwt_token.decode("utf-8")
    
    return jwt_token


# Function-name: generate_access_token
# This function generates access token which needs to be passed to access Adobe Target APIs
# Input: JWT
# Output: String - Access Token
def generate_access_token(jwt_token):

    access_token = ''
    
    # Final URL for access-token generation API end-point
    accesstoken_url = "https://" + IMS_HOST + IMS_ENDPOINT_JWT

    accesstoken_headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Cache-Control" : "no-cache"
    }

    accesstoken_body_credentials = {
        "client_id" : dict_ioproject_credentials[IOPROJECT_API_KEY],
        "client_secret" : dict_ioproject_credentials[IOPROJECT_CLIENT_SECRET],
        "jwt_token" : jwt_token
    }
    
    accesstoken_body = urlencode(accesstoken_body_credentials)

    # send http request

    res = requests.post(accesstoken_url, headers = accesstoken_headers, data = accesstoken_body)

    if res.status_code == 200:
        # extract token
        access_token = json.loads(res.text)['access_token']
    
    return access_token

# Function-name: get_adobetarget_activitieslist
# This function calls Adobe Target's API to fetch list of activities 
# Input: string - access token
# Output: json - corresponding to list of activities
def get_adobetarget_activitieslist(access_token):
    
    # Endpoint for Adobe Targte Activities List API
    # More details: https://developers.adobetarget.com/api/#list-activities
    activitieslist_url = "https://mc.adobe.io/" + ADOBE_TARGET_TENANT + "/target/activities/"

    activitieslist_headers = {
        "Accept" : "application/vnd.adobe.target.v3+json",
        "Cache-Control" : "no-cache",
        "X-Api-Key": dict_ioproject_credentials[IOPROJECT_API_KEY],
        "Authorization" : "Bearer " + access_token
    }

    # activitieslist_body = urlencode(body_credentials)

    # send http request
    res = requests.get(activitieslist_url, headers=activitieslist_headers)
                       
    if res.status_code == 200:
        res_json_data = json.loads(res.text)
        res_total_count = res_json_data["total"]
        if res_total_count >= 0:
            myprint("Total number of activities returned: " + str(res_total_count))
            res_activities = res_json_data["activities"]
            return res_activities


## Function-name: update_value_in_sheet_activity_list
## This function updates data retrieved from Adobe Target into sheet-activity-list
## sheet-activity-list represents a list that is pushed into Activities Data
## Input: target_activity_key - name of the key from Adobe Target API
## Input: sheet_activity_list - list of values that represent a sheet-activity
## Output: sheet_activity_list - updated list
def update_value_in_sheet_activity_list(target_activity_key, target_activity_keys, target_activity, sheet_activity_list):
    if target_activity_key in target_activity_keys:
        # get the corresponding GoogleSheet column from dict_apifields_sheetcolumns_mapping
        sheet_activity_list[DICT_TARGETAPI_SHEETCOLUMNS_MAPPING[target_activity_key]] = target_activity[target_activity_key]
    return sheet_activity_list

## Funtion-name: lear_activitiessheet_data
## This function clears data in activities sheet, leaving only header row
## Input: googlesheet - googlesheet object
## Input: worksheet - worksheet to be cleared
## Output: None
def clear_activitiessheet_data(googlesheet, worksheet):
    googlesheet.values_clear(WORKSHEET_ACTIVITIESDATA_NAME + \
                                            "!A2:" + ACTIVITIESDATA_LAST_COLUMN + str(next_available_row(worksheet)))
    
        
def main(data, context):
    #---------------------------------------------------------------------------------------------------------------
    ## Initialisations
    #---------------------------------------------------------------------------------------------------------------

    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    # SERVICE_ACCOUNT_CREDENTIALS_KEYFILE_NAME 
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_CREDENTIALS_KEYFILE_NAME, scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instances of both GoogleSheets
    googlesheet_credentials = client.open(CREDENTIALS_GOOGLESHEET_NAME)
    googlesheet_activitiesdata = client.open(ACTIVITIESDATA_GOOGLESHEET_NAME)

    # initialise both worksheets
    worksheet_credentials = googlesheet_credentials.get_worksheet(WORKSHEET_CREDENTIALS_INDEX)
    worksheet_activitiesdata = googlesheet_activitiesdata.get_worksheet(WORKSHEET_ACTIVITIESDATA_INDEX)


    #---------------------------------------------------------------------------------------------------------------
    ## 1. Iterate through the Credentials worksheet to gather data to connect with Adobe IO
    #----------------------------------------------------------------------------------------------------------------

    # get data from Credentials worksheet
    credentials_data = worksheet_credentials.get_all_records()

    # convert credentials data to a Pandas dataframe
    credentials_df = pd.DataFrame.from_dict(credentials_data)

    # create sereis of Tenant column
    # you can add multiple tenants in Credentials sheet
    tenants_series = credentials_df.loc[:,'Tenant']

    # get the row index of tenant you want to get report on
    tenant_index = tenants_series[tenants_series == ADOBE_TARGET_TENANT].index[0]

    # extract all credentials params required for creating JWT and Access token and put these in a dict
    dict_ioproject_credentials[IOPROJECT_API_KEY] = credentials_df.loc[tenant_index,'X-Api-Key']
    dict_ioproject_credentials[IOPROJECT_CLIENT_SECRET] = credentials_df.loc[tenant_index,'Client-Secret']
    dict_ioproject_credentials[IOPROJECT_ORG_ID] = credentials_df.loc[tenant_index,'Adobe-Org-Id']
    dict_ioproject_credentials[IOPROJECT_ACCOUNT_ID] = credentials_df.loc[tenant_index,'Tech-Account_Id']
    dict_ioproject_credentials[IOPROJECT_PRIAVTE_KEY_PATH] = credentials_df.loc[tenant_index,'Private-Key-Path']


    #---------------------------------------------------------------------------------------------------------------
    ## 2. Generate JWT
    #----------------------------------------------------------------------------------------------------------------

    jwt_token = generate_jwt()
    myprint("JWT Token is:" + str(jwt_token))

    #---------------------------------------------------------------------------------------------------------------
    ## 3. Generate Access Token using JWT
    #----------------------------------------------------------------------------------------------------------------

    access_token = generate_access_token(jwt_token)
    myprint("Access token is:" + access_token)

    #---------------------------------------------------------------------------------------------------------------
    ## 4. Get list of Adobe Target Activities
    ## there are 2 types of Activities
    ## A. target_activity: activity returned by Adobe Target
    ## B. existing_activity: acivity that already exists in GoogleSheet
    #----------------------------------------------------------------------------------------------------------------
    if access_token is not None and access_token != "":
        # get the list of activities from Adobe Target
        target_activities_list = get_adobetarget_activitieslist(access_token)

        # get data from ActivitiesData worksheet and create a Dataframe
        existing_sheet_activities_data = worksheet_activitiesdata.get_all_records()
        existing_sheet_activities_df = pd.DataFrame.from_dict(existing_sheet_activities_data)

        # get the count of existing activities in Activities sheet
        existing_sheet_activities_count = len(existing_sheet_activities_df.index)

        # create series of Activity-IDs that already exist in ActivitiesData sheet
        if existing_sheet_activities_count > 0:
            existing_sheet_activities_ids = existing_sheet_activities_df.loc[:,'AT-ID']
        
        # if no existing activities then create a list of all activities data and update the sheet
        if existing_sheet_activities_count == 0:
            # list to hold activity list - A list of lists that will be written to the googlesheet
            toupload_activities_list = []
        else:
            # if there are existing activities in AcvitiesSheet then put the data into a list of lists
            # each list represents row for an activity
            # We'll also clear all the content excpet the header row
            # as I could not find a way to replace rows in gspread package - SUGGESTIONS WELCOME
            toupload_activities_list = existing_sheet_activities_df.values.tolist()
            # clear the content of ActivitiesData sheet
            clear_activitiessheet_data(googlesheet_activitiesdata, worksheet_activitiesdata)
        
        # iterate through list of activities returned by Adobe Target Activities List API
        for target_activity in target_activities_list:
            # this flag means an existing sheet-activity has been modified since last time and should be updated
            # Conditions when it will be set True
            # 1. if target-modified-date is different from sheet-last-updated-date
            # 2. if target-modified-date or sheet-last-updated-date does not exist
            # 3. if target-actity does not exist in ActivitiesData
            sheet_activity_needs_update_flag = False
            
            # get the list of all keys in target-activity
            target_activity_keys = list(target_activity.keys())
            
            if 'id' in target_activity_keys:
                target_activity_id  = target_activity['id']  
                # Initialise a list to hold data for an activity
                
                toupload_activity_list = [''] *11
               
                # If activity already exists but lastModifiedDate is still the same then do not take any action
                if existing_sheet_activities_count > 0:
                    
                    if target_activity_id in existing_sheet_activities_ids.values:
                        sheet_activity_row = existing_sheet_activities_ids[existing_sheet_activities_ids==target_activity_id].index[0]
                        toupload_activity_list = toupload_activities_list[sheet_activity_row]
                        print("activity_id " + str(target_activity_id))
                        print("activity_row" + str(sheet_activity_row))
                        print("activity_list" + str(toupload_activity_list))
                        # get the lastModifiedDate from Adobe Target
                        if 'modifiedAt' in target_activity_keys:
                            target_activity_modified_date = target_activity['modifiedAt']
                            sheet_activity_last_update_date = toupload_activity_list[10]
                            # compare target-activity-modified is different from  wit
                            datetime_lastmodified = datetime.strptime(target_activity_modified_date, '%Y-%m-%dT%H:%M:%SZ')
                            datetime_lastupdated = datetime.strptime(sheet_activity_last_update_date, '%Y-%m-%dT%H:%M:%SZ')
                            print(""+str(datetime_lastmodified))
                            print(""+str(datetime_lastupdated))
                            if datetime_lastmodified > datetime_lastupdated:
                                print("Activity flag is true")
                                sheet_activity_needs_update_flag = True
                        else:
                            sheet_activity_needs_update_flag = True
                    else:
                        sheet_activity_needs_update_flag = True
                else:
                    sheet_activity_needs_update_flag = True
                
                if sheet_activity_needs_update_flag == True:
                    # 1. update sheet_activity_list with the latest Adobe Target data
                    toupload_activity_list = update_value_in_sheet_activity_list('id', target_activity_keys, target_activity, toupload_activity_list)
                    toupload_activity_list = update_value_in_sheet_activity_list('name', target_activity_keys, target_activity, toupload_activity_list)
                    toupload_activity_list = update_value_in_sheet_activity_list('type', target_activity_keys, target_activity, toupload_activity_list)
                    toupload_activity_list = update_value_in_sheet_activity_list('state', target_activity_keys, target_activity, toupload_activity_list)
                    toupload_activity_list = update_value_in_sheet_activity_list('priority', target_activity_keys, target_activity, toupload_activity_list)
                    toupload_activity_list = update_value_in_sheet_activity_list('modifiedAt', target_activity_keys, target_activity, toupload_activity_list)

                    if 'lifetime' in target_activity_keys:
                        target_activity_lifetime = target_activity['lifetime']
                        lifetime_keys = list(target_activity_lifetime.keys())
                        if 'start' in lifetime_keys:
                            toupload_activity_list[DICT_TARGETAPI_SHEETCOLUMNS_MAPPING['start']] = target_activity_lifetime['start']
                        if 'end' in lifetime_keys:
                            toupload_activity_list[DICT_TARGETAPI_SHEETCOLUMNS_MAPPING['end']] = target_activity_lifetime['end']
                        
                    
                    toupload_activity_list = update_value_in_sheet_activity_list('thirdPartyId', target_activity_keys, target_activity, toupload_activity_list)
                    toupload_activity_list = update_value_in_sheet_activity_list('workspace', target_activity_keys, target_activity, toupload_activity_list)
                    
                    toupload_activity_list[10] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                    
                    # if an existing sheet-activity has been updated 
                    # then update the list of activities toupload_activities_list
                    # else append the activity-list to toupload_activities_list
                    if existing_sheet_activities_count > 0 and target_activity_id in existing_sheet_activities_ids.values:
                        sheet_activity_index = existing_sheet_activities_ids[existing_sheet_activities_ids==target_activity_id].index[0]
                        toupload_activities_list[sheet_activity_index] = toupload_activity_list
                    else:
                        toupload_activities_list.append(toupload_activity_list)
        
        # upload list of activities to ActivitiesData Worksheet
        worksheet_activitiesdata.append_rows(toupload_activities_list, 2)  

if __name__ == "__main__":
    main('data','context')

