import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from typing import Text
import os
from pathlib import Path
import ds_messenger as dsm
import Profile
from tkinter.messagebox import showinfo


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contacts(self, l_ist):
        for c in l_ist:
            self.insert_contact(c._name)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        entry - contact
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=entry)

    def insert_user_message(self, message: str):
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
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
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, background="Pink",
                                text="Send", width=20, command=self.send_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="all ready :)")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class JoinServerDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS server address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show="*")
        self.password_entry.pack()

        self.apply()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, recipient=None):
        self.root = root
        self.user = user
        self.recipient = recipient
        super().__init__(root, title)

    def body(self, frame):

        self.new_username_label = tk.Label(frame, width=30,
                                           text="recipient's username")
        self.new_username_label.pack()
        self.new_username_entry = tk.Entry(frame, width=30)
        self.new_username_entry.pack()

        self.apply()

    def apply(self):
        self.recipient = self.new_username_entry.get()


class CreateFileDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, path=None, name=None):
        self.root = root
        self.path = path
        self.name = name
        super().__init__(root, title)

    def body(self, frame):

        self.path_label = tk.Label(frame, width=30,
                                   text="path for file location")
        self.path_label.pack()
        self.path_entry = tk.Entry(frame, width=30)
        self.path_entry.pack()

        self.name_label = tk.Label(frame, width=30,
                                   text="name for your file")
        self.name_label.pack()
        self.name_entry = tk.Entry(frame, width=30)
        self.name_entry.pack()

        self.apply()

    def apply(self):
        self.path = self.path_entry.get()
        self.name = self.name_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.token = None
        self.direct_messenger = dsm.DirectMessenger(self.server,
                                                    self.username, self.password)
        self.profile = None
        self.filename = None
        self._draw()

    def send_message(self):
        mm = Body.get_text_entry(self.body)
        if mm != "":
            try:
                self.direct_messenger.send(mm, self.recipient)
                self.token = dsm.DirectMessenger.gettoken(self.direct_messenger)
                self.body.insert_user_message(f"{self.username}: {mm}")
                self.body.message_editor.delete("1.0",tk.END)

                m = dsm.DirectMessage()
                m.message = mm
                m.recipient = self.recipient
                m.sender = self.username

                self.profile.load_profile(self.filename)
                self.profile.add_msg(recipient=m.recipient, msg=mm,
                                     sender=m.sender, opt="me")
                self.profile.save_profile(self.filename)
            except:
                pass

    def add_contact(self):
        idk = tk.simpledialog.askstring("Add New Contact", "what is the username?")

        self.body.insert_contact(idk)
        self.profile.add_convo(recp=idk)
        self.profile.save_profile(self.filename)

    def recipient_selected(self, recipient):
        self.body.entry_editor.delete(1.0,tk.END)
        self.recipient = recipient
        self.load_msgs(recipient)

    def load_msgs(self, recipient):
        try:
            self.profile.load_profile(self.filename)
            self.body.entry_editor.delete("1.0",tk.END)
            l = []
            l = self.profile._convos
            if l != []:
                for l1 in l:
                    if l1._name == recipient:
                        if l1._messages != []:
                            for m in l1._messages:
                                if m.recipient == recipient or  m.sender == recipient:
                                    self.body.insert_contact_message(f"{m.sender}: {m.message}")
        except:
            pass

    def configure_server(self):
        ud = JoinServerDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)

        if ud.user.strip() != "" and ud.pwd.strip() != "" and ud.server != "":
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server

            try:
                self.direct_messenger = dsm.DirectMessenger(self.server,
                                                            self.username, self.password)
                dsm.DirectMessenger.send(self.direct_messenger)
            except:
                pass

    def create_p(self):
        idk = CreateFileDialog(self.root, "Create DSU File")
        filename = idk.name + ".dsu"
        comb = os.path.join(idk.path, filename)

        self.configure_server(self.root)

        try:
            ppath = Path(comb)
            ppath.touch(exist_ok=True)

            self.profile = Profile.Profile(username=self.username,
                                           password=self.password)
            self.profile.dsuserver = self.server

            self.profile.save_profile(ppath)
            self.filename = ppath

            self.direct_messenger = dsm.DirectMessenger(self.server,
                                                        self.username, self.password)
            dsm.DirectMessenger.send(self.direct_messenger)
        except:
            pass

    def load_p(self):
        idk = tk.simpledialog.askstring("Load DSU File",
                                        "what is the path to the file?")
        self.profile = Profile.Profile()
        self.profile.load_profile(path=idk)
        self.filename = idk

        self.username = self.profile.username
        self.password = self.profile.password
        self.server = self.profile.dsuserver

        self.body.insert_contacts(self.profile._convos)

        self.direct_messenger = dsm.DirectMessenger(self.server,
                                                    self.username, self.password)
        
        try:
            dsm.DirectMessenger.send(self.direct_messenger)
        except:
            showinfo("error", "we could not connect to the server. you cannot send anything.")


    def check_new(self):
        x = dsm.DirectMessenger.retrieve_new(self.direct_messenger)
        if x is not None:
            for x1 in x:
                self.profile.add_msg(sender=x1.sender, msg=x1.message,
                                     recipient=self.username, opt="no")
                self.profile.save_profile(self.filename)

            self.body.entry_editor.delete("1.0",tk.END)
            self.load_msgs(self.recipient)

        self.root.after(ms = 5000, func = self.check_new)

    def _draw(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.create_p)
        menu_file.add_command(label='Open...', command=self.load_p)

        menu_bar.add_command(label='Add Contact',
                                  command=self.add_contact)
        menu_bar.add_command(label='Configure DS Server',
                                  command=self.configure_server)
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        showinfo("window", "welcome to the program!! please click file first, and then choose to open or make a DSU file.")



def main():
    main = tk.Tk()
    main.title("melody's ds messaging")
    main.geometry("560x560")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    main.after(ms=5000, func=app.check_new)
    main.mainloop()


if __name__ == "__main__":
    main()
