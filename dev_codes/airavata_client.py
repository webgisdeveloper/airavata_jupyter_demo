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

import sys, os, json, random


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

        self.storagehost = ""
        self.storageid = ""
        self.storageroot = ""

        if configfile != "":
            self.initwithconfigfile(configfile)
        else:
            print("Empty client created! pleae use initwithconfigfile!")

    def __get_authz_token(self, accessTokenURL, userInfoURL, clientKey, clientSecret, username, password, gatewayID):

        request_data = {'grant_type': 'password', 'scope': 'openid', 'username': username, 'password': password}
        access_token_req = requests.post(accessTokenURL, auth=(clientKey, clientSecret), data=request_data, verify=False)
        access_token_json = access_token_req.json()
        if 'access_token' not in access_token_json:
            raise Exception("Failed to get access_token: {}".format(access_token_json))
        access_token = access_token_json['access_token']
        user_info_req = requests.get(userInfoURL, headers={'Authorization': "Bearer " + access_token}, verify=False)

        username_claim = 'preferred_username'

        return AuthzToken(accessToken=access_token, claimsMap={'gatewayID': gatewayID, 'userName': user_info_req.json()[username_claim]})

   
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
    
        self.authztoken = self.__get_authz_token(accessTokenURL, userInfoURL, clientKey, clientSecret, username, password, gatewayID)
        self.gatewayid = self.authztoken.claimsMap['gatewayID']
        self.username =  self.authztoken.claimsMap['userName']

        print(self.username + " has been authorized to access " + self.gatewayid)

        self.apiserverhostname = config['airavata-api-server']['Hostname']
        self.apiserverport = config['airavata-api-server']['Port']

        self.__get_transport()
        self.__get_apiserverclient()

        # storage
        self.storagehost = config['storage']['StorageHost']
        self.storageid = config['storage']['StorageID']
        self.storageroot = config['storage']['StorageRoot']


    def getprojects(self, projectname = "", idonly=False):
        """get all or partial project list"""

        self.__open_connection()

        projectlist = self.apiclient.getUserProjects(self.authztoken, self.gatewayid, self.username, -1, 0)

        self.__close_connection()

        if projectname == '':
            return projectlist
        else:
            projectlist_filtered = []
            for item in projectlist:
                if projectname.lower() in item.name.lower():
                    if idonly:
                        projectlist_filtered.append(item.projectID)
                    else:
                        projectlist_filtered.append(item)
            return projectlist_filtered


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


    def getapplications(self, appname=""):
        """get all or partial project list"""

        self.__open_connection()

        applists = self.apiclient.getAllApplicationDeployments(self.authztoken, self.gatewayid)

        self.__close_connection()

        if appname == "":
            return applists
        else:    
            applists_flitered = []
            for item in applists:
                if appname.lower() in item.appModuleId.lower():
                    applists_flitered.append([item.appModuleId,item.appDeploymentId,item.computeHostId])
            return applists_flitered
    

    def getapplicationinterfaces(self,appname="",idonly=False):

        self.__open_connection()
        
        appinterfacelist = self.apiclient.getAllApplicationInterfaces(self.authztoken,self.gatewayid)
        
        self.__close_connection()

        if appname == "":
            return appinterfacelist
        else:
            appinterfacelist_filtered = []
            for item in appinterfacelist:
                if appname.lower() in item.applicationName.lower():
                    if idonly:
                        appinterfacelist_filtered.append(item.applicationInterfaceId)
                    else:
                        appinterfacelist_filtered.append(item)
                        
            return appinterfacelist_filtered

        return appinterfacelist            
    

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
            print("launch: ", experimentid)
            self.apiclient.launchExperiment(self.authztoken, experimentid, self.gatewayid)
        else:
            print("Not validated: ", experimentid)
        
        self.__close_connection()

  
    def getexperiments(self,experimentname='',idonly=False):

        self.__open_connection()

        experimentlist = self.apiclient.getUserExperiments(self.authztoken, self.gatewayid, self.username, -1, 0)

        self.__close_connection()

        if experimentname == "":
            return experimentlist
        else:
            experimentlist_filtered = []
            for item in experimentlist:
                if experimentname.lower() in item.experimentName.lower():
                    if idonly:
                        experimentlist_filtered.append(item.experimentId)
                    else:
                        experimentlist_filtered.append(item)
            return experimentlist_filtered


    def getexperimentbyid(self,experimentid):
        
        self.__open_connection()

        #experiment
        experiment = self.apiclient.getExperiment(self.authztoken, experimentid)

        self.__close_connection()

        return experiment

  
    def getexperimentstatus(self,experimentid):
        
        self.__open_connection()

        #ExperimentStatus
        experimentstatus = self.apiclient.getExperimentStatus(self.authztoken, experimentid)

        self.__close_connection()

        return experimentstatus

    
    def getexperimentoutputs(self,experimentid):
        
        self.__open_connection()

        #ExperimentStatus
        experimentoutputs = self.apiclient.getExperimentOutputs(self.authztoken, experimentid)

        self.__close_connection()

        return experimentoutputs


    def getstorages(self, storageid=""):

        self.__open_connection()

        if storageid == "":
            storagelist = self.apiclient.getAllStorageResourceNames(self.authztoken)
        else:
            storagelist = self.apiclient.getStorageResource(self.authztoken,storageid)

        self.__close_connection()

        return storagelist

    def sampleexperiment(self):
        """define a simple Gaussion application"""

        experiment = ExperimentModel()
    
        # skip experiment.experimentId
        # use default project for the testing
        projectname = "DemoProject"
        projectid = self.getprojects(projectname=projectname, idonly=True)[0]
        experiment.projectId = projectid
        experiment.gatewayId = self.gatewayid
        experiment.experimentType = ExperimentType.SINGLE_APPLICATION
        experiment.userName = self.username
        randomexname = "GaussianTestJob" + str(random.randint(2,100))
        experiment.experimentName = randomexname
        experiment.description = "Gaussian Experiment Sample" 

        # register input file
        gefile = DataProductModel()
        gefile.gatewayId = self.gatewayid
        gefile.ownerName = self.username
        gefile.productName = "Gaussian.com"
        gefile.dataProductType = DataProductType.FILE

        gest = DataReplicaLocationModel()
        gest.storageResourceId = self.storageid
        gest.replicaName = "Gaussian.com"
        gest.replicaLocationCategory = ReplicaLocationCategory.GATEWAY_DATA_STORE 
        gest.replicaPersistentType = ReplicaPersistentType.TRANSIENT
        storagehost = self.storagehost
        workingdir = self.storageroot + "/" + self.username + "/" + projectname + "/" + experiment.experimentName + "/"
        #gest.filePath = workingdir + "Gaussian.com"
        #"file://" . $hostName . ":" . $filePath;
        gest.filePath = "file://" + self.storagehost + ":" + workingdir + "Gaussian.com"
        #print(gest.filePath)

        gefile.replicaLocations = [gest]

        uri = self.registerinputfile(gefile)
        # this a good uri example
        #uri = "airavata-dp://37b07a00-e75c-4399-8ec3-4c0e8b7691b2"
        inputobj = InputDataObjectType()
        inputobj.name = "Gaussian.com"
        inputobj.type = DataType.URI
        inputobj.value = uri
        inputobj.inputOrder=1
        inputobj.isRequired=True
        inputobj.requiredToAddedToCommandLine=True
        inputobj.storageResourceId = self.storageid
        
        experiment.experimentInputs = [inputobj]
        # appModuleId ='Gaussian_57eb2905-1cd8-400e-ad40-cadfba8f434f'
        # computeHostId = 'comet.sdsc.edu_91b900df-0ee0-4909-89b3-98e8f64e1969'
        # appDeploymentId = 'comet.sdsc.edu_Gaussian_57eb2905-1cd8-400e-ad40-cadfba8f434f'
        # should use applicationid
        appinterfaceid = self.getapplicationinterfaces(appname = "Gaussian",idonly=True)[0]
        experiment.executionId = appinterfaceid

        # schedule reosurce
        ucdm = UserConfigurationDataModel()
        crsm = ComputationalResourceSchedulingModel()
        crsm.resourceHostId = 'comet.sdsc.edu_91b900df-0ee0-4909-89b3-98e8f64e1969'
        # queue = shared node=1 corecount=4 walltimelimit = 30
        crsm.totalCPUCount = 4
        crsm.nodeCount = 1
        crsm.numberOfThreads = 0
        crsm.totalPhysicalMemory = 0
        crsm.wallTimeLimit = 30
        crsm.queueName = "shared"
        ucdm.computationalResourceScheduling = crsm
        ucdm.storageId = self.storageid
        ucdm.experimentDataDir = workingdir
        experiment.userConfigurationData = ucdm

        print("generating a sample experiment: ", randomexname)

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



