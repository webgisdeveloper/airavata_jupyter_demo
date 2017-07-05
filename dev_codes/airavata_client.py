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
        self.apiserverhostname = ""
        self.apiserverport = ""

        self.transport = ""
        self.apiclient = ""

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

    def __get_transport(self):
        # Create a socket to the Airavata Server
        transport = TSSLSocket.TSSLSocket(self.apiserverhostname, self.apiserverport, validate=False)

        # Use Buffered Protocol to speedup over raw sockets
        self.transport = TTransport.TBufferedTransport(transport)
    
    def __get_apiserverclient(self):

        # Airavata currently uses Binary Protocol
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        # Create a Airavata client to use the protocol encoder
        self.apiclient = Airavata.Client(protocol)


    def __open_connection(self):

        self.transport.open()

    def __close_connection(self):

        self.transport.close()

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

        print(self.username + " has been authorized to access " + self.gatewayid)

        self.apiserverhostname = config['airavata-api-server']['Hostname']
        self.apiserverport = config['airavata-api-server']['Port']

        self.__get_transport()
        self.__get_apiserverclient()

    def getprojects(self):
        """get all or partial project list"""

        self.__open_connection()

        projectlists = self.apiclient.getUserProjects(self.authztoken, self.gatewayid, self.username, -1, 0)

        self.__close_connection()

        return projectlists

    def createproject(self, projectname="", projectdescription=""):

        self.__open_connection()

        projectobject = Project()
        projectobject.owner = self.username
        projectobject.gatewayId = self.gatewayid
        projectobject.name = projectname
        projectobject.description = projectdescription
        status = self.apiclient.createProject(self.authztoken, self.gatewayid, projectobject)

        if status:
            print("Successed to create the project: " + projectname)
        else:
            print("Failed to create the project: " + projectname)

        self.__close_connection()

    def deleteproject(self,projectid=""):

        self.__open_connection()

        status = self.apiclient.deleteProject(self.authztoken, projectid)

        if status:
            print("Successed to delete the project: " + projectid)
        else:
            print("Failed to delete the project: " + projectid)

        self.__close_connection()


    def isnotebook(self):
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                return True   # Jupyter notebook or qtconsole
            elif shell == 'TerminalInteractiveShell':
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False      # Probably standard Python interpreter


