# Create a new Adobe IO Project with Adobe Target API

These are instructions to create a new Adobe IO Project and enable Adobe Target API. This project can then be used to extract list of activities, their details, reporting as well as Admin actions. Please check http://developers.adobetarget.com/api/#introduction for details of possible actions.

**Step 1: Login to Adobe IO** 
Login to Adobe IO Console website https://console.adobe.io/home using your Adobe credentials.

**Step 2: Create a new Adobe IO Project** 
Click on Create New Project link on the Adobe IO Console Homepage.
![new adobe io project create](https://user-images.githubusercontent.com/71815964/104339359-6696ae00-54ef-11eb-8154-df44ba35a497.png)

**Step 3: Edit Project details** 
Click on Edit Project link on top-right to enter name of the project and description
![new adobe io project edit details](https://user-images.githubusercontent.com/71815964/104339356-6696ae00-54ef-11eb-9d41-6cee0238e48a.png)

**Step 4: Add Target API** 
Click on Add API. Select Adobe Target and click on Next.
![new adobe io project add api](https://user-images.githubusercontent.com/71815964/104339354-6696ae00-54ef-11eb-91d5-701fbba48af7.png)
![new adobe io project add api](https://user-images.githubusercontent.com/71815964/104339352-65fe1780-54ef-11eb-8978-20b86d0fb8ff.png)

**Step 5 - Generate JWT credential** 
Adobe IO uses JSON Web Token (JWT) for secure connection using REST APIs. JWT requires public-private keypair for establishing secure connection. You can use Adobe IO to generate this keypair (Option 1) or use your own pair (Option 2). I have used the easiest option to use Adobe IO in this example.
Select Option 1 and click Generate keypair button.
![new adobe io project generate jwt credentials](https://user-images.githubusercontent.com/71815964/104339350-65658100-54ef-11eb-83c2-ffdab8b37f65.png)

**Step 6 - Save JWT keypair**
Adobe generates a keypair and downloads it on your local machine as a zip file with 2 files: certificate_pub.crt and private.key
Rename (if needed) and save these files. We will use the private key file in Python to connect to this Adobe IO.
![new adobe io project save keypair](https://user-images.githubusercontent.com/71815964/104339349-64ccea80-54ef-11eb-8382-37beca073e5f.png)

**Step 7 - Select Adobe Target profiles**
Select the Adobe Target profiles you want to report on. 
![new adobe io project select profiles](https://user-images.githubusercontent.com/71815964/104339346-64ccea80-54ef-11eb-9444-7008c4a4a626.png)

**Step 8 - Generate Access token**
Test the keypair downloaded in the previous step to generate Access token by copying the content of the private key and clicking on Generate Token button. 
![new adobe io project generate access token1](https://user-images.githubusercontent.com/71815964/104339345-64ccea80-54ef-11eb-9926-5e0f82f01ef7.png)

![new adobe io project generate access token2](https://user-images.githubusercontent.com/71815964/104339342-64345400-54ef-11eb-87f2-d41aa6f952ac.png)

**Step 9 - Access Project Credentials**
Click on Project Overview and click on Service Account (JWT) card under Credentials. You would need these credentials to generate Access Token in your Python code later.
![new adobe io project overview](https://user-images.githubusercontent.com/71815964/104339341-64345400-54ef-11eb-9f06-d3bf8be01d40.png)
![new adobe io project credentials](https://user-images.githubusercontent.com/71815964/104339337-639bbd80-54ef-11eb-8d29-68bb400cae7b.png)

