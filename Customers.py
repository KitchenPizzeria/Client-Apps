from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re

class Customers():
    def __init__(self,CustomerWin):
        self.master = CustomerWin

        Headers = ['Firstname', 'Surname',"Company",'Contact Number',"Email","Address","Postcode"]
        frame = Frame(CustomerWin)
        frame.pack(side=BOTTOM)
        self.tree = ttk.Treeview(frame,columns=Headers,show="headings")
        self.tree.grid(row = 0,column=0,in_=frame)
        
        RepeatedFunctions.TreeView(CustomerWin,Headers,self.tree,frame)
        RepeatedFunctions.WindowConfig(CustomerWin,750,487,100,100)
        RepeatedFunctions.ProduceMenuCanvas(CustomerWin,"Clients")
        RepeatedFunctions.ProduceTitleCanvas(CustomerWin,"Clients")
        
        self.ProduceClientEditor(CustomerWin,self.tree)
        self.ProduceAddClientForm(CustomerWin)
        
        CustomerWin.mainloop()
        
    def ProduceClientEditor(self,master,TreeView):

        FilterCanvas = Canvas(master)
        FilterCanvas.place(x=134,y=72, width = 357, height = 187)
        FilterCanvas.create_rectangle(1, 1, 355, 185, fill="#add8e6",width = 3,outline="grey")        
        
        self.CFirstname = Label(FilterCanvas,text = "Firstname: None",bg = "#add8e6")
        self.CFirstname.place(x=210,y=8)
        self.CLastname = Label(FilterCanvas,text = "Lastname: None",bg = "#add8e6")
        self.CLastname.place(x=210,y=28)
        self.CCompany = Label(FilterCanvas,text = "Company: None",bg = "#add8e6")
        self.CCompany.place(x=210,y=48)
        self.CTelephone = Label(FilterCanvas,text = "Telephone: None",bg = "#add8e6")
        self.CTelephone.place(x=210,y=68)
        self.CEmail = Label(FilterCanvas,text = "Email: None",bg = "#add8e6")
        self.CEmail.place(x=210,y=88)
        self.CAddress = Label(FilterCanvas,text = "Address: None",bg = "#add8e6")
        self.CAddress.place(x=210,y=108)
        self.CPostcode = Label(FilterCanvas,text = "Postcode: None",bg = "#add8e6")
        self.CPostcode.place(x=210,y=128)   
        self.AmountOfClients = Label(FilterCanvas,text ="Amount of Clients: 0",bg = "#add8e6")
        self.AmountOfClients.place(x=40,y=128)

        self.ShowRecordsButton = ttk.Button(FilterCanvas,text = "Show clients",command = self.DisplayAllRecords)
        self.ShowRecordsButton.place(x=21,y=155)

        self.SelectRecord = ttk.Button(FilterCanvas,text = "Select",command = self.SelectClient)
        self.SelectRecord.place(x=101,y=155)

        self.RemoveClient = ttk.Button(FilterCanvas,text = "Delete",state=DISABLED,command = self.DeleteClient)
        self.RemoveClient.place(x=180,y=155)

        self.EditClient = ttk.Button(FilterCanvas,text="Edit info",state=DISABLED,command = self.OpenEditForm)
        self.EditClient.place(x=260,y=155)