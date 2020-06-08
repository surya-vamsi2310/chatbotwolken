from requests.auth import HTTPBasicAuth
import requests
import json


def login():
    login_url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/login/authenticate"

    res = requests.get(login_url, auth=HTTPBasicAuth('extuse', 'wSOylMKaeTNekc1'))

    print(res.json())

    response_token = res.json()['token']

    return response_token


def create_request(input_json):
    print(input_json)

    # fill json details from input_json below to create the request

    response_token = login()
    request_url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/generic/create_request_generic"

    # Note: Wrong input from Documentation: Content-Type
    headers = {"userPsNo": "poornima@wolkensoftware.com", "wolken_token": response_token, "Content-Type": "application/json"}
    
    data = {"requestMasterVO": {"sourceId": 6, "requestDesc": "Test", "requestedEmail": input_json['emailID']}, "descDetailsVO": {"descLarge": "test"}, "userDetails": {"userFname": "testFName", "userLname": "testLname"}}
    res11 = requests.post(url=request_url, data=json.dumps(data), headers=headers)
    print(res11.json())
    return res11.json()
   
# for getting detial, use get case details or use get_all_requesy, check with client once, which to su

def get_all_request(email_id):
    response_token = login()
    all_request_url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/get_all_request"

    # Note: Wrong input from Documentation: Content-Type
    headers = {"userEmail": email_id, "wolken_token": response_token, "Content-Type": "application/json"}

    data = {"myRequestDtlCondition": "3"}

    all_request_res = requests.post(url=all_request_url, data=json.dumps(data), headers=headers)
    return all_request_res.json()


def get_case_details(email_id):
    response_token = login()
    url = "https://api-wolken-demo.wolkenservicedesk.com/lur/external/specific_request_details?requestId=1470&sections=REQUEST_MASTER"

    headers = {"userPsNo": email_id, "wolken_token": response_token}

    case_res = requests.get(url=url, headers=headers)

    return case_res.json()
