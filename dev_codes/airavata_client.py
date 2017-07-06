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
from apache.airavata.model.data.replica.ttypes import *
from apache.airavata.model.scheduling.ttypes import *
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

    def getapplications(self, module=""):
        """get all or partial project list"""

        self.__open_connection()

        applists = self.apiclient.getAllApplicationDeployments(self.authztoken, self.gatewayid)

        self.__close_connection()

        if module == "":
            return applists
        else:    
            applists_flitered = []
            for item in applists:
                if module.lower() in item.appModuleId.lower():
                    applists_flitered.append([item.appModuleId,item.appDeploymentId,item.computeHostId])
            return applists_flitered
 
    def registerinputfile(self, dataproduct):

        self.__open_connection()

        uri = self.apiclient.registerDataProduct(self.authztoken, dataproduct)
        
        self.__close_connection()

        return uri

    def createexperiment(self, experiment):

        self.__open_connection()

        experimentid = self.apiclient.createExperiment(self.authztoken, self.gatewayid, experiment)
        
        self.__close_connection()

        return experimentid


    def launchexperiment(self,experimentid):

        self.__open_connection()

        status = self.apiclient.validateExperiment(self.authztoken, experimentid)

        if status:
            self.apiclient.launchExperiment(self.authztoken, experimentid, self.gatewayid)
        else:
            print("Not validated: ", experimentid)
        
        self.__close_connection()

    def getexperimentstatus(self,experimentid):
        
        self.__open_connection()

        #ExperimentStatus
        experimentstatus = self.apiclient.getExperimentStatus(self.authztoken, experimentid)

        self.__close_connection()

        return experimentstatus

    def sampleexperiment(self):
        """define a simple Gaussion application"""

        experiment = ExperimentModel()
    
        # skip experiment.experimentId
        # use default project for the testing
        projectname = "DefaultProject"
        experiment.projectId = "DefaultProject_01720113-3d7c-4020-ba83-2c977ae5c3ba"
        experiment.gatewayId = self.gatewayid
        experiment.experimentType = ExperimentType.SINGLE_APPLICATION
        experiment.userName = self.username
        experiment.experimentName = "GaussianTestJob01"
        experiment.description = "Gaussian Test Job 01"

        # register input file
        gefile = DataProductModel()
        gefile.gatewayId = self.gatewayid
        gefile.ownerName = self.username
        gefile.productName = "Gaussian.com"
        gefile.dataProductType = DataProductType.FILE

        gest = DataReplicaLocationModel()
        gest.storageResourceId = "156.56.177.220_aac7149e-d642-4849-9c2a-020c8af8419e"
        gest.replicaName = "Gaussian.com"
        gest.replicaLocationCategory = ReplicaLocationCategory.GATEWAY_DATA_STORE 
        gest.replicaPersistentType = ReplicaPersistentType.TRANSIENT
        storagehost = "156.56.177.220"
        gest.filePath = "file://" + storagehost + ":" + self.username + "/" + projectname + "/" + experiment.experimentName + "/Gaussian.com"

        gefile.replicaLocations = [gest]

        #uri = self.registerinputfile(gefile)
        uri = "airavata-dp://57f9fb47-c09e-4421-8a3c-8f8a1bd5a771"
        inputobj = InputDataObjectType()
        inputobj.name = "Gaussian.com"
        inputobj.type = DataType.URI
        inputobj.value = uri
        
        experiment.experimentInputs = [inputobj]
        # appModuleId ='Gaussian_57eb2905-1cd8-400e-ad40-cadfba8f434f'
        # computeHostId = 'comet.sdsc.edu_91b900df-0ee0-4909-89b3-98e8f64e1969'
        # appDeploymentId = 'comet.sdsc.edu_Gaussian_57eb2905-1cd8-400e-ad40-cadfba8f434f'
        experiment.excutionId = 'comet.sdsc.edu_Gaussian_57eb2905-1cd8-400e-ad40-cadfba8f434f'

        # schedule reosurce
        ucdm = UserConfigurationDataModel()
        crsm = ComputationalResourceSchedulingModel()
        crsm.resourceHostId = 'comet.sdsc.edu_91b900df-0ee0-4909-89b3-98e8f64e1969'
        # queue = shared node=1 corecount=4 walltimelimit = 30
        crsm.totalCPUCount = 4
        crsm.nodeCount = 1
        crsm.wallTimeLimit = 30
        queueName = "shared"
        ucdm.computationalResourceScheduling = crsm

        experiment.userConfigurationData = ucdm

        return experiment

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



