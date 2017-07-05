"""
	airavata_client_test.py
"""

from airavata_client import AiravataClient

def main():
	
	ac = AiravataClient(configfile = '~/Projects/airavata-client.ini')
	
if __name__ == '__main__':
	main()
