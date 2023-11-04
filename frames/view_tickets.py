import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from network import client
import threading

class ViewTickets(ctk.CTkFrame):
    """View Tickets Frame"""
    def __init__(self, master, switch_frame, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.switch_frame = switch_frame
        self._create_widgets()

    def _create_widgets(self):
        # Welcome label
        label = ctk.CTkLabel(self, text=f"Hi, {self.app_state.username}, here are your current purchased tickets! 🎫",
                             font=("Roboto", 24))
        label.grid(row=0, column=0, columnspan=8, pady=20, padx=20)

        # Currency label
        label = ctk.CTkLabel(self, text=f"You currently have ${self.app_state.currency} credit.",
                             font=("Roboto", 16))
        label.grid(row=1, column=0, columnspan=8, pady=20, padx=5)

        # Fetch and display user tickets
        user_ticket_data = self.fetch_user_ticket_data()
        self._display_tickets(user_ticket_data)

        # Home button
        home_button = ctk.CTkButton(self, text="Home", command=self._home_command)
        home_button.grid(row=20, column=0, columnspan=8, pady=30, padx=20, sticky="s")

    # Fetch user tickets from the client -> server
    def fetch_user_ticket_data(self):
        username = self.app_state.username
        data = client.get_user_tickets(username)

        # Check if the server returned an error message
        if isinstance(data, str) and "error" in data.lower():
            print("Error fetching user tickets:", data)
            CTkMessagebox(title="Error", message="Error fetching user tickets.", icon="cancel")
            return []

            # Attempt to parse the string data into a list of lists
        try:
            # Assuming the data format is a comma-separated string of ticket details
            # and each ticket is separated by a newline
            ticket_data = [ticket.strip().split(', ') for ticket in data.split('\n') if ticket.strip()]
            # Convert each detail into the appropriate type, if necessary
            # For example, if the price should be a float and the quantity an integer
            processed_data = [[detail if index != 1 else float(detail) for index, detail in enumerate(ticket)] for
                              ticket in ticket_data]
            return processed_data
        except Exception as e:
            print(f"Failed to process user ticket data: {e}")
            CTkMessagebox(title="Error", message="Failed to process user ticket data.", icon="cancel")
            return []

    # Display user tickets
    def _display_tickets(self, ticket_data):
        """Displays ticket data in the frame"""
        # Check if the list is empty or contains 'No tickets'
        if not ticket_data or ticket_data == [['No tickets']]:
            label = ctk.CTkLabel(self, text="You have no purchased tickets.", font=("Roboto", 24))
            label.grid(row=3, column=0, columnspan=8, pady=20, padx=20)

            # Buy Tickets button
            buy_button = ctk.CTkButton(self, text="Buy Tickets", command=lambda: self.switch_frame("Buy_Tickets"))
            buy_button.grid(row=4, column=0, columnspan=8, pady=20, padx=20)
            return

        # create labels for each ticket detail
        ctk.CTkLabel(self, text="Event Name", font=("Roboto", 20)).grid(row=2, column=0, pady=20, padx=20)
        ctk.CTkLabel(self, text="Selling Price", font=("Roboto", 20)).grid(row=2, column=1, pady=20, padx=20)
        ctk.CTkLabel(self, text="Amount Owned", font=("Roboto", 20)).grid(row=2, column=2, pady=20, padx=20)

        displayed_tickets = {}
        for ticket_info in ticket_data:
            ticket_id = ticket_info[0]
            if ticket_id in displayed_tickets:
                displayed_tickets[ticket_id][-1] = str(int(displayed_tickets[ticket_id][-1]) + int(ticket_info[-1]))
            else:
                displayed_tickets[ticket_id] = ticket_info

        for row, (ticket_id, ticket_info) in enumerate(displayed_tickets.items(), start=3):  # Start at row 3 to avoid overlapping with labels
            for col, detail in enumerate(ticket_info, start=0):
                detail_label = ctk.CTkLabel(self, text=detail, font=("Roboto", 20))
                detail_label.grid(row=row, column=col, pady=20, padx=20)
            sell_button = ctk.CTkButton(self, text="Sell Ticket",
                                        command=lambda ticket=ticket_info: self._sell_ticket_command(ticket))
            sell_button.grid(row=row, column=len(ticket_info))

    def _home_command(self):
        self.after(0, self.switch_frame, "Home")

    def _sell_ticket_command(self, ticket):
        # Run the selling ticket operation in a separate thread
        thread = threading.Thread(target=self._perform_sell_ticket, args=(ticket,))
        thread.start()

    def _perform_sell_ticket(self, ticket):
        client.sell_ticket(ticket[0], self.app_state.username)
        self.app_state.currency = client.get_currency(self.app_state.username)
        # Schedule switch_frame to be run in the main thread
        self.after(0, lambda: self.switch_frame("View_Tickets"))

