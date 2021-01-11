# Create a new Adobe IO Project with Adobe Target API

These are instructions to create a new Adobe IO Project and enable Adobe Target API. This project can then be used to extract list of activities, their details, reporting as well as Admin actions. Please check http://developers.adobetarget.com/api/#introduction for details of possible actions.

**Step 1: Login to Adobe IO** 
Login to Adobe IO Console website https://console.adobe.io/home using your Adobe credentials.

**Step 2: Create a new Adobe IO Project** 
Click on Create New Project link on the Adobe IO Console Homepage.
![new adobe io project create](https://user-images.githubusercontent.com/71815964/104186769-ce28fc80-540e-11eb-89b9-08450f3f8bc4.png)

**Step 3: Edit Project details** 
Click on Edit Project link on top-right to enter name of the project and description
![new adobe io project edit details](https://user-images.githubusercontent.com/71815964/104181647-16442100-5407-11eb-9e04-f539ab2045de.png)

**Step 4: Add Target API** 
Click on Add API. Select Adobe Target and click on Next.
![new adobe io project add api](https://user-images.githubusercontent.com/71815964/104189925-4396cc00-5413-11eb-9c00-1798ed6281a8.png)

![new adobe io project add target api](https://user-images.githubusercontent.com/71815964/104190229-b43de880-5413-11eb-8f03-fa62000641d4.png)

**Step 5 - Generate JWT credential** 
Adobe IO uses JSON Web Token (JWT) for secure connection using REST APIs. JWT requires public-private keypair for establishing secure connection. You can use Adobe IO to generate this keypair (Option 1) or use your own pair (Option 2). I have used the easiest option to use Adobe IO in this example.
Select Option 1 and click Generate keypair button.
![new adobe io project generate jwt credentials](https://user-images.githubusercontent.com/71815964/104190415-fb2bde00-5413-11eb-93d8-bd48190f6c0d.png)

**Step 6 - Save JWT keypair**
Adobe generates a keypair and downloads it on your local machine. Rename and save these files. We will use the private key file in Python to connect to this Adobe IO.
![new adobe io project save keypair](https://user-images.githubusercontent.com/71815964/104190504-1b5b9d00-5414-11eb-95f8-756d0abd8626.png)

**Step 7 - Generate Access token**
Test the keypair downloaded in the previous step to generate Access token by copying the content of the private key and clicking on Generate Token button. 
![new adobe io project generate access token1](https://user-images.githubusercontent.com/71815964/104192644-02a0b680-5417-11eb-8fdb-d3a9ef955ae5.png)

![new adobe io project generate access token2](https://user-images.githubusercontent.com/71815964/104192671-0e8c7880-5417-11eb-8cce-5e1922892c4f.png)

**Step 8 - Copy Project Credentials**
Click on Project Overview and click on Service Account (JWT) card under Credentials. You would need these credentials to generate Access Token in your Python code later.
![new adobe io project generate access token2](https://user-images.githubusercontent.com/71815964/104194628-780d8680-5419-11eb-819d-67ceaa20791c.png)

