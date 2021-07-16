from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re

from HomeWindow import Parent

class Sales(Parent):
    def __init__(self,master):
        self.master = master

        Headers = ['Firstname', 'Surname',"Category",'Description',"Unit Price","Quantity","Total"]
        frame = Frame(master)
        frame.pack(side = BOTTOM)
        master.Tree = ttk.Treeview(frame,columns=Headers,show="headings")
        master.Tree.grid(row = 0,column=0,in_=frame)

        self.WindowConfig(master,750,487,100,100)
        self.ProduceTitleCanvas(master,"Sales")
        self.ProduceMenuCanvas(master,"Sales")
        self.TreeView(master,Headers,Sales.Tree,frame)
        
        self.SalesFilterDisplayBox(master)
        self.AddSalesForm(master)
        self.Receipt(master)

        master.mainloop()

    def SalesFilterDisplayBox(Sales,master):
        FilterCanvas = Canvas(master)
        FilterCanvas.place(x=140,y=72, width = 328, height = 187)
        FilterCanvas.create_rectangle(1, 1, 326, 185, fill="#add8e6",width = 3,outline="grey")        