#!/usr/bin/env python3
import requests, json, time, sys, csv
from config import *

# Get key values required to access Enterprise API from config file; build complete header to accompany API request
if SESSION_ID:
	myHeader = {'Authorization': 'Bearer ' + SESSION_ID,
				'User-Agent': 'KBH Python Script to explore sObjects',
				'Host': HOST,
				'Content-Type' : 'application/json'
				}
else:
	print("Session ID or Auth token not found - cannot proceed")
	sys.exit(2)

############################################ FUNCTION DEFINITIONS #############################################

# Function that makes Product Catalog API request until successful response obtained, returns that response for processing
def apiRequest(url):

	try:
		apiResponse = requests.get(url, headers=myHeader, timeout=120)
		apiResponse.close()
	except:
		print(apiResponse.status_code)

	return apiResponse

######################################### END OF FUNCTION DEFINITIONS #########################################

print("Start: ", time.asctime( time.localtime(time.time()) ))	#Log script start time to console

outfile=open('./objects-and-scopes.csv','w')
filewriter=csv.writer(outfile)
filewriter.writerow(["Object Name", "Object Label", "Object Scope", "Scope Label"])

getObjectsUrl = "https://{0}/services/data/v{1}/sobjects/".format(HOST, VERSION)
#print(getObjectsUrl)

objectsResponse = apiRequest(getObjectsUrl)

nbrObjects = 0

print("Number of sObjects in org: " + str(nbrObjects))

for sObjects in objectsResponse.json()['sobjects']:

	print(sObjects['name'] + " - " + sObjects['label'])

	describeObjectUrl = "https://{0}/services/data/v{1}/sobjects/{2}/describe".format(HOST, VERSION, sObjects['name'])
	describeResponse = apiRequest(describeObjectUrl)

	nbrScopes = 0

	if describeResponse.json()['supportedScopes']:
		for scope in describeResponse.json()['supportedScopes']:

			#print(describeResponse.json()['supportedScopes'][nbrScopes]['name'] + " - " + describeResponse.json()['supportedScopes'][nbrScopes]['label'])
			filewriter.writerow([sObjects['name'], sObjects['label'], describeResponse.json()['supportedScopes'][nbrScopes]['name'], 
				describeResponse.json()['supportedScopes'][nbrScopes]['label']])

			nbrScopes += 1
	else:
		#print("No scope defined")
		filewriter.writerow([sObjects['name'], sObjects['label'], "No scope name", "No scope label"])

	nbrObjects += 1

print("Number of sObjects in org: " + str(nbrObjects))

print("End: ", time.asctime( time.localtime(time.time()) ))	# Log script completion ending time to console
print(describeResponse.headers['Sforce-Limit-Info'])