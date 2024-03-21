"""
 tthis module handles decoding and encoding json messages to aid
 DS_messenger.py. extract_json() converts the server's response messages
 into something the rest of the program can read.
"""
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


RecTuple = namedtuple('RecTuple', ['type', 'message', 'token', 'messages'])


def extract_json(json_msg: str) -> RecTuple:
    '''
    call the json.loads function on a json string and convert it
    to a DataTuple object.

    '''
    try:
        json_obj = json.loads(json_msg)
        type1 = json_obj['response']['type']
        msg = ""
        try:
            msg = json_obj['response']['message']
        except Exception:  # pylint: disable=broad-except
            pass

        msgs = []
        try:
            for m in json_obj['response']['messages']:
                m_e = dsm.DirectMessage()
                m_e.sender = m['from']
                m_e.timestamp = m['timestamp']
                m_e.message = m['message']
                msgs.append(m_e)
        except Exception:  # pylint: disable=broad-except
            pass
        token = ""

        if type1 == "ok":
            if "token" in str(json_obj):
                token = json_obj['response']['token']

    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return RecTuple(type1, msg, token, msgs)


def format_json_join(username, password):
    '''
    given the username and password, format a json string to send
    as a json join message to server.
    '''
    return '{"join": {"username": ' + '"' + username + '"' + ', "password": ' \
        + '"' + password + '"' + ', "token": ""' + '}}'


def format_json_post(token, postmsg):
    '''
    given the token and the message to post, format a json string to
    send as a json post message to server.
    '''
    t = time.time()
    return '{"token": ' + '"' + token + '"' + ', "post": {"entry": ' + \
        '"' + postmsg + '"' + ', "timestamp" :' + str(t) + '}}'


def format_json_bio(token, bio):
    '''
    given the token and the new bio, format a json string to send as a
    change-bio message to server.
    '''
    t = time.time()
    return '{"token": ' + '"' + token + '"' + ', "bio": {"entry": ' + '"' + \
        bio + '"' + ', "timestamp" :' + str(t) + '}}'


def format_json_send_dm(token, message, recipient, t=""):
    '''
    given the token, message, and recipient's username format a json string to
    send a dm through the server. timestamp is generated if not given.
    '''
    if t == "":
        t = time.time()
    else:
        pass
    return '{"token":' + '"' + token + '"' + ', "directmessage": {"entry": '\
        + '"' + message + '","recipient":"' + recipient + '"' + \
        ', "timestamp": "' + str(t) + '"}}'


def format_json_other_dm(token, option):
    '''
    given the token, format a json string to either retrieve new messages, or
    retrieve all messages from the server.
    '''
    r = ""
    if option == "n":
        r = '{"token":"' + token + '", "directmessage": "new"}'
    elif option == "a":
        r = '{"token":"' + token + '", "directmessage": "all"}'
    else:
        r = "problem"
    return r
