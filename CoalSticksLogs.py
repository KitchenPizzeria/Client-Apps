from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re

BUTTON_FONT = ("Georgia",16)
TITLE_FONT = ("Georgia",28)

class CoalSticksLogs():
    def __init__(self,master):
        self.master = master

        # master.config(bg="#ffca00")
        # master.resizable(0,0)
        # master.geometry('%dx%d' % (750, 487))

        Headers = ['Product', 'Quantity', 'Unit Price', "Total", "VAT"]
        frame = Frame(master)
        frame.place(x=119,y=259)
        self.tree = ttk.Treeview(frame,columns=Headers,show="headings")
        self.tree.grid(row = 0,column=0,in_=frame)

        self.TreeView(master,Headers,self.tree,frame)
        self.MiddleCanvas(master)
        self.CoalAddSaleBox(master)
        self.TotalSales(master)
    
    def MiddleCanvas(self,master):

        MiddleCanvas = Canvas(master)
        MiddleCanvas.place(x=10,y=71, width = 400, height = 187)
        MiddleCanvas.create_rectangle(1, 1, 1000, 1000, fill="#add8e6")

        Buttons = Canvas(MiddleCanvas)
        Buttons.pack(side = BOTTOM, pady=8)

        self.ShowRecords = ttk.Button(Buttons,text = "Show Orders",command = self.FillTree)
        self.SelectRecords = ttk.Button(Buttons,text = "Select")
        self.DeleteRecords = ttk.Button(Buttons,text = "Delete")
        self.EditRecords = ttk.Button(Buttons,text = "Edit")

        self.ShowRecords.grid(row=0,column=0)
        self.SelectRecords.grid(row=0,column=1)
        self.DeleteRecords.grid(row=0,column=2)
        self.EditRecords.grid(row=0,column=3)
        
        Label(MiddleCanvas,text="Sold Items",font = BUTTON_FONT, bg = "#add8e6").place(x=7,y=3)
        self.HouseCoal = Label(MiddleCanvas,text = "House self: 0",bg = "#add8e6").place(x=10,y=30)
        self.PremHouseCoal = Label(MiddleCanvas,text = "Premium self: 0",bg = "#add8e6").place(x=10,y=50)
        self.StoveGlow = Label(MiddleCanvas,text = "StoveGlow: 0",bg = "#add8e6").place(x=10,y=70)
        self.HomefireOvals = Label(MiddleCanvas,text = "Homefire Ovals: 0",bg = "#add8e6").place(x=10,y=90)
        self.Logs = Label(MiddleCanvas,text = "Logs: 0",bg = "#add8e6").place(x=10,y=110)
        self.Kindling = Label(MiddleCanvas,text = "Kindling: 0",bg = "#add8e6").place(x=10,y=130)

    def CoalAddSaleBox(self,master):
        CoalSaleCanvas = Canvas(master)
        CoalSaleCanvas.place(x=449, y=40, width = 220, height = 165)
        CoalSaleCanvas.create_rectangle(1, 1, 1000, 1000, fill="#add8e6",width = 3,outline="grey")
        CoalAddFrame = LabelFrame(CoalSaleCanvas,bg="#add8e6",bd=0)
        CoalAddFrame.place(x=6,y=7)
        
        Label(CoalAddFrame, text="Product",bg="#add8e6").grid(row=0)
        Label(CoalAddFrame, text="Quantity",bg="#add8e6").grid(row=1)
        Label(CoalAddFrame, text="Unit Price",bg="#add8e6").grid(row=2)
        Label(CoalAddFrame, text="Total",bg="#add8e6").grid(row=3)
        Label(CoalAddFrame, text="VAT",bg="#add8e6").grid(row=4)
        self.AddSaleButton = ttk.Button(CoalAddFrame, text= "Add Sale", command = lambda: self.CheckandConfirm(CoalAddFrame))
        self.AddSaleButton.grid(row=5)

        
        db = sqlite3.connect("Customers.db")
        Link = db.cursor()
        Products = db.execute("SELECT * FROM Inventory")
        BoxValues = []
        for x in Products:
            if x[1] == "CoalSticksLogs":
                BoxValues.append(x[2])
                
        self.Product = ttk.Combobox(CoalAddFrame, width=10)
        self.Product["values"] = BoxValues
        self.Product.bind("<Configure>", self.CheckWidth(BoxValues))
        
        self.ProductQuantity = ttk.Entry(CoalAddFrame, width = 10)
        self.UnitPrice = Label(CoalAddFrame, bg="#add8e6")
        self.Total = Label(CoalAddFrame, bg="#add8e6")  
        self.VAT = Label(CoalAddFrame, bg="#add8e6")
        self.StateLabel = Label(CoalAddFrame, bg="#add8e6")

        self.Product.grid(row=0, column=1)
        self.ProductQuantity.grid(row=1, column=1)
        self.UnitPrice.grid(row=2, column=1)
        self.Total.grid(row=3, column=1)
        self.VAT.grid(row = 4,column=1)
        self.StateLabel.grid(row=5,column=1)
   
    def TotalSales(self, master):
        
        TotalCoalSales = Canvas(master)
        TotalCoalSales.place(x=449,y=217, width = 180, height = 41)
        TotalCoalSales.create_rectangle(1, 1, 178, 39, fill="#add8e6")

        TotalSales = Label(TotalCoalSales,text = "Sales: £0.00",bg="#add8e6")
        TotalSales.place(x=5,y=9)
        TotalVAT = Label(TotalCoalSales,text = "VAT: £0.00",bg="#add8e6")
        TotalVAT.place(x=96,y=9)
        
    def CheckandConfirm(self,frame):

        buttonText = self.AddSaleButton.cget("text")
        if buttonText == "Add Sale" and self.ProductQuantity.get() != "":

            self.AddSaleButton.config(text = "Return")
            try:
                fetchQuan = int(self.ProductQuantity.get())

                db = sqlite3.connect("Customers.db")
                c = db.cursor()
                c.execute("SELECT * FROM Inventory")
                result = c.fetchall() 
                for Record in result:
                    if Record[2] == self.Product.get():
                        ProductPrice = Record[3]
                
                TotalPriceMoney = Decimal(str(fetchQuan*ProductPrice)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
                VatMoney = Decimal(str(TotalPriceMoney/5)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
                self.UnitPrice.config(text = "£ "+ str(ProductPrice))
                self.Total.config(text = "£ "+ str(TotalPriceMoney))
                self.VAT.config(text = "£ "+ str(VatMoney))

                self.Product.config(state=DISABLED)
                self.ProductQuantity.config(state = DISABLED)
                
                self.StateLabel.config(text="")
                self.ConfirmButton = ttk.Button(frame,text = "Confirm Sale",command = lambda:self.AddRecordToDatabase(frame))
                self.ConfirmButton.grid(row=5,column=1)

            except:
                self.StateLabel.config(text="**Error**",fg="red",bg="#add8e6")
        else:
            
            self.AddSaleButton.config(text = "Add Sale")
            self.Product.set("")
            self.Product.config(state = NORMAL)
            self.ProductQuantity.config(state = NORMAL)
            self.ProductQuantity.delete(0, END)
            self.ConfirmButton.grid_forget()

            self.UnitPrice.config(text = "")
            self.Total.config(text = "")
            self.VAT.config(text = "")

    def AddRecordToDatabase(self,frame):

        self.AddSaleButton.config(text = "Add Sale")

        db = sqlite3.connect("Customers.db")

        CSLItems = db.execute("SELECT * FROM Inventory")
        for Record in CSLItems:
            if Record[2] == self.Product.get():
                CoalID = Record[0] 

        db.execute('''INSERT INTO Sales(OrderID,ProductID,Quantity,CoalSticksLogs)
                   Values (?,?,?,?)''',
                  ("Null",CoalID,self.ProductQuantity.get(),"Y"))
        db.commit()
        db.close()

            
        self.Confirm.destroy()
        self.AddSale.config(text = "Add New",command = lambda:self.Reset(frame))
        
        self.StateLabel.config(text = "Sale Added !! ")
        self.ProductQuantity.delete(0,END)
        self.Product.set("")
        self.UnitPrice.config(text = "")
        self.Total.config(text = "")
        self.VAT.config(text = "")

    def Reset(self,frame):
        self.Product.config(state = NORMAL)
        self.ProductQuantity.config(state=NORMAL)
        self.StateLabel.config(text = "")
        self.AddSale.config(text = "Add Sale",command = lambda: self.CheckandConfirm(frame))

    def FillTree(self):
        self.ShowRecords.config(state=DISABLED)
        
        table_list = []
        db = sqlite3.connect("Customers.db")
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
            self.Tree.insert('', 'end', values=item)

    def TreeView(self,master,Header,tree,frame):
        
        ScrollBar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        ScrollBar.grid(row=0, column=1, sticky='ns',in_=frame)
        tree.configure(yscrollcommand=ScrollBar.set)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        if Header[0] == "Product":
            
            width = 491
            HeaderLength = 0
            for x in Header:
                HeaderLength += len(x)
            
            tree.column(Header[0],width=int(len(Header[0])/HeaderLength*width)+40)
            tree.column(Header[1],width=int(len(Header[1])/HeaderLength*width)-20)
            tree.column(Header[2],width=int(len(Header[2])/HeaderLength*width)-50)
            tree.column(Header[3],width=int(len(Header[3])/HeaderLength*width)+20)
            tree.column(Header[4],width=int(len(Header[4])/HeaderLength*width)+10)
            
        else:   
            width = 734
            HeaderLength = 0
            for x in Header:
                HeaderLength += len(x)
            
            tree.column(Header[0],width=int(len(Header[0])/HeaderLength*width)-30)
            tree.column(Header[1],width=int(len(Header[1])/HeaderLength*width))
            tree.column(Header[2],width=int(len(Header[2])/HeaderLength*width)+20)
            tree.column(Header[3],width=int(len(Header[3])/HeaderLength*width)-80)
            tree.column(Header[4],width=int(len(Header[4])/HeaderLength*width)+90)
            tree.column(Header[5],width=int(len(Header[5])/HeaderLength*width))
            tree.column(Header[6],width=int(len(Header[6])/HeaderLength*width))

        for col in Header:
            tree.heading(col, text=col.title(), anchor = "w",command=lambda c=col: RepeatedFunctions.SortRecords(c,1,Header,tree))
           
    def CheckWidth(self, List1):
            LongestWord = 0
            for x in List1:
                if len(x) > LongestWord:
                    LongestWord = len(x)
            for x in List1:
                if len(x) == LongestWord:               
                    style = ttk.Style()
                    style.configure('TCombobox', postoffset=(0,0,len(x)+70,0))

