import customtkinter as ctk
from frames.login import Login
from frames.home import Home
from frames.register import Register
from frames.view_tickets import View_tickets

WINDOW_SIZE = "700x500"

class AppState:
    """class to hold the state of the application"""
    def __init__(self):
        self.username = None  # Current username
        self.frames = {'Login': Login, 'Home': Home, 'Register': Register, "View_Tickets": View_tickets}  # Available frames

def switch_frame(frame_name):
    """switch to a different frame"""
    # clear the container
    for widget in container_frame.winfo_children():
        widget.destroy()

    # load the new frame
    frame_class = app_state.frames.get(frame_name)
    if frame_class:
        frame_instance = frame_class(container_frame, switch_frame, app_state)
        frame_instance.place(relx=0.5, rely=0.5, anchor='c')

# initialize app state
app_state = AppState()

# set up the root window appearance and theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# create the root window and set its title and size
root = ctk.CTk()
root.title("Ticket System")
root.geometry(WINDOW_SIZE)

# main container for frames (packs into root)
container_frame = ctk.CTkFrame(root)
container_frame.pack(fill='both', expand=True)

# start with the login frame initially
switch_frame("Login")

# run the main event loop (tkinter)
root.mainloop()

"""2 for loop and creat labels with for loop
put the purchase """