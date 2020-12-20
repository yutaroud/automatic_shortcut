import os
import json
import requests
from requests.auth import HTTPBasicAuth
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

# dotenvの設定
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

key = os.environ.get("TOGGLE_API_KEY")

# APIキーの指定
url = "https://www.toggl.com/api/v8/workspaces"
headers = {'Content-Type': 'application/json'}

def get_workspace_id():
  request = requests.get(url, auth=(key, 'api_token'))
  response = request.json()
  return response[0]['id']

def get_projects(work_space_id):
  dictionary = {}
  request = requests.get(url, auth=(key, 'api_token'))
  response = request.json()
  for res in response:
    dictionary[res["name"]] = res["id"]
  return dictionary

def get_running_time_entry():
  response = requests.get('https://www.toggl.com/api/v8/time_entries/current',
               auth=HTTPBasicAuth(key, 'api_token'))
  if response.status_code != 200:
    print("Error: cannot get running time entry. please check the token.")
    return ""
  data = response.json()['data']
  if data is None:
    return None
  return data['id']

def start(description, project_id):
  params = {"time_entry": {"description": description, "pid": project_id, "created_with": "python"}}
  response = requests.post('https://www.toggl.com/api/v8/time_entries/start',
               auth=HTTPBasicAuth(key, 'api_token'),
               headers=headers,
               data=json.dumps(params))
  print('time entry start. HTTP status :', response.status_code)

def stop(running_time_entry_id):
  url = 'https://www.toggl.com/api/v8/time_entries/' + str(running_time_entry_id) + '/stop'
  response = requests.put(url, auth=HTTPBasicAuth(key, 'api_token'), headers=headers)

  print('time entry stop. HTTP status :', response.status_code)

def main(description):
  work_space_id = get_workspace_id
  project_id = get_projects(work_space_id)
  running_id = get_running_time_entry()
  if running_id == None:
    start(description, project_id)
  else:
    stop(running_id)
