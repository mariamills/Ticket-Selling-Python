import customtkinter as ctk
import threading
from network import client

class Login(ctk.CTkFrame):
    """login frame"""
    def __init__(self, master, switch_frame, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.switch_frame = switch_frame

        self._create_widgets()

    def _create_widgets(self):
        """create the widgets for the frame"""

        # Login label
        label = ctk.CTkLabel(self, text="Login", font=("Roboto", 24))
        label.pack(pady=20, padx=20)

        # Username entry
        self.entry1 = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry1.pack(pady=10, padx=30)

        # Password entry
        self.entry2 = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry2.pack(pady=10, padx=30)

        # Login button
        button = ctk.CTkButton(self, text="Login", command=self._login_command)
        button.pack(pady=10, padx=20)

        # Register button
        button = ctk.CTkButton(self, text="Register", command=self._register_command)
        button.pack(pady=10, padx=20)

    # login operation (threaded)
    def login_operation(self):
        # get the username and password from the entries
        username = self.entry1.get()
        password = self.entry2.get()

        # send the username and password to the server
        response = client.login(username, password)

        # print the response (testing)
        print("response:", response)

        # if login successful, switch to the home frame (testing)
        if response == "Login successful":
            self.app_state.username = username
            self.app_state.currency = client.get_currency(username)
            # check if the user is an admin
            if client.admin_check(username) == "ADMIN":
                self.app_state.is_admin = True
            # after 0ms, switch to the home frame, 'after' is a tkinter method to schedule a function to run on the main GUI thread
            self.after(0, self.switch_frame, "Home")
            print("Login successful - switching to home frame")
        else:
            # TODO: show a message box saying that the login failed
            print("MessageBox: Login failed")

    # login command
    def _login_command(self):
        # start the login operation in a new thread (to avoid GUI freezing)
        threading.Thread(target=self.login_operation).start()

    # register command
    def _register_command(self):
        # after 0ms, switch to the register frame
        self.after(0, self.switch_frame, "Register")
        print("Switching to register frame")


