import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
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

    def post_login_operations(self, username):
        self.app_state.username = username
        self.app_state.currency = client.get_currency(username)
        if client.admin_check(username) == "ADMIN":
            self.app_state.is_admin = True
        self.after(0, self.switch_frame, "Home")

    # login operation (threaded)
    def login_operation(self):
        # get the username and password from the entries
        username = self.entry1.get()
        password = self.entry2.get()

        if not username or not password:
            CTkMessagebox(title="Alert", message="Please enter a username and password.", icon="warning")
            return

        # send the username and password to the server
        response = client.login(username, password)

        # if login successful, switch to the home frame
        if response == "Login successful":
            threading.Thread(target=self.post_login_operations, args=(username,)).start()
        elif "Receive failed" in response:
            CTkMessagebox(title="Error", message="Server is offline.", icon="error")
        else:
            CTkMessagebox(title="Alert", message="Incorrect Credentials. Login Failed.", icon="warning")

    # login command
    def _login_command(self):
        # start the login operation in a new thread (to avoid GUI freezing)
        threading.Thread(target=self.login_operation).start()

    # register command
    def _register_command(self):
        # after 0ms, switch to the register frame
        self.after(0, self.switch_frame, "Register")


