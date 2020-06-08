from requests.auth import HTTPBasicAuth
import requests
import json

####################################### 1. login module ##########################################
login_url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/login/authenticate"

res = requests.get(login_url, auth=HTTPBasicAuth('extuse', 'wSOylMKaeTNekc1'))

print(res.json())

response_token = res.json()['token']

###################################### 2. Create Request #########################################
request_url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/generic/create_request_generic"

# Note: Wrong input from Documentation: Content-Type
headers = {"userPsNo": "poornima@wolkensoftware.com", "wolken_token": response_token, "Content-Type": "application/json"}

data = {"requestMasterVO": {"sourceId": 6, "requestDesc": "Test", "requestedEmail": "testFandLName@gmail.com"}, "descDetailsVO": {"descLarge": "test"}, "userDetails": {"userFname": "testFName", "userLname": "testLname"}}

res11 = requests.post(url=request_url, data=json.dumps(data), headers=headers)
print(res11.json())

##################################### 3. Update Request ###########################################
update_request_url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/generic/update_request"

# Note: Wrong input from Documentation: Content-Type
headers = {"userPsNo": "poornima@wolkensoftware.com", "wolken_token": response_token, "Content-Type": "application/json"}

data = {"requestId": 1513602290, "threadVO": {"resDesc": "Test"}, "otherInfoVO": {"milestoneId": 5}}

all_request_res = requests.post(url=update_request_url, data=json.dumps(data), headers=headers)
print(all_request_res.json())

#################################### 4. Get All Request #########################################
all_request_url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/get_all_request"

# Note: Wrong input from Documentation: Content-Type
headers = {"userPsNo": "preetham@wolkensoftware.com", "wolken_token": response_token, "Content-Type": "application/json"}

data = {"myRequestDtlCondition": "3"}

all_request_res = requests.post(url=all_request_url, data=json.dumps(data), headers=headers)
print(all_request_res.json())

#################################### 5. Get Case Details #########################################
url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/specific_request_details?requestId=1470&sections=REQUEST_MASTER"

headers = {"userPsNo": "preetham@wolkensoftware.com", "wolken_token": response_token}

case_res = requests.get(url=url, headers=headers)

print(case_res.json())

#################################### 6. Close Request #########################################

close_request_url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/generic/update_request"

# Note: Wrong input from Documentation: Content-Type
headers = {"userPsNo": "poornima@wolkensoftware.com", "wolken_token": response_token, "Content-Type": "application/json"}

data = {"requestId": 1513602290, "threadVO": {"resDesc": "Test"}, "otherInfoVO": {"milestoneId": 7}}

# Note: Wrong input from Documentation: Method
close_res = requests.get(url=url, headers=headers, data = json.dumps(data))

print(close_res.json())
