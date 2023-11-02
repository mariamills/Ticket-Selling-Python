import customtkinter as ctk
from network import client

class Home(ctk.CTkFrame):
    """home frame"""
    def __init__(self, master, switch_frame, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.switch_frame = switch_frame
        self._create_widgets()

    def _create_widgets(self):
        """create the widgets for the frame"""

        # Home (Dashboard) label
        label = ctk.CTkLabel(self, text="Dashboard", font=("Roboto", 24))
        label.pack(pady=20, padx=20)

        # Username label
        label = ctk.CTkLabel(self, text=f"Welcome {self.app_state.username}! \n\nYou currently have ${self.app_state.currency} dollars.", font=("Roboto", 16))
        label.pack(pady=20, padx=5)

        # Buy tickets button
        button = ctk.CTkButton(self, text="Buy Tickets", command=self._buy_tickets_command)
        button.pack(pady=3, padx=5)

        # View tickets button
        button = ctk.CTkButton(self, text="View My Tickets", command=self._view_tickets_command)
        button.pack(pady=20, padx=20)

        # Admin Panel button - only show if the user is an admin
        self._update_ui_for_admin()

        # Logout button
        button = ctk.CTkButton(self, text="Logout", command=self._logout_command)
        button.pack(pady=20, padx=20)

    # Admin Home (Dashboard) label
    def _update_ui_for_admin(self):
        if self.app_state.is_admin:
            button = ctk.CTkButton(self, text="Admin Dashboard", command=self._admin_command)
            button.pack(pady=20, padx=20)

    def _admin_command(self):
        self.after(0, self.switch_frame, "Admin")
        print("Switching to admin frame")


    # buy ticket command
    def _buy_tickets_command(self):
        # after 0ms, switch to the buy ticket frame, 'after' is a tkinter method to schedule a function to run on the main GUI thread
        self.after(0, self.switch_frame, "Buy_Tickets")
        print("Switching to buy ticket frame")

    # view ticket command
    def _view_tickets_command(self):
        # after 0ms, switch to the view ticket frame
        self.after(0, self.switch_frame, "View_Tickets")
        print("Switching to view ticket frame")

    # logout command
    def _logout_command(self):
        # after 0ms, switch to the login frame
        self.after(0, self.switch_frame, "Login")
        print("Logout successful - switching to login frame")
        client.logout()