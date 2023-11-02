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
        ticket_data = self._fetch_ticket_data()
        self._display_tickets(ticket_data)

        label = ctk.CTkLabel(self, text="🎟️Available Tickets for purchase 🎟️", font=("Roboto", 24))
        label.grid(row=0, column=0, columnspan=6, pady=20, padx=20)

        # Home button
        home_button = ctk.CTkButton(self, text="Home", command=self._home_command)
        home_button.grid(row=20, column=0, columnspan=6, pady=30, padx=20, sticky="s")

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
        # create labels for each ticket detail
        ctk.CTkLabel(self, text="Event Name", font=("Roboto", 20)).grid(row=1, column=0, pady=20, padx=20)
        ctk.CTkLabel(self, text="Price", font=("Roboto", 20)).grid(row=1, column=1, pady=20, padx=20)
        ctk.CTkLabel(self, text="Amount Available", font=("Roboto", 20)).grid(row=1, column=2, pady=20, padx=20)
        ctk.CTkLabel(self, text="Date", font=("Roboto", 20)).grid(row=1, column=3, pady=20, padx=20)

        for row, ticket_info in enumerate(ticket_data, start=2):  # Start from row 2
            # display ticket details in labels
            for col, detail in enumerate(ticket_info[1:], start=0):
                detail_label = ctk.CTkLabel(self, text=detail, font=("Roboto", 20))
                detail_label.grid(row=row, column=col, pady=20, padx=20)

            # create a button for buying the ticket
            buy_button = ctk.CTkButton(self, text="Buy Ticket",
                                       command=lambda ticket=ticket_info: self._buy_ticket_command(ticket))
            buy_button.grid(row=row, column=4, padx=10)

    def _home_command(self):
        self.after(0, self.switch_frame, "Home")
        print("Switching to home frame")

    def _buy_ticket_command(self, ticket):
        client.buy_ticket(ticket[0], self.app_state.username)
        self.app_state.currency = client.get_currency(self.app_state.username)
        print("Buying ticket:", ticket)
