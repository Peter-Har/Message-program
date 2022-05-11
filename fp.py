# Peter Hartmeier
# phartmei@uci.edu
# 61283483

import tkinter as tk
from tkinter import ttk, filedialog
import Profile
import ds_messenger


class Body(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the body portion of the root frame.
    """

    def __init__(self, root, select_callback=None, dmhis=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback
        self.dmhis_call = dmhis
        self.username = ''
        self.color_choice = ['REDD', 'BLUEE']

        # a list of the Post objects available in the active DSU file
        self._posts = []

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def set_colors(self, mine, yours):
        """sets the color choice from MainApp"""
        self.color_choice = [mine, yours]
        print(self.color_choice)

    def node_select(self, event):
        """
        Update the entry_editor with the full post entry when the corresponding node in the posts_tree
        is selected.
        """
        self.set_text_entry('')
        dmhis = self.dmhis_call
        print(dmhis.__dict__)
        index = int(self.posts_tree.selection()[0])
        entry = dmhis.users[index]
        dmhis.current_user = entry
        print('node')
        print(dmhis.users)
        print(entry)
        dmhis.convo_construct(dmhis.current_user)
        self.conversation(dmhis.conversation)

    def conversation(self, convo: list):
        """constructs and prints the ordered conversation given an ordered list of DM objects"""
        self.set_text_entry('')
        my_color = self.color_choice[0]
        your_color = self.color_choice[1]
        for i in convo:
            if i.recipient == None:
                output = self.username + ':: ' + i.message
                self.entry_editor.insert('end', output + '\n', my_color)
            else:
                output = i.recipient + ':: ' + i.message
                self.entry_editor.insert('end', output + '\n', your_color)
        self.entry_editor.yview_pickplace('end')

    def set_dm(self, dmhis):
        """brings in DMHistory from MainApp"""
        self.dmhis_call = dmhis

    def set_usrname(self, username):
        """brings in username from MainApp"""
        self.username = username

    def get_text_entry(self) -> str:
        """
        Returns the text that is currently displayed in the entry_mess widget.
        """
        return self.entry_mess.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """
        Sets the text to be displayed in the entry_editor widget.
        NOTE: This method is useful for clearing the widget, just pass an empty string.
        """
        self.entry_editor.delete(0.0, 'end')
        self.entry_editor.insert(0.0, text)

    def set_message_entry(self, text: str):
        """
        Sets the text to be displayed in the entry_editor widget.
        NOTE: This method is useful for clearing the widget, just pass an empty string.
        """
        self.entry_mess.delete(0.0, 'end')
        self.entry_mess.insert(0.0, text)

    def set_users(self, users: list):
        """
        Populates the self.users attribute with users from the active DSU file.
        """
        self.users = users
        print(self.users)

        for (i, n) in enumerate(self.users):
            self._insert_post_tree(i, n)

    def insert_user(self, user, his):
        """
        Inserts a single user to the post_tree widget.
        """
        id = len(his.users) - 1  # adjust id for 0-base of treeview widget
        self._insert_post_tree(id, user)
        print('insert user')
        print(his.users)

    def reset_ui(self):
        """
        Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
        as when a new DSU file is loaded, for example.
        """
        self.set_text_entry("")
        self.entry_editor.configure(state=tk.NORMAL)
        # self.entry_editor['state'] = 'disabled'
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    def _insert_post_tree(self, id, user):
        """
        Inserts a user into the posts_tree widget.
        """
        entry = user
        print('entry  ' + entry)
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."

        self.posts_tree.insert('', id, id, text=entry)

    def _draw(self):
        """
            Call only once upon initialization to add widgets to the frame
        """
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="", height=20)
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        ##
        messanger_frame = tk.Frame(master=entry_frame, bg="yellow")
        messanger_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

        self.entry_mess = tk.Text(messanger_frame, height=5)
        self.entry_mess.pack(fill=tk.BOTH, side=tk.LEFT, expand=False, padx=0, pady=0)
        ##

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.entry_editor = tk.Text(editor_frame, width=0, height=20)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)
        self.entry_editor.tag_config('REDD', foreground='red')
        self.entry_editor.tag_config('BLUEE', foreground='blue')
        self.entry_editor.tag_config('BLACKK', foreground='black')
        self.entry_editor.tag_config('GREENN', foreground='green')
        # self.entry_editor['state'] = 'disabled'

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""


class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, online_callback=None, user_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        self.user_callback = user_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using he get() function:
        # chk_value = self.is_online.get()
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance
        self._draw()

    def save_click(self):
        """
        Calls the callback function specified in the save_callback class attribute, if
        available, when the save_button has been clicked.
        """
        if self._save_callback is not None:
            self._save_callback()
        else:
            print('save click')

    def set_status(self, message):
        """
        Updates the text that is displayed in the footer_label widget
        """
        self.footer_label.configure(text=message)

    def _draw(self):
        """
        Call only once upon initialization to add widgets to the frame
        """
        save_button = tk.Button(master=self, text="Send Message", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        ##
        user_button = tk.Button(master=self, text="Add User", width=20)
        user_button.configure(command=self.user_callback)
        user_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)
        ##

        # self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        # self.chk_button.configure(command=self.online_click)
        # self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class MainApp(tk.Frame):
    """
    A subclass of tk.Frame that is responsible for drawing all of the widgets
    in the main portion of the root frame.
    """

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self._is_online = False
        self._profile_filename = None
        self.root = root

        # Initialize a new Profile and assign it to a class attribute.
        self._current_profile = Profile.Profile()
        self.history_profile = Profile.DmHistory([], [])

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    def saveuser(self, win, user, password):
        """saves the username and password to the profile
        :param win: the current window
        :param user: the username
        :param password: the password"""
        self._current_profile.username = user
        self._current_profile.password = password

        self._current_profile.save_profile(self.profile_filename)
        self.history_profile = Profile.DmHistory(self._current_profile.messages, self._current_profile.responses)

        self.body.reset_ui()

        win.destroy()

        print('saveuser')
        print(self._current_profile.username)
        self.body.set_dm(self.history_profile)
        self.body.set_usrname(self._current_profile.username)

    def add_user(self):
        self.popup_add_user()

    def popup_add_user(self):
        """creates the popup window for the user creator"""
        newuse = tk.Toplevel()
        newuse.geometry('200x200')

        # creates the buttons and entry fields for the popup
        name = tk.StringVar()
        label = tk.Label(newuse, text="Username")
        label.pack(pady=5)
        namefield = ttk.Entry(newuse, textvariable=name, width=10)
        namefield.pack()

        done = tk.Button(newuse, text='Submit', command=lambda: self.new_user(newuse, namefield.get()))
        done.pack(pady=10)

    def new_user(self, win, user):
        """adds new user to dmhistory"""
        print(user)
        if user not in self.history_profile.users:
            self.history_profile.users.append(user)
            self.history_profile.current_user = user

            self.body.insert_user(user, self.history_profile)
            self.history_profile.save_to_profile(self._current_profile, self.profile_filename)
            self.all_retriever()
        else:
            self.body.set_text_entry('Conversation already started: select their profile in the sidebar to continue')

        self.body.set_dm(self.history_profile)
        win.destroy()

    def new_profile(self):
        """
        Creates a new DSU file when the 'New' menu item is clicked.
        """
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')],
                                               defaultextension=[('Distributed Social Profile', '*.dsu')])
        self.profile_filename = filename.name
        print(self.profile_filename)

        # sets current profile
        self._current_profile = Profile.Profile()
        self.popup_prof()

    def popup_prof(self):
        """creates the popup window for the profile creator"""
        newuse = tk.Toplevel()
        newuse.geometry('200x200')

        # creates the buttons and entry fields for the popup
        name = tk.StringVar()
        label = tk.Label(newuse, text="Username")
        label.pack(pady=5)
        namefield = ttk.Entry(newuse, textvariable=name, width=10)
        namefield.pack()

        pas = tk.StringVar()
        label2 = tk.Label(newuse, text="Password")
        label2.pack(pady=5)
        namefield2 = ttk.Entry(newuse, textvariable=pas, width=10)
        namefield2.pack()

        done = tk.Button(newuse, text='Submit',
                         command=lambda: self.saveuser(newuse, namefield.get(), namefield2.get()))
        done.pack(pady=10)
        ##

    def open_profile(self):
        """
        Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
        data into the UI.
        """
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        self.profile_filename = filename.name
        self._current_profile = Profile.Profile()
        self._current_profile.load_profile(self.profile_filename)
        self.history_profile = Profile.DmHistory(self._current_profile.messages, self._current_profile.responses)
        self.all_retriever()

        self.body.reset_ui()

        self.body.set_users(self.history_profile.users)
        self.body.set_dm(self.history_profile)
        self.body.set_usrname(self._current_profile.username)
        print(self._current_profile.__dict__)
        print(self.history_profile.__dict__)

    def popup_color(self):
        """creates the popup window for the color chooser"""
        newuse = tk.Toplevel()
        newuse.geometry('700x700')

        color1 = tk.StringVar()
        label = tk.Label(newuse, text="Your text")
        label.pack(pady=5)

        red = tk.Radiobutton(newuse, text='Red', variable=color1, value='REDD')
        red.pack()
        blue = tk.Radiobutton(newuse, text='Blue', variable=color1, value='BLUEE')
        blue.pack()
        black = tk.Radiobutton(newuse, text='Black', variable=color1, value='BLACKK')
        black.pack()
        green = tk.Radiobutton(newuse, text='Green', variable=color1, value='GREENN')
        green.pack()

        color2 = tk.StringVar()
        label = tk.Label(newuse, text="Their text")
        label.pack(pady=5)

        red1 = tk.Radiobutton(newuse, text='Red', variable=color2, value='REDD')
        red1.pack()
        blue1 = tk.Radiobutton(newuse, text='Blue', variable=color2, value='BLUEE')
        blue1.pack()
        black1 = tk.Radiobutton(newuse, text='Black', variable=color2, value='BLACKK')
        black1.pack()
        green1 = tk.Radiobutton(newuse, text='Green', variable=color2, value='GREENN')
        green1.pack()

        done = tk.Button(newuse, text='Done', command=lambda: self.color_closer(color1.get(), color2.get(), newuse))
        done.pack(pady=10)

    def color_closer(self, color1, color2, win):
        """closes color popup and submits colors to Body"""
        self.body.set_colors(color1, color2)
        win.destroy()

    def close(self):
        """
        Closes the program when the 'Close' menu item is clicked.
        """
        self.root.destroy()

    def send_message(self):
        """sends message to recipient when send button is pressed"""

        if self._is_online:
            mess = ds_messenger.DirectMessenger(username=self._current_profile.username,
                                                password=self._current_profile.password)
            print('send mess')

            messag = self.body.get_text_entry()
            print('message', messag, '\nrecipient', self.history_profile.current_user, '\ndmhis',
                  self.history_profile.__dict__)

            mess.send(message=messag, recipient=self.history_profile.current_user, dmhis=self.history_profile)
            self.history_profile.save_to_profile(self._current_profile, self.profile_filename)
            self.body.set_dm(self.history_profile)
            print(self.history_profile.__dict__)
            self.body.set_message_entry('')
        else:
            print('offline1')
            self.body.set_text_entry('Currently Offline: Check your connection')

    def online_changed(self):
        """changes online status checker"""
        chec = ds_messenger.DirectMessenger(username='defaultingcheck', password='password')
        check = chec.online_check()
        if check:
            self.footer.set_status("Online")
        else:
            self.footer.set_status("Offline")

        # flags online status
        self._is_online = check
        self.root.after(5000, self.online_changed)

    def new_retriever(self):
        '''retrieves new messages every 5 sec while online with a loaded user'''
        if self._is_online and self._current_profile.username != None:
            x = ds_messenger.DirectMessenger(username=self._current_profile.username,
                                             password=self._current_profile.password).retrieve_new()
            for i in x:
                print(i.message)
                self.history_profile.serv.append(i)

            self.body.set_dm(self.history_profile)
            self.history_profile.convo_construct(self.history_profile.current_user)
            self.body.conversation(self.history_profile.conversation)
            print('new retrieve')
        self.root.after(1000, self.new_retriever)

    def all_retriever(self):
        if self._is_online:
            x = ds_messenger.DirectMessenger(username=self._current_profile.username,
                                             password=self._current_profile.password).retrieve_all()

            self.history_profile.serv = x

            self.body.set_dm(self.history_profile)
            print('all retrieve')

    def _draw(self):
        """
        Call only once, upon initialization to add widgets to root frame
        """
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)

        color_choice = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=color_choice, label='Settings')
        color_choice.add_command(label='Choose Text Color', command=self.popup_color)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar.

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile, dmhis=self.history_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        # TODO: Add a callback for detecting changes to the online checkbox widget in the Footer class. Follow
        # the conventions established by the existing save_callback parameter.
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, save_callback=self.send_message, online_callback=self.online_changed,
                             user_callback=self.add_user)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        self.online_changed()
        self.new_retriever()


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support.
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()
