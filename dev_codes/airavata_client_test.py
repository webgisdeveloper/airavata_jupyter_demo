"""
	airavata_client_test.py
"""

from airavata_client import AiravataClient

def main():
	

	ac = AiravataClient(configfile = '~/Projects/airavata-client.ini')
	#print(ac.getprojects())
	#ac.createproject("Test01","Testing project for Gaussian application")
	#print(ac.isnotebook())
	#apps = ac.getapplications(module = "Gaussian")
	#print("appModuleID,appDeploymentId,computeHostId")
	#print(apps)
	#ex =ac.sampleexperiment()
	#exid = ac.createexperiment(ex)
	#print(exid)
	exid = "GaussianTestJob01_d71be9c6-4e69-431c-91b2-6ab70aff68ed"
	ac.launchexperiment(exid)

if __name__ == '__main__':
	main()
