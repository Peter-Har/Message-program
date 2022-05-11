# Peter Hartmeier
# phartmei@uci.edu
# 61283483

import json, time
import nacl.utils
from nacl.public import Box

# breaks down ICS 32 DSP json messages to their base parts
def output(json_msg:str):
  try:
    json_obj = json.loads(json_msg)
    response = json_obj['response']
    status = json_obj['response']['type']
    message = json_obj['response']['message']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return [response, status, message]

def ptpsend(mess, to, fro):
  """formats a direct message request to json"""
  return '{"token":"' + fro + '", "directmessage": {"entry": "' + mess + '","recipient":"' + to + '", "timestamp": "' + str(time.time()) + '"}}'

def request_new(fro):
  """formats a new message request to json"""
  return '{"token":"' + fro + '", "directmessage": "new"}'

def request_all(fro):
  """formats an all message request to json"""
  return '{"token":"' + fro + '", "directmessage": "all"}'

def ingest_dmresponse(resp):
  """processes json dm response"""
  resp = output(resp)
  return [resp[1], resp[2]]

def ingest_messresponse(resp):
  """processes json 'new' and 'all' responses"""

  resp = json.loads(resp)
  users = {}

  if resp['response']['type'] == 'ok':
    for i in resp['response']['messages']:
      if i['from'] in users:
        users[i['from']].append({'message': i['message'], 'timestamp': i['timestamp']})
      else:
        users[i['from']] = [{'message': i['message'], 'timestamp': i['timestamp']}]

  return users


