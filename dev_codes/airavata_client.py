"""
    airavata_client.py
        --- API helper for Airavata Python Client

    reference:
        Apache Airavata API: http://airavata.readthedocs.io/en/latest/AiravataApi/
"""

from apache.airavata.api import Airavata
from apache.airavata.api.ttypes import *
from apache.airavata.model.experiment.ttypes import *
from apache.airavata.model.workspace.ttypes import *
from apache.airavata.model.experiment.ttypes import *
from apache.airavata.model.application.io.ttypes import *
from apache.airavata.model.security.ttypes import AuthzToken

import requests

from thrift import Thrift
from thrift.transport import TSSLSocket
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import configparser

import sys, os, json


class AiravataClient():
    """
    Airavata Client 
    """

    def __init__(self, configfile = ""):

        self.configfile = configfile
        self.authztoken = ""
        self.username = ""
        self.gatewayid = ""

        if configfile != "":
            self.initwithconfigfile(configfile)
        else:
            print("Empty client created! pleae use initwithconfigfile!")

    def __get_authz_token(self, accessTokenURL, userInfoURL, clientKey, clientSecret, username, password, gatewayID):
    
        request_data = {'grant_type': 'password', 'scope': 'openid', 'username': username, 'password': password}
        access_token_req = requests.post(accessTokenURL, auth=(clientKey, clientSecret), data=request_data, verify=False)
        access_token = access_token_req.json()['access_token']
        user_info_req = requests.get(userInfoURL, headers={'Authorization': "Bearer " + access_token}, verify=False)
    
        return AuthzToken(accessToken=access_token, claimsMap={'gatewayID': gatewayID, 'userName': user_info_req.json()['sub']})


    def initwithconfigfile(self, configfile):
   
        self.configfile = os.path.expanduser(configfile)
        config = configparser.ConfigParser()

        config.read(self.configfile)
        
        accessTokenURL = config['identity-server']['AccessTokenURL']
        userInfoURL = config['identity-server']['UserInfoURL']
        clientKey = config['identity-server']['ClientKey']
        clientSecret = config['identity-server']['ClientSecret']
        tenantDomain = config['identity-server']['TenantDomain']
        
        username = config['credentials']['Username']
        password = config['credentials']['Password']
        gatewayID = config['credentials']['GatewayID']
    
        self.authztoken = self.__get_authz_token(accessTokenURL, userInfoURL, clientKey, clientSecret, username + "@" + tenantDomain, password, gatewayID)
        self.gatewayid = self.authztoken.claimsMap['gatewayID']
        self.username =  self.authztoken.claimsMap['userName']

        print(self.username + " has been authoried to access " + self.gatewayid)

        return 



