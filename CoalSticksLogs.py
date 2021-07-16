from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re

class CoalSticksLogs:
    def __init__(Coal,master):
        Coal.master = master

        Headers = ['Product', 'Quantity','Unit Price',"Total","VAT"]
        frame = Frame(master)
        frame.place(x=119,y=259)
        Coal.Tree = ttk.Treeview(frame,columns=Headers,show="headings")
        Coal.Tree.grid(row = 0,column=0,in_=frame)

        RepeatedFunctions.WindowConfig(master,630,487,100,100)
        RepeatedFunctions.ProduceTitleCanvas(master,"Coal Sticks Logs")
        RepeatedFunctions.ProduceMenuCanvas(master,"Coal")
        RepeatedFunctions.TreeView(master,Headers,Coal.Tree,frame)
        Coal.MiddleCanvas(master)
        Coal.CoalAddSaleBox(master)
        Coal.TotalSales(master)
    
    def MiddleCanvas(Coal,master):
        MiddleCanvas = Canvas(master)
        MiddleCanvas.place(x=120,y=71, width = 328, height = 187)
        MiddleCanvas.create_rectangle(1, 1, 326, 185, fill="#add8e6",width = 3,outline="grey")

        Coal.ShowRecords = ttk.Button(MiddleCanvas,text = "Show Orders",command = Coal.FillTree)
        Coal.ShowRecords.place(x=5,y=155)
        Coal.SelectRecords = ttk.Button(MiddleCanvas,text = "Select").place(x=85,y=155)
        Coal.DeleteRecords = ttk.Button(MiddleCanvas,text = "Delete").place(x=165,y=155)
        Coal.EditRecords = ttk.Button(MiddleCanvas,text = "Edit").place(x=245,y=155)
        
        Label(MiddleCanvas,text="Sold Items",font = BUTTON_FONT,bg = "#add8e6").place(x=7,y=3)
        Coal.HouseCoal = Label(MiddleCanvas,text = "House Coal: 0",bg = "#add8e6").place(x=10,y=30)
        Coal.PremHouseCoal = Label(MiddleCanvas,text = "Premium Coal: 0",bg = "#add8e6").place(x=10,y=50)
        Coal.StoveGlow = Label(MiddleCanvas,text = "StoveGlow: 0",bg = "#add8e6").place(x=10,y=70)
        Coal.HomefireOvals = Label(MiddleCanvas,text = "Homefire Ovals: 0",bg = "#add8e6").place(x=10,y=90)
        Coal.Logs = Label(MiddleCanvas,text = "Logs: 0",bg = "#add8e6").place(x=10,y=110)
        Coal.Kindling = Label(MiddleCanvas,text = "Kindling: 0",bg = "#add8e6").place(x=10,y=130)

    def CoalAddSaleBox(Coal,master):

        CoalSaleCanvas = Canvas(master)
        CoalSaleCanvas.place(x=449,y=71, width = 180, height = 145)
        CoalSaleCanvas.create_rectangle(1, 1, 178, 143, fill="#add8e6",width = 3,outline="grey")
        CoalAddFrame = LabelFrame(CoalSaleCanvas,bg="#add8e6",bd=0)
        CoalAddFrame.place(x=6,y=7)
        
        Label(CoalAddFrame, text="Product",bg="#add8e6").grid(row=0)
        Label(CoalAddFrame, text="Quantity",bg="#add8e6").grid(row=1)
        Label(CoalAddFrame, text="Unit Price",bg="#add8e6").grid(row=2)
        Label(CoalAddFrame, text="Total",bg="#add8e6").grid(row=3)
        Label(CoalAddFrame, text="VAT",bg="#add8e6").grid(row=4)
        Coal.AddSale = ttk.Button(CoalAddFrame,text="Add Sale",command = lambda: Coal.CheckandConfirm(CoalAddFrame))
        Coal.AddSale.grid(row=5)

        
        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()
        Products = db.execute("SELECT * FROM Inventory")
        BoxValues = []
        for x in Products:
            if x[1] == "CoalSticksLogs":
                BoxValues.append(x[2])
                
        Coal.Product = ttk.Combobox(CoalAddFrame,width=10)
        Coal.Product["values"] = BoxValues
        Coal.Product.bind("<Configure>",RepeatedFunctions.CheckWidth(BoxValues))
        
        Coal.ProductQuantity = ttk.Entry(CoalAddFrame,width = 10)
        Coal.UnitPrice = Label(CoalAddFrame,bg="#add8e6")
        Coal.Total = Label(CoalAddFrame,bg="#add8e6")  
        Coal.VAT = Label(CoalAddFrame,bg="#add8e6")
        Coal.StateLabel = Label(CoalAddFrame,bg="#add8e6")

        Coal.Product.grid(row=0, column=1)
        Coal.ProductQuantity.grid(row=1, column=1)
        Coal.UnitPrice.grid(row=2, column=1)
        Coal.Total.grid(row=3, column=1)
        Coal.VAT.grid(row = 4,column=1)
        Coal.StateLabel.grid(row=5,column=1)
   
    def TotalSales(Coal,master):
        
        TotalCoalSales = Canvas(master)
        TotalCoalSales.place(x=449,y=217, width = 180, height = 41)
        TotalCoalSales.create_rectangle(1, 1, 178, 39, fill="#add8e6",width = 3,outline="grey")

        TotalSales = Label(TotalCoalSales,text = "Sales: £0.00",bg="#add8e6")
        TotalSales.place(x=21,y=9)
        TotalVAT = Label(TotalCoalSales,text = "VAT: £0.00",bg="#add8e6")
        TotalVAT.place(x=96,y=9)
        
    def CheckandConfirm(Coal,frame):
        try:
            fetchQuan = int(Coal.ProductQuantity.get())

            db = sqlite3.connect("Customers db.db")
            c = db.cursor()
            c.execute("SELECT * FROM Inventory")
            result = c.fetchall() 
            for Record in result:
                if Record[2] == Coal.Product.get():
                    ProductPrice = Record[3]
            
            TotalPriceMoney = Decimal(str(fetchQuan*ProductPrice)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            VatMoney = Decimal(str(TotalPriceMoney/5)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
            Coal.UnitPrice.config(text = "£ "+ str(ProductPrice))
            Coal.Total.config(text = "£ "+ str(TotalPriceMoney))
            Coal.VAT.config(text = "£ "+ str(VatMoney))

            Coal.Product.config(state=DISABLED)
            Coal.ProductQuantity.config(state = DISABLED)
            
            Coal.StateLabel.config(text="")
            Coal.Confirm = ttk.Button(frame,text = "Confirm Sale",command = lambda:Coal.AddRecordToDatabase(frame))
            Coal.Confirm.grid(row=5,column=1)

        except:
            Coal.StateLabel.config(text="**Error**",fg="red",bg="#add8e6")

    def AddRecordToDatabase(Coal,frame):
        db = sqlite3.connect("Customers db.db")

        CSLItems = db.execute("SELECT * FROM Inventory")
        for Record in CSLItems:
            if Record[2] == Coal.Product.get():
                CoalID = Record[0] 

        db.execute('''INSERT INTO Sales(OrderID,ProductID,Quantity,CoalSticksLogs)
                   Values (?,?,?,?)''',
                  ("Null",CoalID,Coal.ProductQuantity.get(),"Y"))
        db.commit()
        db.close()

            
        Coal.Confirm.destroy()
        Coal.AddSale.config(text = "Add New",command = lambda:Coal.Reset(frame))
        
        Coal.StateLabel.config(text = "Sale Added !! ")
        Coal.ProductQuantity.delete(0,END)
        Coal.Product.set("")
        Coal.UnitPrice.config(text = "")
        Coal.Total.config(text = "")
        Coal.VAT.config(text = "")

    def Reset(Coal,frame):
        Coal.Product.config(state=NORMAL)
        Coal.ProductQuantity.config(state=NORMAL)
        Coal.StateLabel.config(text = "")
        Coal.AddSale.config(text = "Add Sale",command = lambda: Coal.CheckandConfirm(frame))

    def FillTree(Coal):
        Coal.ShowRecords.config(state=DISABLED)
        
        table_list = []
        db = sqlite3.connect("Customers db.db")
        AllSales = db.execute("SELECT * FROM Sales")
        AllProducts = db.execute("SELECT * FROM Inventory")
        Data = ["","","","","","",""]

        for Record in AllSales:
            if Record[4] == "Y":
                print("")
                #Data[1] = Record[3]
                Data[1] = "Yeah"
            for EachRecord in AllProducts:
                if Record[2] == EachRecord[0]:
                    Data[0] == EachRecord[2]
                    print(Data)
            table_list.append((Record[0],Record[1],Record[2],Record[3],Record[4]))
        for item in table_list:
            Coal.Tree.insert('', 'end', values=item)

