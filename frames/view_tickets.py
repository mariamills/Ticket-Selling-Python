import customtkinter as ctk
from network import client


class View_tickets(ctk.CTkFrame):
    """view tickets frame"""


    def __init__(self, master, switch_frame, app_state):
        super().__init__(master)
        self.app_state =app_state
        self.switch_frame = switch_frame

        self._create_widgets()

    def _create_widgets(self):
        
        label = ctk.CTkLabel(self, text="Available Tickets", font=("Roboto", 24))
        label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        data = client.view_tickets()

        #counters used in the loop, x used for rows and y is used for columns. Variable "count" is used in the second for loop
        x=1
        y=1
        count = 0

        splitData = data.split("),")
        newData = splitData[0].replace("[(", "").replace(")", "").replace("'", "").split(", ")

        #used for testing
        # for j in newData:
        #     label2 = ctk.CTkLabel(self, text=j, font=("Roboto", 20))
        #     label2.grid(row = x, column =y, columnspan=1, pady = 20, padx=20)
        #     y=y+1

        #print(newData[0])
        # i = 1
        # for i in newData:
        #      print(i)
        
        # for i in splitData:
        #     label1 = ctk.CTkButton(self, text=x, )
        #     label1.grid(row =x)
        #     label2 = ctk.CTkLabel(self, text=i, font=("Roboto", 20))
        #     label2.grid(row = x, column =1, columnspan=1, pady = 20, padx=20)
        #     x = x +1


        #this is a double for loop that will loop through data received from the server. The data is original received as a list, with each concert being an entry.
        #the first loop will loop through the original data and is split by "),". After splitting all entries, we then slit the individual entry itself by "," and replace unnecessary
        #character with a empty string. 
        for i in splitData:
            label1 = ctk.CTkButton(self, text=x, )
            label1.grid(row =x)

            newData = splitData[count].replace("[", "").replace("(","").replace(")", "").replace("]","").replace("'", "").split(", ")
            for j in newData:
                label2 = ctk.CTkLabel(self, text=j, font=("Roboto", 20))
                label2.grid(row = x, column =y, columnspan=1, pady = 20, padx=20)
                y=y+1
            
            count = count + 1
            x = x +1
            y=1
        


            
            

            





        



        # Home button
        button = ctk.CTkButton(self, text="Home", command=self._home_command)
        button.grid(row=20, column=1, columnspan=1, pady=10, padx=20)



    def _view_tickets_command(self):
        self.after(0, self.switch_frame, "View_Tickets")
        print("Switching to view tickets frame")

    def _home_command(self):
        self.after(0, self.switch_frame, "Home")
        print("Switching to home frame")