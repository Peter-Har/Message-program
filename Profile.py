# Peter Hartmeier
# phartmei@uci.edu
# 61283483

import json, time, os, exceptions, ds_messenger
from pathlib import Path



class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to load or save Profile objects to file the system.

    """
    pass


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to deserialize a dsu file to a Profile object.

    """
    pass
    
class Profile():
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You will need to 
    use this class to manage the information provided by each new user created within your program for a2. 
    Pay close attention to the properties and functions in this class as you will need to make use of 
    each of them in your program.

    When creating your program you will need to collect user input for the properties exposed by this class. 
    A Profile class should ensure that a username and password are set, but contains no conventions to do so. 
    You should make sure that your code verifies that required properties are set.

    """

    def __init__(self, dsuserver='168.235.86.101', username=None, password=None):
        self.dsuserver = dsuserver # REQUIRED
        self.username = username # REQUIRED
        self.password = password # REQUIRED
        self.messages = []
        self.responses = []

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance of Profile to the file system
        """
        p = Path(path)
        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.messages = []
                self.responses = []

                #gets recieved messages
                for post_obj in obj['messages']:
                    self.messages.append(ds_messenger.DirectMessage(r=post_obj['recipient'], m=post_obj['message'], t=post_obj['timestamp']))

                #gets sent messages
                print(obj['responses'])
                for post_obj1 in obj['responses']:
                    print('po', post_obj1)
                    self.responses.append(ds_messenger.DirectMessage(s=post_obj1['sent'], m=post_obj1['message'], t=post_obj1['timestamp']))

                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()


class DmHistory():
  """constructs a dm history of the user"""
  def __init__(self, all, mine):
    '''
    :param all: the server response with all dms of the user organized into list of DirectMessage objects
    :param mine: personal records of sent messages
    '''

    self.users = []
    self.current_user = 'default'

    self.serv = all
    self.pers = mine
    self.conversation = []
    print('serv', self.serv)
    for i in self.serv:
        if i.recipient not in self.users:
            self.users.append(i.recipient)
            self.users.sort()

    print('pers', self.pers)
    for i in self.pers:
        print(i.sent)
        if i.sent not in self.users:
            self.users.append(i.sent)
            self.users.sort()

  def convo_construct(self, usr):
    """
    constructs a time ordered list of conversations
    :param usr: user to be constructed for
    """

    convo = []
    for i in self.serv:
        if i.recipient == usr:
            convo.append(i)

            for (ind, val) in enumerate(convo):
                stam = val.timestamp

                if float(stam) == float(i.timestamp):
                    try:
                        if ind != len(convo) - 1:
                            raise exceptions.Conversation_Sort()
                        else:
                            break
                    except Exception as e:
                        print('Error encountered while sorting: identical timestamps occured\n', e)
                elif float(i.timestamp) > float(stam):
                    pass
                elif float(i.timestamp) < float(stam):
                    convo.insert(ind, i)
                    convo.pop(-1)
                    break

    for i in self.pers:
        if i.sent == usr:
            convo.append(i)

            for (ind, val) in enumerate(convo):
                stam = val.timestamp

                if float(stam) == float(i.timestamp):
                    try:
                        if ind != len(convo) - 1:
                            raise exceptions.Conversation_Sort()
                        else:
                            break
                    except Exception as e:
                        print('Error encountered while sorting: identical timestamps occured\n', e)
                elif float(i.timestamp) > float(stam):
                    pass
                elif float(i.timestamp) < float(stam):
                    convo.insert(ind, i)
                    convo.pop(-1)
                    break

    self.conversation = convo
    return convo

  def new_mess(self, mess, to):
      """adds a new sent message to the saved list"""
      print(ds_messenger.DirectMessage(s=to, m=mess, t=time.time()))

      self.conversation.append(ds_messenger.DirectMessage(s=to, m=mess, t=time.time()))
      self.pers.append(ds_messenger.DirectMessage(s=to, m=mess, t=time.time()))
      print(self.__dict__)
      print('new_mess_end')

  def save_to_profile(self, profile, path):
      """saves dm history to a given profile and saves profile"""
      liss =[]
      for i in self.pers:
          liss.append({'sent': i.sent, 'message': i.message, 'timestamp': i.timestamp})
      profile.responses = liss
      print('stp: ', liss)

      liss = []
      for i in self.serv:
          liss.append({'recipient': i.recipient, 'message': i.message, 'timestamp': i.timestamp})
      profile.messages = liss
      print(liss)

      profile.save_profile(path)