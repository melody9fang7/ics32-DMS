import ds_protocol as dp
import socket

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None
    self.sender = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
    
    def gettoken(self):
        return self.token
    
    def send(self, message:str="", recipient:str="") -> bool:
    # must return true if message successfully sent, false if send failed.
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                ex = False
                client.connect((self.dsuserver, 3021))

                send = client.makefile("wb")
                recv = client.makefile("rb")

                if self.token == None:
                    w = dp.format_json_join(self.username, self.password)
                    send.write(w.encode() + b"\r\n")
                    send.flush()

                    resp = recv.readline()
                    resp = dp.extract_json(resp)

                    if resp.type == "ok":
                        if resp.token != "":
                            self.token = resp.token
                            print(resp.message)
                    else:
                        print(f"error! {resp.message}")
                        ex = False
                
                if message != "" and recipient != "":
                    w = dp.format_json_send_dm(self.token, message, recipient)
                    send.write(w.encode() + b"\r\n")
                    send.flush()

                    resp = recv.readline()
                    resp = dp.extract_json(resp)

                    if resp.type == "ok":
                        if resp.token.strip() != "":
                            self.token = resp.token
                        print(resp.message)
                        ex = True
                    else:
                        print(f"error! {resp.message}")
                        ex = False

            return ex
        except:
            return False



    def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, 3021))

                send = client.makefile("wb")
                recv = client.makefile("rb")
                what_to_send = dp.format_json_other_dm(self.token, "n")

                send.write(what_to_send.encode() + b"\r\n")
                send.flush()

                resp = recv.readline()
                resp = dp.extract_json(resp)

                new_m = []
                if resp.type == "ok":
                    new_m = (resp.messages)
                else:
                    print(f"error! {resp.message}")

            return new_m
        except:
            pass 
 
    def retrieve_all(self) -> list:
    # must return a list of DirectMessage objects containing all messages
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, 3021))

                send = client.makefile("wb")
                recv = client.makefile("rb")
                what_to_send = dp.format_json_other_dm(self.token, "a")

                send.write(what_to_send.encode() + b"\r\n")
                send.flush()

                resp = recv.readline()
                resp = dp.extract_json(resp)
                new_m = (resp.messages)
            
            return new_m
        except:
            pass