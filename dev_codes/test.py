
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



def get_transport(hostname, port):
    # Create a socket to the Airavata Server
    # TODO: validate server certificate
    transport = TSSLSocket.TSSLSocket(hostname, port, validate=False)

    # Use Buffered Protocol to speedup over raw sockets
    transport = TTransport.TBufferedTransport(transport)
    return transport

def get_airavata_client(transport):
    # Airavata currently uses Binary Protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a Airavata client to use the protocol encoder
    airavataClient = Airavata.Client(protocol)
    return airavataClient

def get_authz_token(accessTokenURL, userInfoURL, clientKey, clientSecret, username, password, gatewayID):
    
    request_data = {'grant_type': 'password', 'scope': 'openid', 'username': username, 'password': password}
    access_token_req = requests.post(accessTokenURL, auth=(clientKey, clientSecret), data=request_data, verify=False)
    access_token = access_token_req.json()['access_token']
    user_info_req = requests.get(userInfoURL, headers={'Authorization': "Bearer " + access_token}, verify=False)
    
    return AuthzToken(accessToken=access_token, claimsMap={'gatewayID': gatewayID, 'userName': user_info_req.json()['sub']})

def get_all_projects(airavataClient, authzToken, gatewayId, username):

    projectLists = airavataClient.getUserProjects(authzToken, gatewayId, username, -1, 0)

    return projectLists

def create_new_project(airavataClient, authzToken, gatewayID, username,projectname, projectdescription):

    projectobject = Project()
    projectobject.owner = username
    projectobject.gatewayId = gatewayID
    projectobject.name = projectname
    projectobject.description = projectdescription
    status = airavataClient.createProject(authzToken, gatewayID, projectobject)
    return status

def get_storageid_from_config():

    configfile = get_user_configfile()
    config = configparser.ConfigParser()
    config.read(configfile)
    storageid = config['storage']['StorageID']

    return storageid

def get_authz_token_from_config():
    
    configfile = get_user_configfile()
    config = configparser.ConfigParser()
    config.read(configfile)
    accessTokenURL = config['identity-server']['AccessTokenURL']
    userInfoURL = config['identity-server']['UserInfoURL']
    clientKey = config['identity-server']['ClientKey']
    clientSecret = config['identity-server']['ClientSecret']
    tenantDomain = config['identity-server']['TenantDomain']
    
    username = config['credentials']['Username']
    password = config['credentials']['Password']
    gatewayID = config['credentials']['GatewayID']
    authz_token = get_authz_token(accessTokenURL, userInfoURL, clientKey, clientSecret, username + "@" + tenantDomain, password, gatewayID)

    return authz_token

def get_airavata_client_from_config(configfile='airavata-client.ini'):
    configfile = get_user_configfile()
    config = configparser.ConfigParser()
    config.read(configfile)
    hostname = config['airavata-api-server']['Hostname']
    port = config['airavata-api-server']['Port']

    return [hostname,port]

def get_user_projects(authz_token):
    
    hostname, port = get_airavata_client_from_config()
    transport = get_transport(hostname, port)
    transport.open()
    airavataClient = get_airavata_client(transport)
    
    gatewayID = authz_token.claimsMap['gatewayID']
    username = authz_token.claimsMap['userName']
    projects = get_all_projects(airavataClient, authz_token, gatewayID, username)
    
    transport.close()

    return projects

def create_user_project(authz_token,projectname, projectdescription):

    hostname, port = get_airavata_client_from_config()
    transport = get_transport(hostname, port)
    transport.open()
    airavataClient = get_airavata_client(transport)
    
    gatewayID = authz_token.claimsMap['gatewayID']
    username = authz_token.claimsMap['userName']
    
    create_new_project(airavataClient, authz_token, gatewayID, username, projectname, projectdescription)

    transport.close()

    return "Successful!"

def delete_user_project(authz_token, projectID):

    hostname, port = get_airavata_client_from_config()
    transport = get_transport(hostname, port)
    transport.open()
    airavataClient = get_airavata_client(transport)
    
    #gatewayID = authz_token.claimsMap['gatewayID']
    #username = authz_token.claimsMap['userName']
    
    airavataClient.deleteProject(authz_token, projectID)
    
    transport.close()

    return "Successful!"

def get_user_configfile():
    """ get user configfile for the testing """

    userConfigfile  = os.path.expanduser("~/Projects/") + "airavata-client.ini"

    return userConfigfile

def test_run_gaussian_experiment(authz_token):

    # create sample experiment
    experiment = ExperimentModel()
    
    # skip experiment.experimentId
    # use default project for the testing
    projectname = "Default Project"
    experiment.projectId = "DefaultProject_01720113-3d7c-4020-ba83-2c977ae5c3ba"
    experiment.gatewayId = authz_token.claimsMap['gatewayID']
    experiment.experimentType = ExperimentType.SINGLE_APPLICATION
    experiment.userName = authz_token.claimsMap['userName']
    experiment.experimentName = "GaussianTestJob01"
    experiment.description = "Gaussian Test Job 01"
    # list of InputDataObjectType
    experiment.experimentInputs = ""

    # register input data
    # StoragePath = $user/$projectname/$experimentname
    # input path Gaussian.com
    inputfile = "Gaussian.com"
    inputdata = InputDataObjectType()
    inputdata.name = "gaussian"
    inputdata.type = DataType.URI
    inputdata.storageResourceId = get_storageid_from_config()
    inputdata.value = os.path.join(experiment.userName,projectname,experiment.experimentName,inputfile)
    print (inputdata)

def get_all_application(authz_token):

    gatewayID = authz_token.claimsMap['gatewayID']

    hostname, port = get_airavata_client_from_config()
    transport = get_transport(hostname, port)
    transport.open()
    airavataClient = get_airavata_client(transport)
    applications = airavataClient.getAllApplicationDeployments(authz_token,gatewayID)
    
    transport.close()

    return applications

    
if __name__ == '__main__':
    
    authztoken = get_authz_token_from_config()
    print(authztoken)
    
    projects = get_user_projects(authztoken)
    print(projects)
    
    applications = get_all_application(authztoken)
    print(applications)
    
    #testing experiment
    test_run_gaussian_experiment(authztoken)

    sys.exit(0)
    
