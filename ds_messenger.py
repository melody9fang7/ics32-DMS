import socket
import ds_protocol as dp


class DirectMessage:
    """
    class to represent DMs. includes all properties needed to represent a DM
    sent to the server.
    """
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None
        self.sender = None


class DirectMessenger:
    """
    class to represent a direct messenger object. contains everything needed to
    connect to the server, retrieve messages, and send messages.
    """
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def gettoken(self):
        """
        return the current token.
        """
        return self.token

    def send(self, message:str="", recipient:str="") -> bool:
        """
        connects to server and sends the dm, joining first if not finding an existing token.
        returns true or false depending on whether the execution was successful.
        """
        ex = False
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.dsuserver, 3021))
                send = client.makefile("wb")
                recv = client.makefile("rb")

                if self.token is None:
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
            return ex



    def retrieve_new(self) -> list:
        """
        connects to server and requests all messages, then returns a list of directmessage objects
        """
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
                    new_m = resp.messages
                else:
                    print(f"error! {resp.message}")

            return new_m
        except:
            pass

    def retrieve_all(self) -> list:
        """
        connects to server and requests all messages, then returns a list of directmessage objects
        """
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
                new_m = resp.messages

            return new_m
        except:
            pass
