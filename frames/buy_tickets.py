import customtkinter as ctk
from network import client

class BuyTickets(ctk.CTkFrame):
    """Buy Tickets Frame"""
    def __init__(self, master, switch_frame, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.switch_frame = switch_frame
        self._create_widgets()

    def _create_widgets(self):
        label = ctk.CTkLabel(self, text="Available Tickets", font=("Roboto", 24))
        label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        ticket_data = self._fetch_ticket_data()
        self._display_tickets(ticket_data)

        # Home button
        home_button = ctk.CTkButton(self, text="Home", command=self._home_command)
        home_button.grid(row=20, column=len(ticket_data)+1, pady=30, padx=20, sticky="s")

    def _fetch_ticket_data(self):
        data = client.get_tickets()
        processed_data = []
        # split the data into a list of tuples (each tuple is a row)
        for entry in data.split("),"):
            # remove the extra characters from each entry
            processed_entry = entry.strip(" [()]").replace("'", "")
            # split the entry into a list of items (each item is a column)
            processed_data.append(processed_entry.split(", "))
        return processed_data

    def _display_tickets(self, ticket_data):
        for row_num, ticket_info in enumerate(ticket_data, start=1):
            # create a button for buying the ticket
            # and pass the ticket info to the command with a lambda function - without the lambda, command was being called immediately
            buy_button = ctk.CTkButton(self, text="Buy Ticket",
                                       command=lambda ticket=ticket_info: self._buy_ticket_command(ticket))
            buy_button.grid(row=row_num, column=len(ticket_info))

            # display ticket details in labels
            for col_num, detail in enumerate(ticket_info[1:], start=1):  # Skip the first item (event_id)
                detail_label = ctk.CTkLabel(self, text=detail, font=("Roboto", 20))
                detail_label.grid(row=row_num, column=col_num, pady=20, padx=20)

    def _home_command(self):
        self.after(0, self.switch_frame, "Home")
        print("Switching to home frame")

    def _buy_ticket_command(self, ticket):
        print("Buying ticket:", ticket)
