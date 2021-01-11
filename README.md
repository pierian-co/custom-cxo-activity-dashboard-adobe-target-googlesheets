
# Custom Sharable CXO Activity Tracker using Adobe Target and GoogleSheets

**Digital Marketing Problem:** While Adobe Target Activities page provides list of activities with information such as Activiy-Name and Last Update Date, we wanted to extend it
1. to add custom meta-data to each activity for more filtering criteria e.g. which team owns the activity or whether its an experimentation/personalisation activity
2. to be able to filter/sort activities on fields that are not available on Activities List page. One of the most important one is Priority - makes life much easier to see all the activities that have priorities higher than a specific limit 
3. to easily share this activity-data with other team-members who may not be active Adobe Target users
 
# Technologies used
- Adobe IO
- GoogleSheets API
- Python

# High-level Steps:
1. Create an Adobe IO Project with Adobe Target services
2. Create GoogleSheets
3. Create Google Service Account and Enable required APIs
4. Python code to read activities from Adobe Target using Adobe IO and update Googlesheet


**Step 1. Create an Adobe IO Project with Adobe Target services**
A. Follow the instructions on https://helpx.adobe.com/uk/marketing-cloud-core/kb/adobe-io-authentication-step-by-step.html to create an Adobe IO Project.



Create a GoogleSheet

Create a GoogleSheet using the template shown in the link below. 
https://docs.google.com/spreadsheets/d/1K65VKRYWOJHvLqi5sXBnqX46iR7y9EprtI_glbtAcs4/edit?usp=sharing

This GoogleSheet contains 2 Sheets

A. Activities: This sheet is where all the activities related data goes. First 10 columns are populated using the Adobe Target IO API https://developers.adobetarget.com/api/#list-activities. 
Column lastUpdateDate is when GoogleSheet was populated with activity-data.
You can add additional columns for adding other metadata for activities. For example, I have added:
Custom-Activity-Team: Here add name of the team that owns the activity e.g. eCommerce, Service, Marketing
Custom-Activity-Type:

B. Config: This sheet contains details of Adobe IO Project from Step 1. These details will be used by the Python code to connect to Adobe Target.
Tenant:
Target Client Code:
X-API-Key:
Client-Secret:
Adobe-Org-Id:
Tech-Account_Id:
Private-Key-Path:	

2. Create a Google Service Account
