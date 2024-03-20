# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Melody Fang
# mkfang@uci.edu
# 37001380
import json
from collections import namedtuple
import time
import ds_messenger as dsm

class DS32ProtocolError(Exception):
    '''
    An exception to be used when received commands do not follow
    protocol specifications
    '''
    pass

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
RecTuple = namedtuple('RecTuple', ['type','message', 'token', 'messages'])

def extract_json(json_msg:str) -> RecTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object

    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''
    try:
        json_obj = json.loads(json_msg)
        type = json_obj['response']['type']
        msg = ""
        try:
            msg = json_obj['response']['message']
        except:
            pass

        msgs = []
        try:
            for m in json_obj['response']['messages']:
                m_e = dsm.DirectMessage()
                m_e.sender = m['from']
                m_e.timestamp = m['timestamp']
                m_e.message = m['message']
                msgs.append(m_e)
        except:
            pass
        token = ""

        if type == "ok":
            if "token" in str(json_obj):
                token = json_obj['response']['token']
        
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return RecTuple(type, msg, token, msgs)


def format_json_join(username, password):
    return '{"join": {"username": ' + '"' + username + '"' + ', "password": ' + '"' + password + '"' + ', "token": ""' + '}}' 


def format_json_post(token, postmsg):
    t = time.time()
    return '{"token": ' + '"' + token + '"' + ', "post": {"entry": ' + '"' + postmsg + '"' + ', "timestamp" :' + str(t) + '}}'


def format_json_bio(token, bio):
    t = time.time()
    return '{"token": ' + '"' + token + '"' + ', "bio": {"entry": ' + '"' + bio + '"' + ', "timestamp" :' + str(t) + '}}'


def format_json_send_dm(token, message, recipient, t=""):
    if t == "":
        t = time.time()
    else:
        pass
    return '{"token":' + '"' + token + '"' + ', "directmessage": {"entry": ' + '"' + message + '","recipient":"' + recipient +'"' + ', "timestamp": "' + str(t) + '"}}'

def format_json_other_dm(token, option):
    if option == "n":
        return '{"token":"' + token + '", "directmessage": "new"}'
    elif option == "a":
        return '{"token":"' + token + '", "directmessage": "all"}'
    else:
        return "problem!"
