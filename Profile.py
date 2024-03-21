# pylint: disable=invalid-name
"""
provided Profile module from class, with an added Conversation class.
"""
import json
from pathlib import Path
import ds_messenger as dsm


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch
    in your own code. It is raised when attempting to load or save
    Profile objects to file the system.

    """


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch
    in your own code. It is raised when attempting to deserialize a dsu file
    to a Profile object.

    """


class Conversation(dict):
    """
    Conversation class represents a conversation, sorting messages by who
    they're between. the name attribute is the recipient who we're chatting
    with, but the Conversation attribute includes both
    sent and received messages.
    """
    def __init__(self, name: str = None):
        self.set_name(name)
        self.set_msgs()

        dict.__init__(self, name=self._name, messages=self._messages)

    def add_message(self, msg, recipient, sender):
        """
        adding a DirectMessage object to the msgs attribute.
        """
        d = dsm.DirectMessage()
        d.message = msg
        d.recipient = recipient
        d.sender = sender
        self._messages.append(d)

        dict.__setitem__(self, 'messages', self._messages)

    def set_msgs(self, m=""):
        """
        setting the msgs attirbute to either a blank list or a given list.
        """
        if m == "":
            self._messages = []
        else:
            self._messages = m
        dict.__setitem__(self, 'messages', self._messages)

    def set_name(self, name):
        """
        setting the name of the user who the conversation is with.
        """
        self._name = name
        dict.__setitem__(self, 'name', name)

    def get_name(self):
        """
        returns the name of the user who the conversation is with.
        """
        return self._name

    def get_messages(self):
        """
        returns all messages stored in the conversation
        """
        return self._messages

    def to_dict(self):
        """
        used to convert the messages part of the Conversation to a dictionary,
        for easier json formatting and encoding.
        """
        me = []
        for m in self._messages:
            if isinstance(m, dict):
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
    The Profile class exposes the properties required to join an
    ICS 32 DSU server. You will need to use this class to manage the
    information provided by each new user created within your program
    for a2. Pay close attention to the properties and functions in
    this class as you will need to make use of each of them in your program.

    When creating your program you will need to collect user input for the
    properties exposed by this class. A Profile class should ensure that a
    username and password are set, but contains no conventions to do so.
    You should make sure that your code verifies that required properties
    are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''
        self._convos = []

    def add_msg(self, sender, recipient, msg, opt=""):
        """
        adds a message to the appropriate Conversation.
        """
        if opt == "me":
            for c in self._convos:
                if c.get_name() == recipient:
                    Conversation.add_message(c, msg, sender=sender,
                                             recipient=recipient)
        else:
            for c in self._convos:
                if c.get_name() == sender:
                    Conversation.add_message(c, msg, sender=sender,
                                             recipient=recipient)

    def add_convo(self, recp):
        """
        adds a new Conversation to the profile's list.
        """
        c = Conversation(name=recp)
        self._convos.append(c)

    def get_convos(self):
        """
        returns the convos
        """
        return self._convos

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current
        instance of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError

        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w', encoding="utf-8") as f:
                    convos = [c.to_dict() for c in self._convos]
                    self._convos = convos
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the \
                                   DSU file.", ex) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        load_profile will populate the current instance of Profile with data
        stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError

        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r', encoding="utf-8") as f:
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
                                c.add_message(msg=m['message'],
                                              recipient=m['recipient'],
                                              sender=m['sender'])
                        self._convos.append(c)
            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()
