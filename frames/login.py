import customtkinter as ctk


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
        button.pack(pady=20, padx=20)

    # TODO: implement login functionality
    def _login_command(self):
        print("Login")
