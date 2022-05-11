# Peter Hartmeier
# phartmei@uci.edu
# 61283483
import socket, ds_protocol, Profile, exceptions

class DirectMessage:
    def __init__(self, r=None, m=None, t=None, s=None):
        self.recipient = r
        self.message = m
        self.timestamp = t
        self.sent = s


class DirectMessenger:
    def __init__(self, dsuserver='168.235.86.101', username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.port = 3021
        self.username = username
        self.password = password

    def send(self, message:str, recipient:str, dmhis=None) -> bool:
        print('send running')
        # returns true if message successfully sent, false if send failed.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.connect((self.dsuserver, self.port))

            if self.token == None:
                # link elements for join command and output message
                join_msg = '{"join": {"username": "' + self.username + '","password": "' + self.password + '", "token":""}}'
                joining = ds_protocol.output(cycle(srv, join_msg))

                if joining[1] != 'ok':
                    print('bad\n', joining)
                    return False

                print(joining[2])

                self.token = joining[0]['token']

            send = cycle(srv, ds_protocol.ptpsend(message, recipient, self.token))
            print('test\n', ds_protocol.ingest_dmresponse(send))

            try:
                if ds_protocol.ingest_dmresponse(send) == ['ok', "Direct message sent"]:
                    if dmhis != None:
                        print('ds_send')
                        x = dmhis.new_mess(message, recipient)
                        print('check')
                    return True
                else:
                    print(ds_protocol.ingest_dmresponse(send))
                    return False
            except Exception as err:
                print(err)
                return False

    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.connect((self.dsuserver, self.port))

            if self.token == None:
                # link elements for join command and output message
                join_msg = '{"join": {"username": "' + self.username + '","password": "' + self.password + '", "token":""}}'
                joining = ds_protocol.output(cycle(srv, join_msg))

                if joining[1] != 'ok':
                    raise exceptions.DSU_Join_Issue()

                self.token = joining[0]['token']

            send = cycle(srv, ds_protocol.request_new(self.token))

            users = ds_protocol.ingest_messresponse(send)
            lis = []
            for i in users:
                for m in users[i]:
                    lis.append(DirectMessage(r=i, m=m['message'], t=m['timestamp']))

            return lis

    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.connect((self.dsuserver, self.port))

            if self.token == None:
                # link elements for join command and output message
                join_msg = '{"join": {"username": "' + self.username + '","password": "' + self.password + '", "token":""}}'
                joining = ds_protocol.output(cycle(srv, join_msg))

                if joining[1] != 'ok':
                    raise exceptions.DSU_Join_Issue()

                self.token = joining[0]['token']

            send = cycle(srv, ds_protocol.request_all(self.token))

            users = ds_protocol.ingest_messresponse(send)
            lis = []
            for i in users:
                for m in users[i]:
                    lis.append(DirectMessage(r=i, m=m['message'], t=m['timestamp']))

            return lis

    def online_check(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
                srv.connect((self.dsuserver, self.port))

                # link elements for join command and output message

                join_msg = '{"join": {"username": "' + self.username + '","password": "' + self.password + '", "token":""}}'
                joining = ds_protocol.output(cycle(srv, join_msg))

                if joining[1] != 'ok':
                    return False
                else:
                    return True
        except:
            return False


#send and recieve server commands
def cycle(srv, join_msg):
  send = srv.makefile('w')
  recv = srv.makefile('r')

  send.write(join_msg + '\r\n')
  send.flush()

  return recv.readline()