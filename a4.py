"""
 the main module. Please run this to run the program. A4 deals with tkinter
 and uses all the other modules to be able to send, store, and display
 DirectMessaging. To use the direct messaging system, please obey the popup
 and either load or create a DSU file. Previous conversation and messages will
 automatically load, and new messages will update every 5 seconds.
"""
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import simpledialog
import os
from pathlib import Path
import ds_messenger as dsm
import Profile


class Body(tk.Frame):
    """
    the main body of the program, containing all the widgets and entryboxes.
    """
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):  # pylint: disable=unused-argument
        """
        executes if something is selected; specifically used for
        selecting a contact's name.
        """
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contacts(self, l_ist):
        """
        given a list, insert all the contacts into the contact tree
        """
        for c in l_ist:
            self.insert_contact(c.get_name())

    def insert_contact(self, contact: str):
        """
        insert one contact.
        """
        self._contacts.append(contact)
        i_d = len(self._contacts) - 1
        self._insert_contact_tree(i_d, contact)

    def _insert_contact_tree(self, i_d, contact: str):
        """
        actually inserts the contact into the tree.
        """
        entry = contact
        if len(contact) > 25:
            entry = contact[:24] + "..."
        i_d = self.posts_tree.insert('', i_d, i_d, text=entry)

    def insert_contact_message(self, message: str):
        """
        inserts a message into the body, can be used for sending a
        message or for receiving one.
        """
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """
        returns what the user has typed into the message box, so that we
        can send the contents through a DM.
        """
        return self.message_editor.get('1.0', 'end').rstrip()

    def _draw(self):
        """
        forms the actual window of the body, defining the editors, contact
        trees, labels, and the text window showing all the messages.
        """
        self.header_label = tk.Label(master=self,
                                     text="this is melody's DS messenger!")
        self.header_label.pack(fill=tk.BOTH, side=tk.TOP)

        posts_frame = tk.Frame(master=self, width=150, bg="pink")
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=10, pady=10)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="pink")
        editor_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.RIGHT,
                               expand=True, padx=10, pady=10)

        message_frame = tk.Frame(master=self, bg="pink")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.RIGHT,
                                 expand=True, padx=10, pady=10)

        scroll_frame = tk.Frame(master=entry_frame, bg="pink", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.RIGHT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """
    footer of the window, containing some text and the send button.
    """
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """
        sends the message if the send message is clicked.
        """
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """
        draws the send button and adds the label
        """
        save_button = tk.Button(master=self, background="Pink",
                                text="Send", width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self,
                                     text="developed by melody fang \
(mkfang@uci.edu)")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class ConfigServerDialog(simpledialog.Dialog):
    # pylint: disable=too-many-instance-attributes
    """
    opens the window for users to configure what server they'd like to join,
    and input all of their usernames, passwords, etc.
    """
    def __init__(self, root, title=None):
        self.root = root
        self.server = None
        self.user = None
        self.pwd = None
        super().__init__(root, title)

    def body(self, master):
        """
        forms the window, and prompts for the entry fields.
        """
        self.server_label = tk.Label(master, width=30,
                                     text="DS server address")
        self.server_label.pack()
        self.server_entry = tk.Entry(master, width=30)
        self.server_entry.pack()

        self.username_label = tk.Label(master, width=30, text="username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(master, width=30, text="password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, width=30, show="*")
        self.password_entry.pack()

        self.apply()

    def apply(self):
        """
        sets the values from the entry boxes into the body's attributes.
        """
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class CreateFileDialog(tk.simpledialog.Dialog):
    """
    opens the window for users to create a new DSU file.
    """
    def __init__(self, root, title=None, path=None, name=None):
        self.root = root
        self.path = path
        self.name = name
        super().__init__(root, title)

    def body(self, master):
        """
        forms the window and prompts for the entry fields.
        """
        self.path_label = tk.Label(master, width=30,
                                   text="path for file location")
        self.path_label.pack()
        self.path_entry = tk.Entry(master, width=30)
        self.path_entry.pack()

        self.name_label = tk.Label(master, width=30,
                                   text="name for your file")
        self.name_label.pack()
        self.name_entry = tk.Entry(master, width=30)
        self.name_entry.pack()

        self.apply()

    def apply(self):
        """
        sets the values from the entryboxes into attributes.
        """
        self.path = self.path_entry.get()
        self.name = self.name_entry.get()


class MainApp(tk.Frame):  # pylint: disable=too-many-instance-attributes
    """
    contains almost all of the necessary attributes for the DSMessenger to run.
    """
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.token = None
        self.direct_messenger = dsm.DirectMessenger(self.server,
                                                    self.username,
                                                    self.password)
        self.profile = None
        self.filename = None
        self._draw()

    def send_message(self):
        """
        take the entry from the textbox and send it through DS_Messenger.py,
        handles users trying to send with no wifi.
        """
        mm = Body.get_text_entry(self.body)
        if mm != "":
            try:
                if self.direct_messenger.send(mm, self.recipient) is True:
                    self.token = dsm.DirectMessenger.gettoken(
                        self.direct_messenger)
                    self.body.insert_contact_message(f"{self.username}: {mm}")
                    self.body.message_editor.delete("1.0", tk.END)

                    m = dsm.DirectMessage()
                    m.message = mm
                    m.recipient = self.recipient
                    m.sender = self.username

                    self.profile.load_profile(self.filename)
                    self.profile.add_msg(recipient=m.recipient, msg=mm,
                                         sender=m.sender, opt="me")
                    self.profile.save_profile(self.filename)
                else:
                    showinfo("error", "message was not sent. you may not be \
connected to the internet.")

            except Exception:  # pylint: disable=broad-except
                pass

    def add_contact(self):
        """
        prompts the user for the new contact's username. will show a popup
        if not accepted.
        """
        idk = tk.simpledialog.askstring("Add New Contact",
                                        "what is the username?")

        if idk.strip() != "":
            self.body.insert_contact(idk)
            self.profile.add_convo(recp=idk)
            self.profile.save_profile(self.filename)
        else:
            showinfo("error", "invalid username")

    def recipient_selected(self, recipient):
        """
        clears the shown messages and resents the recipient attribute,
        if a contact is selected from the tree.
        """
        self.body.entry_editor.delete(1.0, tk.END)
        self.recipient = recipient
        self.load_msgs(recipient)

    def load_msgs(self, recipient):
        """
        looks into the profile to find and distribut the existing messages.
        loads them into the text body if either the sender or recipient is
        the selected recipient.
        """
        try:
            self.profile.load_profile(self.filename)
            self.body.entry_editor.delete("1.0", tk.END)
            l_st = []
            l_st = self.profile.get_convos()
            for l1 in l_st:
                if l1.get_name() == recipient:
                    for m in l1.get_messages():
                        if recipient in (m.recipient, m.sender):
                            self.body.insert_contact_message(f"{m.sender}: \
{m.message}")
        except Exception:  # pylint: disable=broad-except
            pass

    def configure_server(self):
        """
        configures the server information once the user makes a new file.
        """
        ud = ConfigServerDialog(self.root, "Configure Account")

        if ud.user.strip() != "" and ud.pwd.strip() != "" and ud.server != "":
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server

            try:
                self.direct_messenger = dsm.DirectMessenger(self.server,
                                                            self.username,
                                                            self.password)
                dsm.DirectMessenger.send(self.direct_messenger)
            except Exception:  # pylint: disable=broad-except
                pass

    def create_p(self):
        """
        creates a new DSU file, prompting for a location and a name.
        """
        idk = CreateFileDialog(self.root, "Create DSU File")
        filename = idk.name + ".dsu"
        comb = os.path.join(idk.path, filename)

        self.configure_server()

        try:
            ppath = Path(comb)
            ppath.touch(exist_ok=True)

            self.profile = Profile.Profile(username=self.username,
                                           password=self.password)
            self.profile.dsuserver = self.server

            self.profile.save_profile(ppath)
            self.filename = ppath

            self.direct_messenger = dsm.DirectMessenger(self.server,
                                                        self.username,
                                                        self.password)
            dsm.DirectMessenger.send(self.direct_messenger)
        except Exception:  # pylint: disable=broad-except
            pass

    def load_p(self):
        """
        loads an existing file, prompting for the path to the file.
        """
        idk = tk.simpledialog.askstring("Load DSU File",
                                        "what is the path to the file?")
        self.profile = Profile.Profile()
        self.profile.load_profile(path=idk)
        self.filename = idk

        self.username = self.profile.username
        self.password = self.profile.password
        self.server = self.profile.dsuserver

        self.body.insert_contacts(self.profile.get_convos())

        self.direct_messenger = dsm.DirectMessenger(self.server,
                                                    self.username,
                                                    self.password)

        try:
            dsm.DirectMessenger.send(self.direct_messenger)
        except Exception:  # pylint: disable=broad-except
            showinfo("error", "we could not connect to the server. \
you cannot send anything.")

    def check_new(self):
        """
        checks for new messages by connecting to the server, and then locally
        stores the new messages if any are found. loops!
        """
        x = dsm.DirectMessenger.retrieve_new(self.direct_messenger)
        if x is not None:
            for x1 in x:
                self.profile.add_msg(sender=x1.sender, msg=x1.message,
                                     recipient=self.username, opt="no")
                self.profile.save_profile(self.filename)

            self.body.entry_editor.delete("1.0", tk.END)
            self.load_msgs(self.recipient)

        self.root.after(ms=5000, func=self.check_new)

    def _draw(self):
        """
        adds the menu and creates an initial popup to give the user some
        instructions.
        """
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.create_p)
        menu_file.add_command(label='Open', command=self.load_p)

        menu_bar.add_command(label='Add Contact',
                             command=self.add_contact)
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        showinfo("window", "welcome to the program!! please click file first, \
and then choose to open or make a DSU file.")


def main():
    """
    initializes everything and creates the initial window, with sizes
    and the loop.
    """
    main_ = tk.Tk()
    main_.title("melody's ds messaging")
    main_.geometry("560x560")
    main_.option_add('*tearOff', False)
    app = MainApp(main_)
    main_.update()
    main_.minsize(main_.winfo_width(), main_.winfo_height())
    main_.after(ms=5000, func=app.check_new)
    main_.mainloop()


if __name__ == "__main__":
    main()
