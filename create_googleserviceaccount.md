# Create Google Service Account to access and update GoogleSheets

To read and update data in GoogleSheets using Python requires creating a Google Service Account. Here are steps:

## High level steps

1. Create a project in Google Developer Console

2. Enable GoogleSheets API

3. Enable GoogleDrive API

4. Create Credentials for the project

5.  Copy Service Account client-email address

> NOTE: GoogleSheets API is free to use but there are usage limits. Please refer to https://developers.google.com/sheets/api/limits for more details.

## Detailed steps

**Step 1 Create a project**

a. Open [Google Developer Console](https://console.developers.google.com/). 

b. Click on Create Project link and provide a name to this project.

![create Google Service Account add project](https://user-images.githubusercontent.com/71815964/104507254-60332f80-55de-11eb-91db-4eda253c44ab.png)

![create Google Service Account name project](https://user-images.githubusercontent.com/71815964/104579808-5d732180-5654-11eb-8deb-0fcbe95dbea0.png)


**Step 2 Enable GoogleSheets API**

a. Click on API Library link under API & Services of newly created project. 

b. Search Google Sheet in the search box. 

c. Select Google Sheets API from the search results and click on Enable button to add to the project.

![create Google Service Account api library](https://user-images.githubusercontent.com/71815964/104508318-f61b8a00-55df-11eb-8f26-2b97be570c23.png)

![create Google Service Account search api](https://user-images.githubusercontent.com/71815964/104508315-f4ea5d00-55df-11eb-963e-00ba0f1828dd.png)

![create Google Service Account select Googlesheet](https://user-images.githubusercontent.com/71815964/104508309-f3b93000-55df-11eb-8f34-4440eb29f046.png)


**Step 3 Enable Google Drive API**

Similarly search for *Google Drive* API and enable it.


**Step 4 Create Credentials**

a. Click on Create Credentials button.

![create Google Service Account create credentails](https://user-images.githubusercontent.com/71815964/104512039-84463f00-55e5-11eb-8426-f25d56222b2b.png)

b. Select following options on Credentials screen:
- Where will you be calling the API from?  *Other non-UI (e.g. cron job, daemon)*
- What data will you be accessing? *Application data*
- Are you planning to use this API with App Engine or Compute Engine? *No, I’m not using them*

![create Google Service Account create credentials options](https://user-images.githubusercontent.com/71815964/104512035-83ada880-55e5-11eb-808b-5fa722b3ddc0.png)

c. Give a name to your Service Account. 

d. Select *Project > Owner* from Role dropdown. 

e. Select *JSON* as Key type.

![create Google Service Account service account name](https://user-images.githubusercontent.com/71815964/104512028-801a2180-55e5-11eb-8f63-6125170aa78f.png)

f. Clicking Continue buttons downloads a JSON file which contains key to access GoogleSheets API.

**Step 5 Copy Service Account Client Email address**

In order to update a GoogleSheet, that sheet must be shared with the Service Account created above. This is done by sharing the sheet with Service Account's email-address. Search for *client_email* in the JSON file downloaded in the step above. Client email address should like below:

![create Google Service Account copy client email](https://user-images.githubusercontent.com/71815964/104516470-4698e480-55ec-11eb-8dc1-4f3ae12f888f.png)
