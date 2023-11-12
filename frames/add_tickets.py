import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import datetime
from network import client


# custom exception for validation errors
class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class AddTicket(ctk.CTkFrame):
    """add ticket frame"""
    def __init__(self, master, switch_frame, app_state):
        super().__init__(master)
        self.app_state = app_state
        self.switch_frame = switch_frame
        self._create_widgets()

    def _create_widgets(self):
        """create the widgets for the frame"""

        # Add Ticket label
        label = ctk.CTkLabel(self, text="Add Ticket", font=("Roboto", 24))
        label.pack(pady=20, padx=20)

        # Ticket Name label
        label = ctk.CTkLabel(self, text="Ticket Name", font=("Roboto", 16))
        label.pack(pady=3, padx=5)

        # Ticket Name entry
        self.ticket_name_entry = ctk.CTkEntry(self, font=("Roboto", 16))
        self.ticket_name_entry.pack(pady=3, padx=5)

        # Ticket Price label
        label = ctk.CTkLabel(self, text="Ticket Price", font=("Roboto", 16))
        label.pack(pady=3, padx=5)

        # Ticket Price entry
        self.ticket_price_entry = ctk.CTkEntry(self, font=("Roboto", 16))
        self.ticket_price_entry.pack(pady=3, padx=5)

        # Ticket Amount label
        label = ctk.CTkLabel(self, text="Ticket Amount", font=("Roboto", 16))
        label.pack(pady=3, padx=5)

        # Ticket Amount entry
        self.ticket_amount_entry = ctk.CTkEntry(self, font=("Roboto", 16))
        self.ticket_amount_entry.pack(pady=3, padx=5)

        # Ticket Date label
        label = ctk.CTkLabel(self, text="Ticket Date", font=("Roboto", 16))
        label.pack(pady=3, padx=5)

        # Ticket Date entry
        self.ticket_date_entry = ctk.CTkEntry(self, font=("Roboto", 16))
        self.ticket_date_entry.pack(pady=3, padx=5)

        # Add Ticket button
        button = ctk.CTkButton(self, text="Add Ticket", command=self._add_ticket_command)
        button.pack(pady=3, padx=5)

        # Back to admin home button
        button = ctk.CTkButton(self, text="Back to Admin Home", command=self._back_command)
        button.pack(pady=20, padx=20)

    # validate each input and raise a ValidationError if one of them is invalid
    def _validate_input(self):
        try:
            ticket_name = self._validate_ticket_name(self.ticket_name_entry.get())
            ticket_price = self._validate_ticket_price(self.ticket_price_entry.get())
            ticket_amount = self._validate_ticket_amount(self.ticket_amount_entry.get())
            ticket_date = self._validate_ticket_date(self.ticket_date_entry.get())
            return ticket_name, ticket_price, ticket_amount, ticket_date
        except ValidationError as ve:
            # show error message and return None if validation fails
            self._show_error_message(str(ve))
            return None

    def _validate_ticket_name(self, name):
        if not name:
            raise ValidationError("Please enter the ticket name.")
        if len(name) > 25:
            raise ValidationError("Ticket Name must be less than or equal to 25 characters.")
        return name

    def _validate_ticket_price(self, price):
        if not price:
            raise ValidationError("Ticket Price must not be empty.")
        try:
            price = float(price)
            if price <= 99:
                raise ValidationError("Ticket Price must be greater than 99.")
            if price > 1000:
                raise ValidationError("Ticket Price must be less than or equal to 1000.")
        except ValueError:
            raise ValidationError("Ticket Price must be a number.")
        return price

    def _validate_ticket_amount(self, amount):
        if not amount:
            raise ValidationError("Ticket Amount must not be empty.")
        try:
            amount = int(amount)
            if amount <= 15:
                raise ValidationError("Ticket Amount must be greater than 15.")
            if amount > 500:
                raise ValidationError("Ticket Amount must be less than or equal to 500.")
        except ValueError:
            raise ValidationError("Ticket Amount must be a number.")
        return amount

    def _validate_ticket_date(self, date_str):
        if not date_str:
            raise ValidationError("Ticket Date must not be empty.")
        try:
            ticket_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Ticket Date must be in YYYY-MM-DD format.")
        return ticket_date.strftime("%Y-%m-%d")

    def _add_ticket_command(self):
        inputs = self._validate_input()
        if inputs is None:
            return  # Validation failed, message already shown.

        ticket_name, ticket_price, ticket_amount, ticket_date = inputs

        try:
            response = client.add_ticket(ticket_name, ticket_price, ticket_amount, ticket_date)
            if response == "Ticket Added":
                CTkMessagebox(title="Success", message="Ticket added successfully.", icon="info")
            elif response == "Ticket Duplicate":
                self._show_error_message("Ticket already exists.")
            elif response == "Ticket limit reached":
                self._show_error_message("Ticket limit reached. Delete a ticket then try again.")
            else:
                self._show_error_message("An error occurred while adding the ticket.")
        except Exception as e:
            self._show_error_message(f"An error occurred: {e}")

    def _show_error_message(self, message):
        CTkMessagebox(title="Error", message=message, icon="cancel")

    def _back_command(self):
        self.after(0, self.switch_frame, "Admin")

