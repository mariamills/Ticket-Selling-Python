import customtkinter as ctk

class Admin(ctk.CTkFrame):
    """admin frame"""
    def __init__(self, master, switch_frame, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.switch_frame = switch_frame
        self._create_widgets()

    def _create_widgets(self):
        """create the widgets for the frame"""

        # Admin Home (Dashboard) label
        label = ctk.CTkLabel(self, text="Admin Dashboard", font=("Roboto", 24))
        label.pack(pady=20, padx=20)

        # Username label
        label = ctk.CTkLabel(self, text=f"Welcome [Admin] {self.app_state.username}", font=("Roboto", 16))
        label.pack(pady=3, padx=5)

        # Add tickets button
        button = ctk.CTkButton(self, text="Add New Ticket", command=self._add_ticket_command)
        button.pack(pady=3, padx=5)

        # Delete ticket button
        button = ctk.CTkButton(self, text="Delete Ticket", command=self._delete_ticket_command)
        button.pack(pady=3, padx=5)

        # Update ticket button
        button = ctk.CTkButton(self, text="Update Ticket", command=self._update_ticket_command)
        button.pack(pady=3, padx=5)

        # Back to regular home button
        button = ctk.CTkButton(self, text="Back to Home", command=self._back_command)
        button.pack(pady=20, padx=20)

    # add ticket command
    def _add_ticket_command(self):
        # after 0ms, switch to the add ticket frame, 'after' is a tkinter method to schedule a function to run on the main GUI thread
        self.after(0, self.switch_frame, "AddTicket")

    # delete ticket command
    def _delete_ticket_command(self):
        # after 0ms, switch to the delete ticket frame
        self.after(0, self.switch_frame, "DeleteTicket")
        print("Switching to delete ticket frame")

    # update ticket command
    def _update_ticket_command(self):
        # after 0ms, switch to the update ticket frame
        self.after(0, self.switch_frame, "UpdateTicket")
        print("Switching to update ticket frame")

    # logout command
    def _back_command(self):
        # after 0ms, switch to the back frame
        self.after(0, self.switch_frame, "Home")
        print("switching back to home frame")