
# Custom Sharable CXO Activity Tracker using Adobe Target and GoogleSheets

**Digital Marketing Problem:** While Adobe Target Activities page provides list of activities with information such as Activiy-Name and Last Update Date, we wanted to extend it
1. to add custom meta-data to each activity for more filtering criteria e.g. which team owns the activity or whether its an experimentation/personalisation activity
2. to be able to filter/sort activities on fields that are not available on Activities List page. One of the most important one is Priority - makes life much easier to see all the activities that have priorities higher than a specific limit 
3. to easily share this activity-dashboard with other team-members who may not be active Adobe Target users
 
## Prerequisites
- Access to Adobe Target and profiles you want to report on
- Developer access to Adobe Target product
- 

## Technologies used
- Adobe IO
- GoogleSheets API
- Python


## High-level Steps:
1. Create an Adobe IO Project with Adobe Target services
2. Create GoogleSheets
3. Create Google Service Account and enable GoogleSheets and GoogleDrive APIs
4. Python code to read activities from Adobe Target using Adobe IO and update Googlesheet


### <a name="step1"></a> Step 1. Create an Adobe IO Project with Adobe Target services
Follow the instructions [here](https://github.com/pierian-co/custom-cxo-activity-dashboard-adobe-target-googlesheets/blob/main/create_adobeioproject_target.md) on to create an Adobe IO Project.

### Step 2. Create GoogleSheets
I have used 2 separate GoogleSheets - one to store Credentials to connect to Adobe IO and another to store details of Adobe Target activities. This way we need not worry about Credentials being shared further - only activity data is shared with the recipients. 

**1. Credentials Googlesheet** 
This Googlesheet contains credentails of the Adobe IO project created on Step 1 above. Here's the [template of Credentials sheet](https://docs.google.com/spreadsheets/d/1nkF3EE3WL0UGhtFFFxjhG1OkDKyGSIBuW6Fd3kcmJa4/edit?usp=sharing)

Fields in Credentials sheet
- Tenant: Adobe Target tenant (you can find it in the URL when you select Adobe Target from Adobe Experience Cloud Console)
- Target Client Code: Get this under Account details section of Adobe Target console by navigating to Administration > Implementation 
- X-Api-Key: Client ID from your Adobe IO Project's Credentential page
- Client-Secret: Get it by clicking on Retrieve client secret button on your Adobe IO Project's Credentential page
- Adobe-Org-Id: Organization Id from your Adobe IO Project's Credentential page
- Tech-Account_Id: Technical Account ID from your Adobe IO Project's Credentential page
- Private-Key-Path: local path of Private Key generated when Adobe IO Project was created (refer to Step 1 details)

**2. Activities Googlesheet**
Activities Googlesheet contains data related to Adobe Target activities. Template of the sheet can be found here. 

Create a GoogleSheet using the template shown in the link below. 
https://docs.google.com/spreadsheets/d/1K65VKRYWOJHvLqi5sXBnqX46iR7y9EprtI_glbtAcs4/edit?usp=sharing



### Step 3. Create a Google Service Account
