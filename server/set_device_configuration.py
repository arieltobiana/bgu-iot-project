import base64, datetime, json, googleapiclient, jwt, requests
from google.oauth2 import service_account
from googleapiclient import discovery
from config import *
import requests, math


def get_client():
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
        service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
        discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials)


def get_temp():
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?units=metric&q=Lehavim&APPID={}'.format(api_key))
    temp = r.json()['main']['temp']
    return temp


def analyze_temp(lehavim_temp,device_temp):
    temp_dist = lehavim_temp - device_temp
    if math.fabs(temp_dist) < 1.5:
        # return 0 if temp close
        return 0
    if temp_dist > 0:
        # return 5,6,7,8 if HOT
        if temp_dist < 3:
            return  5
        elif temp_dist < 5:
            return 6
        elif temp_dist < 8:
            return 7
        else:
            return 8
    else:
        # return 1,2,3,4 if Cold
        temp_dist *= (-1)
        if temp_dist < 3:
            return  1
        elif temp_dist < 5:
            return 2
        elif temp_dist < 8:
            return 3
        else:
            return 4


def set_config(event):
    real_temp = get_temp()
    config = analyze_temp(event['temp'], real_temp)
    print 'temp from device:{}, temp in Lehavim:{}, config:{}'.format(event['temp'],real_temp,config)
    body = {"versionToUpdate": "0", "binaryData": base64.urlsafe_b64encode(str(config))}
    get_client().projects().locations().registries().devices().modifyCloudToDeviceConfig(name=device_name,body=body).execute()