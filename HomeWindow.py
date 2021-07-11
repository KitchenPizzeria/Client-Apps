from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re
from RepeatedFunctions import RepeatedFunctions

BUTTON_FONT = ("Georgia",16)
TITLE_FONT = ("Georgia",28)

class Parent(RepeatedFunctions):
    def __init__(self,master):
        self.master = master
        self.WindowConfig(master,738,260,(master.winfo_screenwidth()-738)/2,(master.winfo_screenheight()-260)/2)
        self.ProduceMenuCanvas(master,"Parent")
        self.PlaceSaleQuickAddBox(master)
        self.PlaceDescription(master)

        master.mainloop()
        
    def PlaceSaleQuickAddBox(Parent,master):

        SideCanvas = Canvas(master,bg="#d8bfd8")
        SideCanvas.place(x=496,y=2,width=240,height=230)
        
        AddSaleCanvas = Canvas(SideCanvas)
        AddSaleCanvas.place(x=4,y=36, width = 232, height = 190)
        AddSaleCanvas.create_rectangle(1, 1, 230, 188, fill="#add8e6",width = 3,outline="grey")

        QuickAddFrame = LabelFrame(AddSaleCanvas,bg="#add8e6",bd=0)
        QuickAddFrame.place(x=6,y=7)
        Label(SideCanvas,text = "Sale Quick Add",bg="#d8bfd8",font = BUTTON_FONT).pack(anchor="n",pady=5)
        Label(QuickAddFrame, text="Company",bg="#add8e6").grid(row=0)
        Label(QuickAddFrame, text="Product Desc.",bg="#add8e6").grid(row=1)
        Label(QuickAddFrame, text="Quantity",bg="#add8e6").grid(row=2)
        Label(QuickAddFrame, text="Unit Price",bg="#add8e6").grid(row=3)
        Label(QuickAddFrame, text = "Gross Total",bg="#add8e6").grid(row=4)
        Label(QuickAddFrame, text = "Net Total",bg="#add8e6").grid(row=5)
        Label(QuickAddFrame, text = "Vat",bg="#add8e6").grid(row=6)

        Parent.Item = ttk.Combobox(QuickAddFrame,state = DISABLED,width = 6)
        Parent.Name = ttk.Combobox(QuickAddFrame,state = DISABLED,width = 6)

        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()

        Parent.Company = ttk.Combobox(QuickAddFrame,width = 6)
        Companies = db.execute("SELECT Company FROM Customers")
        CompanyValues = []
        for x in Companies:
            if max(x) != "":
                CompanyValues.append(max(x))
        CompanyValues = sorted(list(set(CompanyValues)))
        Parent.Company["values"] = CompanyValues

        Parent.Company.bind("<<ComboboxSelected>>",Parent.ActivateAndFillNameBox)

        Categories = db.execute("SELECT Category FROM Inventory")
        StockCat = []
        for x in Categories:
            if max(x) != "" or max(x)!="None":
                StockCat.append(max(x))
        Parent.Category = ttk.Combobox(QuickAddFrame,width = 6)
        StockCat = sorted(list(set(StockCat)))
        Parent.Category["values"] = StockCat

        Parent.Category.bind("<Configure>",RepeatedFunctions.CheckWidth(StockCat))
        Parent.Category.bind("<<ComboboxSelected>>",Parent.ActivateAndFillItemBox)
           
        Parent.Quantity = Entry(QuickAddFrame)
        Parent.UnitPrice = Label(QuickAddFrame,bg="#add8e6") 
        Parent.Gross = Label(QuickAddFrame,bg="#add8e6")  
        Parent.NetTotal = Label(QuickAddFrame,bg="#add8e6")  
        Parent.Vat = Label(QuickAddFrame,bg="#add8e6")
        Parent.StateLabel = Label(QuickAddFrame,bg="#add8e6")

        Parent.Company.place(x=82,y=0)
        Parent.Name.place(x=142,y=0)
        Parent.Category.place(x=82,y=21)
        Parent.Item.place(x=142,y=21)
        Parent.Quantity.grid(row=2, column=1)
        Parent.UnitPrice.grid(row=3, column=1)
        Parent.Gross.grid(row = 4,column=1)
        Parent.NetTotal.grid(row = 5,column=1)
        Parent.Vat.grid(row = 6,column=1)
        Parent.StateLabel.grid(row = 7,column=1)
        
        Parent.AddSale = ttk.Button(QuickAddFrame,text="Add Sale",command = lambda: Parent.CheckandConfirm(QuickAddFrame))
        Parent.AddSale.grid(row=7)
        
    def PlaceDescription(Parent,master):
        
        TextCanvas = Canvas(master)
        TextCanvas.place(x=119,y=113, width = 375, height = 146)
        TextCanvas.create_rectangle(1, 1, 373, 144, fill="#add8e6",width = 3,outline="grey")
        
        Text = '''Client/Stock Management system
Clients --> Edit 
Sales --> Show/Add/Edit/Delete/Filter the sales that clients make
Coal/Sticks/Logs --> Show/Add/Edit/Delete/Filter the CSL orders

You can also create the invoices when ready <-- This
needs touching up 
'''
        Label(TextCanvas,text = Text,font = ("Georgia",15),bg = "#add8e6").place(x=3,y=3)

    def ActivateAndFillItemBox(Parent,event):
        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()

        Parent.StockItems = []
        StockDesc = db.execute("SELECT Description FROM Inventory WHERE Category = '%s'"%Parent.Category.get())
        for x in StockDesc:
            if max(x) != "":
                Parent.StockItems.append(max(x))
        Parent.StockItems = sorted(list(set(Parent.StockItems)))
        Parent.Item["values"] = Parent.StockItems
        Parent.Item.config(state = NORMAL)
        RepeatedFunctions.CheckWidth(Parent.StockItems)
            
    def ActivateAndFillNameBox(Parent,event):
        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()
        
        Parent.Names = []
        Names = db.execute("SELECT Firstname,Surname FROM Customers WHERE Company = '%s'"%Parent.Company.get())
        for x in Names:
            Name = x[0]+" "+x[1]
            if max(x)!="":
                Parent.Names.append(Name)
            
        Parent.Names = sorted(list(set(Parent.Names)))
        Parent.Name["values"] = Parent.Names
        Parent.Name.config(state=ACTIVE)
        RepeatedFunctions.CheckWidth(Parent.Names)

    def CheckandConfirm(Parent,QuickAddFrame):
        db = sqlite3.connect("Customers db.db")
        c = db.cursor()
        c.execute("SELECT * FROM Inventory")
        result = c.fetchall() 
        for Record in result:
            if Record[2] == Parent.Item.get():
                fetchPrice = float(Record[3])
                                
        try:
            fetchQuan = float(Parent.Quantity.get())
            TotalPriceMoney = Decimal(str(fetchQuan*fetchPrice)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            NetMoney = Decimal(str(fetchQuan*fetchPrice*0.8)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            VatMoney = TotalPriceMoney - NetMoney
            if fetchQuan > 0 and fetchPrice > 0:
                
                Parent.UnitPrice.config(text = "£ "+str(fetchPrice))
                Parent.Gross.config(text ="£ "+ str(TotalPriceMoney))
                Parent.NetTotal.config(text = "£ "+ str(NetMoney))
                Parent.Vat.config(text = "£ "+ str(VatMoney))

                Parent.Company.config(state = DISABLED)
                Parent.Name.config(state = DISABLED)
                Parent.Category.config(state = DISABLED)
                Parent.Item.config(state = DISABLED)
                Parent.Quantity.config(state = DISABLED)
                
                Parent.Confirm = ttk.Button(QuickAddFrame,text = "Confirm Sale",command =
                                            lambda:Parent.AddRecordToSalesDatabase(QuickAddFrame))
                Parent.Confirm.grid(row=7,column=1)
                Parent.AddSale.config(text = "Edit",command = lambda:Parent.AddNew(QuickAddFrame))
            else:
                Parent.StateLabel.config(text="**Error**",fg="red")
        except:
          Parent.StateLabel.config(text="**Error**",fg="red")

        
    def AddRecordToSalesDatabase(Parent,QuickAddFrame):
        Parent.Confirm.destroy()
        OrderID = RepeatedFunctions.ProduceUniqueOrderID(Parent.Name)
        
        db = sqlite3.connect("Customers db.db")
        EachItem = db.execute("SELECT * FROM Inventory")
        for Record in EachItem:
            if Record[2] == Parent.Item.get():
                ProdID = Record[0]
                
        CSLCheck = "N"
        CheckValues = db.execute("SELECT * FROM Inventory WHERE Category = 'CoalSticksLogs'")

        for Record in CheckValues:
            if Record[2] == Parent.Item.get():
                CSLCheck = "Y"

        c = db.cursor()
        c.execute('''INSERT INTO Sales(OrderID,ProductID,Quantity,CoalSticksLogs)Values
                  (?,?,?,?)''',(OrderID,ProdID,Parent.Quantity.get(),CSLCheck))
        db.commit()
        db.close()
        
        Parent.Company.set("")
        Parent.Company.config(state=DISABLED)
        Parent.Name.set("")
        Parent.Name.config(state=DISABLED)
        Parent.Category.set("")
        Parent.Category.config(state=DISABLED)
        Parent.Item.set("")
        Parent.Item.config(state=DISABLED)
        
        Parent.Quantity.delete(0,END)
        Parent.UnitPrice.config(text = "")
        Parent.Gross.config(text = "")
        Parent.NetTotal.config(text = "")
        Parent.AddSale.config(text = "Add New",command = lambda:
                              Parent.AddNew(QuickAddFrame))
        Parent.Vat.config(text = "")
        Parent.StateLabel.config(text = "Sale Added!!")

    def AddNew(Parent,QuickAddFrame):
        Parent.Confirm.destroy()
        Parent.Company.config(state=ACTIVE)
        Parent.Category.config(state=ACTIVE)
        Parent.Quantity.config(state = NORMAL)
        Parent.UnitPrice.config(text = "")
        Parent.Gross.config(text = "")
        Parent.NetTotal.config(text = "")
        Parent.Vat.config(text = "")
        Parent.StateLabel.config(text = "")
        Parent.AddSale.config(text = "Add sale",command = lambda:
                              Parent.CheckandConfirm(QuickAddFrame))
   
root = Tk()

backCanvas= Canvas(root, background = "#add8e6")
backCanvas.place(x=119,y=2, width = 375, height = 70)

MainWindow = Parent(root)
root.mainloop()

##http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
##http://stackoverflow.com/questions/20588417/how-to-change-font-and-size-of-buttons-and-frame-in-tkinter-using-python
