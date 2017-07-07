"""
	airavata_client_test.py
"""

from airavata_client import AiravataClient
import time


def main():
	

	ac = AiravataClient(configfile = '~/Projects/airavata-client.ini')

	# get defualt project id
	#print(ac.getprojects(projectname='Default Project',idonly=True))
	# get application id
	#print(ac.getapplicationinterfaces(appname = "Gaussian",idonly=True))

	#print(ac.getapplications(appname = "Gaussian"))

	# pull out an successful experiment
	#exid = ac.getexperiments(experimentname= "GaussianTestJob01",idonly=True)[0]
	#goodex = ac.getexperimentbyid(exid)
	#print(goodex)
	# print("================")
	#ex =ac.sampleexperiment()
	#print(ex)
	
	#exid = ac.createexperiment(ex)
	
	#exid ="GaussianTestJob01_951965a6-a87e-469c-ba23-c0256d564b9e"
	#exid ="GaussianTestJob01_7b6080c9-6029-425d-bf89-9f9143f6caec"
	#print(exid)
	#print(ac.getexperiment(exid))
	#ac.launchexperiment(exid)
	#time.sleep(20)
	#print(ac.getexperimentstatus(exid))
	exid = "test03_bd95f379-bc28-4300-95db-2e28df4377a4"
	print(ac.getexperimentoutputs(exid))

if __name__ == '__main__':
	main()
