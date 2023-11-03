import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
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

        # Available Tickets for purchase label
        label = ctk.CTkLabel(self, text="🎟️Available Tickets for purchase 🎟️", font=("Roboto", 24))
        label.grid(row=0, column=0, columnspan=8, pady=20, padx=20)

        # Currency label
        label = ctk.CTkLabel(self, text=f"You currently have ${self.app_state.currency} credit.",
                             font=("Roboto", 16))
        label.grid(row=1, column=0, columnspan=8, pady=20, padx=5)

        # Home button
        home_button = ctk.CTkButton(self, text="Home", command=self._home_command)
        home_button.grid(row=20, column=0, columnspan=8, pady=30, padx=20, sticky="s")

    def _fetch_ticket_data(self):
        """Fetches ticket data from client (-> server) and returns it as a list of tuples"""
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
        """Displays ticket data in the frame"""
        # create labels for each ticket detail
        ctk.CTkLabel(self, text="Event Name", font=("Roboto", 20)).grid(row=2, column=0, pady=20, padx=20)
        ctk.CTkLabel(self, text="Price", font=("Roboto", 20)).grid(row=1, column=2, pady=20, padx=20)
        ctk.CTkLabel(self, text="Amount Available", font=("Roboto", 20)).grid(row=2, column=2, pady=20, padx=20)
        ctk.CTkLabel(self, text="Date", font=("Roboto", 20)).grid(row=2, column=3, pady=20, padx=20)

        # for each ticket (row) in the data
        for row, ticket_info in enumerate(ticket_data, start=3):  # start at row 3 to avoid overlapping with labels
            # for each ticket detail (column) in the data (except the id)
            for col, detail in enumerate(ticket_info[1:], start=0):  # start at col 0
                # create a label for the ticket detail and add to the grid
                detail_label = ctk.CTkLabel(self, text=detail, font=("Roboto", 20))
                detail_label.grid(row=row, column=col, pady=20, padx=20)

            # create a button for buying the ticket at the end of the row (ticket)
            buy_button = ctk.CTkButton(self, text="Buy Ticket",
                                       command=lambda ticket=ticket_info: self._buy_ticket_command(ticket))
            buy_button.grid(row=row, column=4, padx=10)

    def _home_command(self):
        self.after(0, self.switch_frame, "Home")

    def _buy_ticket_command(self, ticket):
        response = client.buy_ticket(ticket[0], self.app_state.username)

        if response == "Insufficient funds":
            CTkMessagebox(title="Error", message="Insufficient funds.", icon="cancel")
        else:
            self.app_state.currency = client.get_currency(self.app_state.username)
            # TODO: Is there a better way to update the currency label? (i.e. refresh the frame)
            self.after(0, self.switch_frame, "Buy_Tickets")
            print("Buying ticket:", ticket)
