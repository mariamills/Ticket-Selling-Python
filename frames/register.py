import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import threading
from network import client

class Register(ctk.CTkFrame):
    """register frame"""

    def __init__(self, master, switch_frame, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.switch_frame = switch_frame

        self._create_widgets()

    def _create_widgets(self):
        """create the widgets for the frame"""

        # Register label
        label = ctk.CTkLabel(self, text="Register an account", font=("Roboto", 24))
        label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # First name entry
        self.entry1 = ctk.CTkEntry(self, placeholder_text="First name")
        self.entry1.grid(row=1, column=0, pady=10, padx=30)

        # Last name entry
        self.entry2 = ctk.CTkEntry(self, placeholder_text="Last name")
        self.entry2.grid(row=1, column=1, pady=10, padx=30)

        # Email entry
        self.entry3 = ctk.CTkEntry(self, placeholder_text="Email")
        self.entry3.grid(row=2, column=0, pady=10, padx=30)

        # Username entry
        self.entry4 = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry4.grid(row=2, column=1, pady=10, padx=30)

        # Password entry
        self.entry5 = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry5.grid(row=3, column=0, pady=10, padx=30)

        # Password confirm entry
        self.entry6 = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*")
        self.entry6.grid(row=3, column=1, pady=10, padx=30)

        # Register button
        button = ctk.CTkButton(self, text="Register", command=self._register_command)
        button.grid(row=4, column=0, columnspan=2, pady=(50, 10), padx=20)

        # Login button
        button = ctk.CTkButton(self, text="Back to Login", command=self._login_command)
        button.grid(row=5, column=0, columnspan=2, pady=10, padx=20)

    # register validation
    def register_validation(self):
        # get the data from the entries (first name, last name, email, username, password)
        first_name = self.entry1.get()
        last_name = self.entry2.get()
        email = self.entry3.get()
        username = self.entry4.get()
        password = self.entry5.get()
        confirm_password = self.entry6.get()

        # check if any of the entries are empty
        if first_name == "" or last_name == "" or email == "" or username == "" or password == "" or confirm_password == "":
            CTkMessagebox(title="Alert", message="All fields must be filled.", icon="warning")
            return False

        # check if the password and confirm password match
        if password != confirm_password:
            CTkMessagebox(title="Alert", message="Passwords do not match.", icon="warning")
            return False

        # check if password is at least 8 characters long
        if len(password) < 8:
            CTkMessagebox(title="Alert", message="Password must be at least 8 characters long.", icon="warning")
            return False

        # check if password is less than 64 characters long
        if len(password) > 64:
            CTkMessagebox(title="Alert", message="Password must be less than 64 characters long.", icon="warning")
            return False

        # check if user is less than 15 characters long
        if len(username) > 15:
            CTkMessagebox(title="Alert", message="Username must be less than 15 characters long.", icon="warning")
            return False

        # check if email is valid
        if "@" not in email or "." not in email:
            CTkMessagebox(title="Alert", message="Invalid email.", icon="warning")
            return False

        return True

    # register operation (threaded)
    def register_operation(self):
        # check if the entries are valid
        if not self.register_validation():
            return

        # get the data from the entries (first name, last name, email, username, password)
        first_name = self.entry1.get()
        last_name = self.entry2.get()
        email = self.entry3.get()
        username = self.entry4.get()
        password = self.entry5.get()

        # send the username and password to the server
        response = client.register(first_name, last_name, email, username, password)

        # if register successful, switch to the login frame (testing)
        if response == "Register successful":
            # after 0ms, switch to the login frame, 'after' is a tkinter method to schedule a function to run on the main GUI thread
            self.after(0, self.switch_frame, "Login")
        else:
            CTkMessagebox(title="Error", message="Registration failed. Try again.", icon="error")


    def _register_command(self):
        threading.Thread(target=self.register_operation()).start()

    def _login_command(self):
        self.after(0, self.switch_frame, "Login")
