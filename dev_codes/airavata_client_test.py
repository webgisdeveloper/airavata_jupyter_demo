"""
	airavata_client_test.py
"""

from airavata_client import AiravataClient

def main():
	
	ac = AiravataClient(configfile = '~/Projects/airavata-client.ini')
	print(ac.getprojects())
	#ac.createproject("Test01","Testing project for Gaussian application")
	#print(ac.isnotebook())
	apps = ac.getapplications(module = "Gaussian")
	print(apps)

if __name__ == '__main__':
	main()
