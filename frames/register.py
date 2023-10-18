import customtkinter as ctk
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
        label.pack(pady=20, padx=20)

        # Username entry
        self.entry1 = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry1.pack(pady=10, padx=30)

        # Password entry
        self.entry2 = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry2.pack(pady=10, padx=30)

        # Register button
        button = ctk.CTkButton(self, text="Register", command=self._register_command)
        button.pack(pady=10, padx=20)

        # Login button
        button = ctk.CTkButton(self, text="Back to Login", command=self._login_command)
        button.pack(pady=10, padx=20)

    # register operation (threaded)
    def register_operation(self):
        # get the username and password from the entries
        username = self.entry1.get()
        password = self.entry2.get()

        # send the username and password to the server
        response = client.register(username, password)

        # print the response (testing)
        print("response:", response)

        # if register successful, switch to the login frame (testing)
        if response == "Register successful":
            # after 0ms, switch to the login frame, 'after' is a tkinter method to schedule a function to run on the main GUI thread
            self.after(0, self.switch_frame, "Login")
            print("Register successful - switching to login frame")
        else:
            # TODO: add validation & show a message box saying that the register failed
            print("MessageBox: Register failed")


    def _register_command(self):
        threading.Thread(target=self.register_operation()).start()

    def _login_command(self):
        self.after(0, self.switch_frame, "Login")
        print("Switching to login frame")
