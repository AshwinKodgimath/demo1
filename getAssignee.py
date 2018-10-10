import json
import os
import requests
import sys
import traceback

# Module level constants
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED = "FAILED"
STATUS_KEY = "status"
ERROR_KEY = "error"
RESULT_KEY = "result"
CDQ_CONFIG = "commercial_data_quality_config"
ISALIVE_KEY = "isAlive"

"""
Purpose     :   This function will hit to JIRA API to get the list of all assignee's
Input       :   None
Output      :   return json dict
"""
return_status = {}
try:
	print("Started process to call JIRA API - get_assignee_list")
	# Getting Jira URL from app config to get assignee list
	jira_get_assignee_list_url = "https://jira.devops.amgen.com/rest/api/2/user/assignable/search?project=CDQ2"
	# Service account name - to get the value for Reporter
	jira_user = "svc-gco-us-data-prd"
	jira_password = "svc-gco-us-data-prd"

	# Request to JIRA api by providing the jira user name and password
	response = requests.get(jira_get_assignee_list_url, auth=(jira_user, jira_password))

	if "errors" in response.json():
		error_str = "Failed to call JIRA API - get assignee list. ERROR : "
		# Multiple error might be present in 'errors' key, so rotating throughout the json object
		for key in response.json()["errors"]:
			error_str += '>> ' + response.json()["errors"][key]
		print(error_str)
		return_status[STATUS_KEY] = STATUS_FAILED
		return_status[ERROR_KEY] = error_str
		print (return_status)

	assignee_list = []
	for item in response.json():
		assignee = dict()
		assignee["display_name"] = item["displayName"] + " - " + item["emailAddress"]
		assignee["value"] = item["key"]
		assignee_list.append(assignee)

	if len(assignee_list) == 0:
		error_str = "No assignee found for this project."
		print(' ' + error_str)
		return_status[STATUS_KEY] = STATUS_FAILED
		return_status[ERROR_KEY] = error_str
		print (return_status)

	print("Get JIRA - assignee list process completed.")
	return_status[STATUS_KEY] = STATUS_SUCCESS
	return_status[RESULT_KEY] = assignee_list
	return_status[ISALIVE_KEY] = True
	print (return_status)
except Exception as e:
	error_str = "Failed to get the JIRA assignee list. ERROR : " + str(e)
	print(error_str)
	return_status[STATUS_KEY] = STATUS_FAILED
	return_status[ERROR_KEY] = error_str
	return_status[ISALIVE_KEY] = True
	print (return_status)