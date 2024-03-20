# Profile.py
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE 
# RIGHT NOW, though can you certainly take a look at it if you are curious since we 
# already covered a bit of the JSON format in class.
#
import json, time
from pathlib import Path
import ds_messenger as dsm


"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class Conversation(dict):

    def __init__(self, name:str = None):
        self.set_name(name)
        self.set_msgs()

        dict.__init__(self, name=self._name, messages = self._messages)

    def add_message(self, msg, recipient, sender):
        d = dsm.DirectMessage()
        d.message = msg
        d.recipient = recipient
        d.sender = sender
        self._messages.append(d)

        dict.__setitem__(self, 'messages', self._messages)

    def set_msgs(self, m=[]):
        self._messages = m
        dict.__setitem__(self, 'messages', self._messages)
    
    def set_name(self, name):
        self._name = name 
        dict.__setitem__(self, 'name', name)
    
    def to_dict(self):
        me = []
        for m in self._messages:
            if type(m) == dict:
                me.append(m)
            else:
                me.append({
                'message': m.message,
                'recipient': m.recipient,
                'sender': m.sender
            })
        self.set_msgs(m=me)

        return self

    name = property(set_name)
    messages = property(set_msgs, add_message)

    
class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You 
    will need to use this class to manage the information provided by each new user 
    created within your program for a2. Pay close attention to the properties and 
    functions in this class as you will need to make use of each of them in your program.

    When creating your program you will need to collect user input for the properties 
    exposed by this class. A Profile class should ensure that a username and password 
    are set, but contains no conventions to do so. You should make sure that your code 
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver # REQUIRED
        self.username = username # REQUIRED
        self.password = password # REQUIRED
        self.bio = ''            # OPTIONAL
        self._convos = []

    def add_msg(self, sender, recipient, msg, opt=""):
        if opt == "me":
            for c in self._convos:
                if c._name == recipient:
                    Conversation.add_message(c, msg, sender=sender, recipient=recipient)
        else:
            for c in self._convos:
                if c._name == sender:
                    Conversation.add_message(c, msg, sender=sender, recipient=recipient)

    def add_convo(self, recp):
        c = Conversation(name=recp)
        self._convos.append(c)

    """

    save_profile accepts an existing dsu file to save the current instance of Profile 
    to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """
    def save_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                convos = [c.to_dict() for c in self._convos]
                self._convos = convos
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a 
    DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self._convos = []
                for f_obj in obj['_convos']:
                    c = Conversation(f_obj['name'])
                    c.set_msgs(m=[])
                    if f_obj['messages'] != []:
                        for m in f_obj['messages']:
                            c.add_message(msg=m['message'], recipient=m['recipient'], sender=m['sender'])
                    self._convos.append(c)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
