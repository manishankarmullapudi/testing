from distutils.command.config import config
from unittest import result
import yaml
import requests
import json
from datetime import date
from datetime import datetime as dt
import subprocess
from requests_toolbelt import MultipartEncoder
from pathlib import Path
import os
import glob

def dd_debug():
    global DD_URL
    DD_URL='http://127.0.0.1:8000'
    global dd_username
    dd_username='admin'
    global dd_password
    dd_password='t54xNVjDyXNC0EZfVTuA9f'
    global DD_TOKEN
    DD_TOKEN=auth()
    global DD_PRODUCT_NAME
    DD_PRODUCT_NAME='Debug'
    global DD_PROD_DESC
    DD_PROD_DESC='Dev debug Product'
    global SONAR_PROJECT_KEY
    SONAR_PROJECT_KEY='Hello App'
    global SONAR_USERNAME
    SONAR_USERNAME='admin'
    global SONAR_PASSWORD
    SONAR_PASSWORD='admin'
    global SONAR_URL
    SONAR_URL='http://127.0.0.1:9000'
    global DD_SCANTYPE
    DD_SCANTYPE="SonarQube API Import"
    global ENG_NAME
    ENG_NAME='Test Engagement'
    global config_id
    config_id=0

def dd_setup():
    DD_IP = os.environ['dd_ip']
    global DD_URL
    DD_URL='http://'+DD_IP+':8000'

    global dd_username
    dd_username=os.environ['dd_username']
    
    global dd_password
    dd_password=os.environ['dd_password']

    global DD_TOKEN
    DD_TOKEN=auth()

    global DD_PRODUCT_NAME
    DD_PRODUCT_NAME=os.environ['dd_product_name']

    global DD_PROD_DESC
    DD_PROD_DESC=os.environ['dd_product_desc']
    
    global SONAR_PROJECT_KEY
    SONAR_PROJECT_KEY=os.environ['sonar_project_key']

    global SONAR_USERNAME
    SONAR_USERNAME=os.environ['sonar_username']

    global SONAR_PASSWORD
    SONAR_PASSWORD=os.environ['sonar_password']

    global SONAR_URL
    SONAR_URL=os.environ['sonar_url']
    
    global DD_SCANTYPE
    DD_SCANTYPE="SonarQube API Import"

    global ENG_NAME
    ENG_NAME=os.environ['pipeline_no']
    print(ENG_NAME)

    global config_id
    config_id=0

def auth():
    creds={
        'username' : dd_username,
        'password' : dd_password
    }
    r = requests.post(DD_URL+'/api/v2/api-token-auth/',
    data=json.dumps(creds),headers={'Content-Type': 'application/json'} )
    return r.content.decode('UTF-8').split('"')[3]

def get_prod_id():
    r=requests.get(DD_URL+'/api/v2/products', headers={'Authorization': 'Token '+DD_TOKEN})
    for i in r.json()['results']:
        if i['name']==DD_PRODUCT_NAME:
            return i['id']
    return None

def get_eng_id():
    r=requests.get(DD_URL+'/api/v2/engagements', headers={'Authorization': 'Token '+DD_TOKEN})
    for i in r.json()['results']:
        if i['name']==ENG_NAME:
            return i['id']
    return None


def create_prod():
    today = date.today()
    t_date=today.strftime('%Y-%m-%d')
    fields={
    'name': DD_PRODUCT_NAME,
    'product_name': DD_PRODUCT_NAME,
    'prod_type':'1',
    'description': DD_PROD_DESC
    }
    r = requests.post(DD_URL+'/api/v2/products/',
    data=json.dumps(fields),headers={'Content-Type': 'application/json',
    'Authorization': 'Token '+DD_TOKEN} )
    return r.json()['id']

def create_eng():
    today = date.today()
    t_date=today.strftime('%Y-%m-%d')
    fields={
    'name': ENG_NAME,
    'product':str(get_prod_id()),
    'engagement_type':'CI/CD',
    'target_start': str(t_date),
    'prod_type':'1',
    'target_end': str(t_date),
    'description': 'Pipeline no: ' + ENG_NAME + ' Scans'
    }
    r = requests.post(DD_URL+'/api/v2/engagements/',
    data=json.dumps(fields),headers={'Content-Type': 'application/json',
    'Authorization': 'Token '+DD_TOKEN} )


def upload_scan():
    
    mp_encoder = MultipartEncoder(
    fields={
        'scan_type': DD_SCANTYPE,
        'product_name':DD_PRODUCT_NAME,
        'engagement_name': ENG_NAME,
        'name': ENG_NAME,
        'engagement': str(get_eng_id()),
        }
    )
    r = requests.post(DD_URL+'/api/v2/import-scan/',
        data=mp_encoder,headers={'Content-Type': mp_encoder.content_type,
        'Authorization': 'Token '+DD_TOKEN} )

def tool_config():
    fields_data={
        "name": "SonarQube Integration",
        "description": "SonarQube Integration for DefectDojo",
        "url": SONAR_URL,
        "authentication_type": "Password",
        "username": SONAR_USERNAME,
        "password": SONAR_PASSWORD,
        "tool_type": 1
    }
    r = requests.post(DD_URL+'/api/v2/tool_configurations/',
    data=json.dumps(fields_data),headers={'Content-Type': 'application/json',
    'Authorization': 'Token '+DD_TOKEN} )
    return r.json()['id']

def check_tool_config():
    r = requests.get(DD_URL+'/api/v2/tool_configurations/',
    headers={'Content-Type': 'application/json',
    'Authorization': 'Token '+DD_TOKEN} )
    for i in r.json()['results']:
        if(i['name']=="SonarQube Integration"):
            return i['id']
        else:
            return 0

def api_scan_config():
    fields_data={
        "service_key_1": SONAR_PROJECT_KEY,
        "product": get_prod_id(),
        "tool_configuration": config_id
    }
    r = requests.post(DD_URL+'/api/v2/product_api_scan_configurations/',
    data=json.dumps(fields_data),headers={'Content-Type': 'application/json',
    'Authorization': 'Token '+DD_TOKEN} )

def check_api_scan_config():
    r = requests.get(DD_URL+'/api/v2/product_api_scan_configurations/',
    headers={'Content-Type': 'application/json',
    'Authorization': 'Token '+DD_TOKEN} )
    for i in r.json()['results']:
        if(i['product']==get_prod_id() and i['tool_configuration']==check_tool_config()):
            return 1
        else:
            return 0

if __name__=="__main__":
    dd_setup()
    # dd_debug()
    if(get_prod_id()):
        print('Product Already Exists')
    else:
        create_prod()
    
    if(get_eng_id()):
        print('Engagement already Exists')
    else:
        create_eng()
    
    # config_id=tool_config()
    # print(config_id)
    
    if(check_tool_config()):
        print('Tool already configured')
    else:
        global config_id
        config_id=tool_config()
    
    if(check_api_scan_config()):
        print('API scan configurations already made')
    else:
        api_scan_config()
    
    upload_scan()
