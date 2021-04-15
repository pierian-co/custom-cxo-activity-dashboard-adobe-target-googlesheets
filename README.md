
# Custom, sharable CXO Activity Dashboard using Adobe Target and GoogleSheets

**Digital Marketing Challenge:** If you use Adobe Target for Experimentation and Personalisation activities, you'd be aware of the Activities Listing page (or Dashboard page) which gives a view of all activities. While this page covers list of activities with information such as Activity-Name and Last Update Date, we wanted to extend it
1. to add custom meta-data to each activity for more filtering criteria e.g. which team owns the activity or whether it's an experimentation/personalisation activity
2. to be able to filter/sort activities on fields that are not available on Activities List page. One of the most important one is Priority - makes life much easier to see all the activities that have priorities higher than a specific limit
3. to easily share this activity-dashboard with other team-members who may not be active Adobe Target users
4. to add visualisation layer on top of activities data using Google Data Studio
 
## Prerequisites
- Access to Adobe Target and profiles you want to report on
- Developer access to Adobe Target product
- Access to  Google Developer Console

## Technologies used
- Adobe IO
- GoogleSheets API
- Python
- Google Data Studio


## High-level Steps:
[1. Get Credentials of Adobe IO Project](#step1)

[2. Create GoogleSheets](#step2)

[3. Create Google Service Account with GoogleSheets APIs](#step3)

[4. Share GoogleSheets with Google Service Account](#step4)

[5. Python code to read activities from Adobe Target using Adobe IO and update GoogleSheet](#step5)

[6. Schedule Python code to run recurrently using GCP Cloud Functions, Cloud Scheduler and Pub-Sub](#step6)

[7. Visualise activities data using Google Data Studio](#step7)

[8. Share GoogleSheet and Data Studio Dashboard](#step8)


### <a name="step1"></a> Step 1. Get Credentials of an existing Adobe IO Project or Create a new Adobe IO Project with Adobe Target services
If you have an existing Adobe IO Project with Adobe Target service, login to Adobe IO Console, select your project and copy credentials from Credentials details page.

If you do not have an existing project,  [create a new Adobe IO Project with Adobe Target services](https://github.com/pierian-co/custom-cxo-activity-dashboard-adobe-target-googlesheets/blob/main/create_adobeioproject_target.md).

![new adobe io project credentials](https://user-images.githubusercontent.com/71815964/104573955-6a404700-564d-11eb-9711-a1f47cf99454.png)


### <a name="step2"></a> Step 2. Create GoogleSheets
I have used 2 separate GoogleSheets - one to store Credentials to connect to Adobe IO and another to store details of Adobe Target activities. This way we need not worry about Credentials being shared further - only activity data is shared with the recipients. 

**1. Credentials GoogleSheet** 
This GoogleSheet contains credentials of the Adobe IO project created on Step 1 above. Here's the [template of Credentials sheet](https://docs.google.com/spreadsheets/d/1nkF3EE3WL0UGhtFFFxjhG1OkDKyGSIBuW6Fd3kcmJa4/edit?usp=sharing)

Fields in Credentials sheet
- Tenant: Adobe Target tenant (you can find it in the URL when you select Adobe Target from Adobe Experience Cloud Console)
- Target Client Code: Get this under Account details section of Adobe Target console by navigating to Administration > Implementation 
- X-Api-Key: Client ID from your Adobe IO Project's Credential page
- Client-Secret: Get it by clicking on Retrieve client secret button on your Adobe IO Project's Credential page
- Adobe-Org-Id: Organization Id from your Adobe IO Project's Credential page
- Tech-Account_Id: Technical Account ID from your Adobe IO Project's Credential page
- Private-Key-Path: local path of Private Key generated when Adobe IO Project was created (refer to Step 1 details)

**2. ActivitiesData GoogleSheet**
ActivitiesData GoogleSheet contains data related to Adobe Target activities. Here's the [template of ActivitiesData sheet](https://docs.google.com/spreadsheets/d/1lk5btAUQAwO6IfaA4UeqSIF29wnC7zNNvsA_Dyoophw/edit?usp=sharing) I have used in this project.

This GoogleSheet contains 2 types of fields:
a. Extracted from Adobe Target API: The fields have prefix of AT in the template.
b. Custom fields: I have added some custom fields examples in the template that can be updated against each activity. Anyone who accesses the dashboard can make use of these custom fields to filter activities e.g. 
- just show me activities that belong to eCommerce team
- show me activities that had a clear winning experience

Additionally you can add fields that provide further details about an activity. For example, we create a Confluence page for each activity with all details such as Audiences, Screen-shots, Results and so on. Users of the dashboard can click on the link and access more details.

Examples of Custom fields used in this example:
- Custom-LastDBUpdateDate: Date when details of an activity were updated last
- Custom-Team: owner team e.g. eCommerce, Marketing, Services
- Custom-Category: experiment, personalisation or monitoring
- Custom-ConfluenceLink: Link to the Confluence page with further details of the activity
- Custom-IsClearWinner: a flag (Yes/No/TBC) whether the activity had a winning experience


### <a name="step3"></a> Step 3. Create a Google Service Account

Follow [steps to create a Google Service Account](https://github.com/pierian-co/custom-cxo-activity-dashboard-adobe-target-googlesheets/blob/main/create_googleserviceaccount.md). 

### <a name="step4"></a> Step 4. Share GoogleSheets with Google Service Account

For read and update operations, both GoogleSheets must be given access to the Service Account Client email address.

a. Copy client-email address from the JSON file downloaded while creating Google Service Account in Step 3 above.

b. For both GoogleSheets (Credentials and ActivitiesData), click on Share button. Paste and select the client-email address.

![Share GoogleSheets with Google Service Account](https://user-images.githubusercontent.com/71815964/104570760-3b74a180-564a-11eb-97ae-899c8aebaaa9.png)

c. Make sure to provide Editor access to the client-email.
![Share GoogleSheets with Google Service Account Editor Access](https://user-images.githubusercontent.com/71815964/104573412-c3f44180-564c-11eb-81ce-c528fa7eb422.png)

### <a name="step5"></a> Step 5. Execute the Python code

a. Python code when executed first, updates the ActivitiesData GoogleSheet with activities-details from Adobe Target's [Activities-List API] (https://developers.adobetarget.com/api/#list-activities).

b. You can update the ActivitiesData sheet with data for custom-fields.

c. On subsequent runs, Python code
- adds new activities to the bottom of the sheet (ones that don't exist already)
- updates existing activities

### <a name="step6"></a> Step 6. Schedule Python code to run recurrently

The steps we have taken so far would not be very beneficial until code is executed recurrently in automated way. For this I have used Google Cloud Platform however all enterprise Cloud platforms provide this capability.

For GCP, I have used Cloud Functions to deploy Python script on cloud, Cloud Scheduler to run a job recurrently and Pub-Sub to act as mediator between Functions and Scheduler.

Here are [detailed steps on scheduling Python script using GCP](https://github.com/pierian-co/execute-python-script-recurrently-gcp)

You'd need four files:
1. main.py - Python script
2. requirements.txt - To declare dependencies
3. Service Account JSON - The JSON file downloaded as part of [Step 3](#step3)
4. Adobe IO Project Private key - Private key for generating JWT, downloaded as part of [Step 1](#step1)

### <a name="step7"></a> Step 7. Visualise data using Google Data Studio

Google Data Studio has in-built connector to Google Sheets which makes visualisation much easier.

### <a name="step8"></a> Step 8. Share the ActivitiesData GoogleSheet and Data Studio Visualisation

Now you have the data in GoogleSheets and Data Studio, you can share it further with other colleagues.
