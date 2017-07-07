"""
	airavata_client_test.py
"""

from airavata_client import AiravataClient
import time


def main():
	

	ac = AiravataClient(configfile = '~/Projects/airavata-client.ini')
	print(ac.authztoken)
	print(ac.getprojects())

	#ac.createproject("Test01","Testing project for Gaussian application")
	#print(ac.isnotebook())
	#apps = ac.getapplications(module = "Gaussian")
	#print("appModuleID,appDeploymentId,computeHostId")
	#print(apps)
	#appinterfaces = ac.getapplicationinterfaces(appname = "Gaussian")
	#print(appinterfaces)
	#ex =ac.sampleexperiment()
	#exid = ac.createexperiment(ex)
	#exid ="GaussianTestJob01_951965a6-a87e-469c-ba23-c0256d564b9e"
	#exid ="GaussianTestJob01_7b6080c9-6029-425d-bf89-9f9143f6caec"
	#print(exid)
	#print(ac.getexperiment(exid))
	#ac.launchexperiment(exid)
	#time.sleep(10)
	#print(ac.getexperimentstatus(exid))
	#print(ac.getexperimentoutputs(exid))

if __name__ == '__main__':
	main()
