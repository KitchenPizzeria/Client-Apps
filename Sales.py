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

        master.config(bg="#ffca00")
        master.resizable(0,0)
        master.geometry('%dx%d' % (750, 487))

        Headers = ['Firstname', 'Surname',"Category",'Description',"Unit Price","Quantity","Total"]
        frame = Frame(master)
        frame.pack(side = BOTTOM)
        self.tree = ttk.Treeview(frame,columns=Headers,show="headings")
        self.tree.grid(row = 0,column=0,in_=frame)

        self.TreeView(Headers,self.tree,frame)
        
        self.SalesFilterDisplayBox(master)
        self.AddSalesForm(master)
        #self.Receipt(master)

    def SalesFilterDisplayBox(self,master):
        FilterCanvas = Canvas(master)
        FilterCanvas.place(x=140,y=72, width = 328, height = 187)
        FilterCanvas.create_rectangle(1, 1, 326, 185, fill="#add8e6",width = 3,outline="grey")   
    
    def AddSalesForm(self, master):
    
        AddSaleCanvas = Canvas(master)
        AddSaleCanvas.place(x=400, y=50, width = 315, height = 220)
        AddSaleCanvas.create_rectangle(1, 1, 1000, 1000, fill="#add8e6",width = 3,outline="grey")

        QuickAddFrame = LabelFrame(AddSaleCanvas,bg="#add8e6",bd=0)
        QuickAddFrame.place(x=6,y=7)

        Label(QuickAddFrame, text="Company", bg="#add8e6").grid(row=0)
        Label(QuickAddFrame, text="Client", bg="#add8e6").grid(row=1)
        Label(QuickAddFrame, text="Category", bg="#add8e6").grid(row=2)
        Label(QuickAddFrame, text="Item", bg="#add8e6").grid(row=3)
        Label(QuickAddFrame, text = "Quantity", bg="#add8e6").grid(row=4)
        Label(QuickAddFrame, text = "Unit Price", bg="#add8e6").grid(row=5)
        Label(QuickAddFrame, text = "Total", bg="#add8e6").grid(row=6)
        
        Sales.Item = ttk.Combobox(QuickAddFrame, state = DISABLED, width = 20)
        Sales.Name = ttk.Combobox(QuickAddFrame, state = DISABLED, width = 20)

        db = sqlite3.connect("Customers.db")
        Link = db.cursor()

        Sales.Company = ttk.Combobox(QuickAddFrame, width = 20)
        Companies = db.execute("SELECT Company FROM Customers")
        CompanyValues = []
        for x in Companies:
            if max(x) != "":
                CompanyValues.append(max(x))
        CompanyValues = sorted(list(set(CompanyValues)))
        Sales.Company["values"] = CompanyValues
        
        Sales.Company.bind("<Configure>",Parent.CheckWidth(CompanyValues))
        Sales.Company.bind("<<ComboboxSelected>>",Sales.ActivateAndFillNameBox)
        
        Sales.Category = ttk.Combobox(QuickAddFrame,width = 20)
        Categories = db.execute("SELECT Category FROM Inventory")
        StockCat = []
        for x in Categories:
            if max(x) != "" or max(x)!="None":
                StockCat.append(max(x))
        StockCat = sorted(list(set(StockCat)))
        Sales.Category["values"] = StockCat

        Sales.Category.bind("<Configure>",Parent.CheckWidth(StockCat))
        Sales.Category.bind("<<ComboboxSelected>>",Sales.ActivateAndFillItemBox)

        Sales.Quantity = ttk.Entry(QuickAddFrame,width = 20)
        Sales.UnitPrice = Label(QuickAddFrame,bg="#add8e6")  
        Sales.Total = Label(QuickAddFrame,bg="#add8e6")  
        Sales.StateLabel = Label(QuickAddFrame,width = 10,bg="#add8e6")
        Sales.UniqueIDRepeat = True
        Sales.AddSale = ttk.Button(QuickAddFrame,text="Add Sale",command = lambda: Sales.CheckandConfirm(QuickAddFrame,Sales.UniqueIDRepeat))
        Sales.Confirm = ttk.Button(QuickAddFrame,state=DISABLED,text = "Confirm")

        Sales.Company.grid(row = 0,column=1,columnspan = 2)
        Sales.Name.grid(row = 1,column=1,columnspan = 2)
        Sales.Category.grid(row = 2,column=1,columnspan = 2)
        Sales.Item.grid(row = 3,column=1,columnspan = 2)
        Sales.Quantity.grid(row = 4,column=1,columnspan = 2)
        Sales.UnitPrice.grid(row = 5,column =1)
        Sales.Total.grid(row = 6,column=1)
        Sales.AddSale.grid(row=7,padx = 1)
        Sales.Confirm.grid(row=7,column=1,padx=1)
        Sales.StateLabel.grid(row = 7,column=2,padx=1)
    


root = Tk()
Sales(root)
root.mainloop()     