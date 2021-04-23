from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re

BUTTON_FONT = ("Georgia",16)
TITLE_FONT = ("Georgia",28)

class RepeatedFunctions:
    def WindowConfig(self,w,h,x,y):
        self.config(bg="#ffca00")
        self.resizable(0,0)
        self.geometry('%dx%d+%d+%d' % (w,h,x,y))

    def ProduceTitleCanvas(self,text):
        if text == "Coal Sticks Logs" or text == "Invoices":
            w = 509
        elif text == "Edit Form":
            w = 317
        else:
            w = 628
            
        TitleCanvas = Canvas(self)
        if text == "Edit Form":
            TitleCanvas.place(x=2,y=2,width=w,height = 68)
        else:
            TitleCanvas.place(x=120,y=2,width=w,height = 68)
        TitleCanvas.create_rectangle(1, 1, w-2, 66, fill="#96C8A2",width = 3,outline="grey")

        WindowLabel = Label(TitleCanvas,text = text,font = TITLE_FONT,bg="#96C8A2").pack(side=LEFT,padx = 3) 
        
        ReturnButton = ttk.Button(TitleCanvas,text="Return >",command =self.destroy)
        ReturnButton.pack(side=RIGHT,padx=9)
    
    def ProduceMenuCanvas(self,text):
        MenuCanvas = Canvas(self)
        MenuCanvas.create_rectangle(1, 1, 114, 255, fill="#add8e6",width = 3,outline="grey")
        MenuTitle = "Menu"
        
        if text != "Coal":
            MenuCanvas.place(x=2,y=2, width = 116, height = 257)
        else:
            MenuCanvas.place(x=2,y=70, width = 116, height = 257)
            
        if text == "Parent":
            MenuTitle = "Home"
        else:
            MenuTitle = "Menu"

        Label(MenuCanvas,text = MenuTitle,font=BUTTON_FONT,bg = "#add8e6").pack(side=TOP,pady=14)
        ClientButton = ttk.Button(MenuCanvas,text = "Clients",width=15,command = lambda: Customers(Tk())).pack(pady=2)
        SalesButton = ttk.Button(MenuCanvas,text = "Sales",width=15,command = Sales(Tk())).pack(pady=2)
        CoalSticksLogsButton = ttk.Button(MenuCanvas,text = "Coal Sticks Logs",width = 15,command = CoalSticksLogs(Tk())).pack(pady=2)
        InvoicesButton = ttk.Button(MenuCanvas,text = "Invoices",width=15).pack(pady=2)

        Close = "Return >"
        if text == "Parent":
            Close = "Quit"
            
        ReturnButton = ttk.Button(MenuCanvas,text=Close,command =self.destroy).pack(side=BOTTOM,pady=7)
        
    def ProduceUniqueOrderID(Name):
        now = datetime.datetime.now()
        Date = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        
        db = sqlite3.connect("Customers db.db")

        EachName = db.execute("SELECT * FROM Customers")
        for Record in EachName:
            if Record[1]+" "+Record[2] == Name.get():
                CustID = Record[0]
                
        db.execute("INSERT INTO Orders(Date,CustomerID)Values (?,?)",(Date,CustID))

        Orders = db.execute("SELECT * FROM Orders")
        for x in Orders:
            OrderID = x[0]
           
        db.commit()
        db.close()

        return OrderID
        
    def OpenClients(ClientButton):
        NewWin = Customers(Tk())
    def OpenSales():
        NewWin = Sales(Tk())
    def OpenCSL():
        NewWin = CoalSticksLogs(Tk())
    def OpenInvoices():
        NewWin = Invoices(Tk())
   
    def TreeView(master,Header,tree,frame):

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

    def SortRecords(col, descending,table_header,tree):
        List = []
        for child in tree.get_children(''):
            List.append((tree.set(child,0),tree.set(child,1),
                         tree.set(child,2),tree.set(child,3),  
                         tree.set(child,4),tree.set(child,5),
                         tree.set(child,6)))
        index = table_header.index(col)
        exchanges = True
        passnum = len(List)-1
        while passnum > 0 and exchanges:
            exchanges = False
            for i in range(passnum):
                if descending and List[i][index] > List[i+1][index]:
                    exchanges = True
                    temp = List[i]
                    List[i] = List[i+1]
                    List[i+1] = temp
                elif not descending and List[i][index] < List[i+1][index]:
                    exchanges = True
                    temp = List[i]
                    List[i] = List[i+1]
                    List[i+1] = temp
            passnum = passnum-1
        tree.delete(*tree.get_children()) 
        for item in List:
            tree.insert('', 'end', values=item) 
        tree.heading(col, command=lambda c=col:RepeatedFunctions.SortRecords
                     (c,int(not descending),table_header,tree))

    def CheckWidth(List1):
        LongestWord = 0
        for x in List1:
            if len(x) > LongestWord:
                LongestWord = len(x)
        for x in List1:
            if len(x) == LongestWord:               
                style = ttk.Style()
                style.configure('TCombobox', postoffset=(0,0,len(x)+70,0))
                
    def InputMask(self,master,grid,items,text):
        
        TelephoneRegEx = r"\d+[ ]{0,1}\d*$"
        NamesCompanyRegEx = r"[a-zA-Z]+"
        PostcodeRegEx = r"[a-zA-Z0-9]{2,4}[ ]{1}[0-9]{1}[a-zA-Z]{2}$"
        EmailRegEx = r"[a-zA-z0-9]+[@]{1}[a-zA-Z0-9.]+$"
        AddressRegEx = r"\d{1,3}[ ]{1}[a-zA-Z]+[ ]{1}[a-zA-Z]+"

        if re.match(TelephoneRegEx,self.ContactNum.get()):
            if re.match(EmailRegEx,self.Email.get()):
                if re.match(PostcodeRegEx,self.Postcode.get()):
                    if re.match(NamesCompanyRegEx,self.Firstname.get()):
                        if re.match(NamesCompanyRegEx,self.Lastname.get()):
                            if re.match(NamesCompanyRegEx,self.CompanyEntry.get()):
                                if re.match(AddressRegEx,self.Address.get()):
                                
                                    self.Firstname.config(state = DISABLED)
                                    self.Lastname.config(state = DISABLED)
                                    self.CompanyEntry.config(state = DISABLED)
                                    self.Email.config(state = DISABLED)
                                    self.ContactNum.config(state = DISABLED)
                                    self.Postcode.config(state = DISABLED)
                                    self.Address.config(state = DISABLED)
                                    self.StateLabel.config(text="")

                                    if text == "Customers":                       
                                        self.ConfirmButton = ttk.Button(grid,text = "Confirm",command =
                                                                        lambda:Customers.AddRecordToCustomerDatabase
                                                                        (self,grid,master))
                                        self.ConfirmButton.grid(column = 1, row = 7)
                                        self.Submit.config(text = "Edit",command =
                                                           lambda:Customers.Reset
                                                           (self,"Edit",grid,master))
                                        
                                    elif text == "FormWindow":
                                        self.ConfirmButton = ttk.Button(grid,text = "Confirm",command = lambda:EditFormWindow.ChangeDatabase
                                                                        (self,master,self.ConfirmButton,items))
                                        self.ConfirmButton.grid(column = 1, row = 7)
                                        #self.Submit.config(text = "Edit",command = lambda:Customers.Reset(self,"Edit",grid))
                                else:
                                    self.StateLabel.config(text= "Error: Address",fg="red")
                            else:
                                self.StateLabel.config(text= "Error: Company",fg="red")
                        else:
                            self.StateLabel.config(text= "Error: Surname",fg="red")
                    else:
                        self.StateLabel.config(text= "Error: Firstname",fg="red")
                else:
                    self.StateLabel.config(text= "Error: Postcode",fg="red")
            else:
                self.StateLabel.config(text= "Error: Email",fg="red")
        else:
            self.StateLabel.config(text= "Error: Contact Number",fg="red")

            
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================


class Invoices:
    def __init__ (Invoice,master):
        Invoice.master = master

        RepeatedFunctions.WindowConfig(master,630,260,100,100)
        RepeatedFunctions.ProduceTitleCanvas(master,"Invoices")
        RepeatedFunctions.ProduceMenuCanvas(master,"Invoice")

        Button(master,text = "print all invoices",command = Invoice.ProduceInvoicesRequired).place(x=300,y=100)
        
    def ProduceInvoicesRequired(Invoice):
        db = sqlite3.connect("Customers db.db")
        c = db.cursor()
        GetOrders = db.execute("SELECT * FROM Orders")
        c.execute("SELECT * FROM Customers")
        Result = c.fetchall()

        NameswithIDs = []
        Companies = []
        for x in Result:
            data = [x[0],x[1],x[2],x[3]]
            Companies.append(x[3])
            NameswithIDs.append(data)
        Companies = sorted(set(Companies))
        OrderIdswithCustIds = []
        for x in GetOrders:
            data = [x[0],x[2]]
            OrderIdswithCustIds.append(data)
            
        NamesToInvoice = []
        for x in OrderIdswithCustIds:
            OrderCustID = x[1]
            for y in NameswithIDs:
                Name = str(y[1])+" "+str(y[2])
                CustID = y[0]
                if OrderCustID == CustID:            
                    NamesToInvoice.append(Name)      
        NamesToInvoice = sorted(set(NamesToInvoice))


        data = '<tr><th>Rep</th><th>Date</th><th>Date</th></tr>'
        for x in Result:
            Filename = x[3]+".html" ## filename is company
            ProduceFile = open(Filename,"w")

            Reps = db.execute("SELECT Firstname,Surname FROM Customers WHERE Company = '%s'"%x[3])
        

            ProduceFile.write('''<!DOCTYPE html>
            <html>
            <head><title>Invoice</title>
            <style>
            table, th, td {border: 1px solid black;border-collapse: collapse;}
            th, td {padding: 5px;}
            th {text-align: left;}
            </style>
            </head>
            <body><h1>Invoices</h1><h2>'''+x[3]+'''</h2><table style="width:60%">'''+data+'''</table>
            </body>
            </html''')

            
        ProduceFile.close()
                         
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================

        
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
    
    
        
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================


class Sales:
    def __init__(Sales,master):
        Sales.master = master

        Headers = ['Firstname', 'Surname',"Category",'Description',"Unit Price","Quantity","Total"]
        frame = Frame(master)
        frame.pack(side = BOTTOM)
        Sales.Tree = ttk.Treeview(frame,columns=Headers,show="headings")
        Sales.Tree.grid(row = 0,column=0,in_=frame)

        RepeatedFunctions.WindowConfig(master,750,487,100,100)
        RepeatedFunctions.ProduceTitleCanvas(master,"Sales")
        RepeatedFunctions.ProduceMenuCanvas(master,"Sales")
        RepeatedFunctions.TreeView(master,Headers,Sales.Tree,frame)
        
        Sales.SalesFilterDisplayBox(master)
        Sales.AddSalesForm(master)
        #Sales.Receipt(master)

        master.mainloop()

    def SalesFilterDisplayBox(Sales,master):
        FilterCanvas = Canvas(master)
        FilterCanvas.place(x=140,y=72, width = 328, height = 187)
        FilterCanvas.create_rectangle(1, 1, 326, 185, fill="#add8e6",width = 3,outline="grey")        
#----------------
        ButtonFilters = LabelFrame(FilterCanvas,bg = "#add8e6",bd=0)
        ButtonFilters.place(x=4,y=4,width = 200,height=120)
        
        Label(ButtonFilters,text = "Filter",font = ("Georgia",15),bg = "#add8e6").pack(side = TOP)
        
        Sales.Description = ttk.Combobox(ButtonFilters,state=DISABLED,width=10)
        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()
        
        Descriptions = db.execute("SELECT Description FROM Inventory")
        data = []
        for x in Descriptions:
            if max(x) != "":
                data.append(max(x))
        Sales.Description["values"] = data
        Sales.Description.place(x=100,y=30)

        Sales.radioChoice = IntVar()
        Radiobutton(ButtonFilters, text="Company", variable=Sales.radioChoice, value=1,bg = "#add8e6").place(x=10,y=30)
        Radiobutton(ButtonFilters, text="ASC", variable=Sales.radioChoice, value=2,bg = "#add8e6").place(x=40,y=55)
        Radiobutton(ButtonFilters, text="DSC", variable=Sales.radioChoice, value=3,bg = "#add8e6").place(x=100,y=55)

        Sales.ApplyButton = ttk.Button(ButtonFilters,state=DISABLED,text = "Apply")
        Sales.ApplyButton.pack(side=BOTTOM,pady = 8)
#--------------------     
        Sales.SCompany = Label(FilterCanvas,text = "Company: None",bg = "#add8e6")
        Sales.SCompany.place(x=210,y=8)
        Sales.SDescription = Label(FilterCanvas,text = "Description: None",bg = "#add8e6")
        Sales.SDescription.place(x=210,y=28)
        Sales.SQuantity = Label(FilterCanvas,text = "Quantity: None",bg = "#add8e6")
        Sales.SQuantity.place(x=210,y=48)
        Sales.SUnitPrice = Label(FilterCanvas,text = "Unit Price: None",bg = "#add8e6")
        Sales.SUnitPrice.place(x=210,y=68)
        Sales.SNetTotal = Label(FilterCanvas,text = "Net: None",bg = "#add8e6")
        Sales.SNetTotal.place(x=210,y=88)
        Sales.SGrossTotal = Label(FilterCanvas,text = "Gross: None",bg = "#add8e6")
        Sales.SGrossTotal.place(x=210,y=108)
        Sales.SVAT = Label(FilterCanvas,text = "VAT: None",bg = "#add8e6")
        Sales.SVAT.place(x=210,y=128)
        
        Sales.AmountOfSales = Label(FilterCanvas,text ="Amount of Clients: 0",bg = "#add8e6")
        Sales.AmountOfSales.place(x=49,y=128)
        Sales.ShowRecordsButton = ttk.Button(FilterCanvas,text = "Show Sales",command = Sales.DisplayAllRecords)
        Sales.ShowRecordsButton.place(x=5,y=153)
        Sales.SelectRecord = ttk.Button(FilterCanvas,text = "Select")
        Sales.SelectRecord.place(x=84,y=153)
        Sales.RemoveClient = ttk.Button(FilterCanvas,text = "Delete",state=DISABLED)
        Sales.RemoveClient.place(x=163,y=153)
        Sales.EditClient = ttk.Button(FilterCanvas,text="Edit",state=DISABLED)
        Sales.EditClient.place(x=242,y=153)

    def AddSalesForm(Sales,master):

        AddSaleCanvas = Canvas(master)
        AddSaleCanvas.place(x=470,y=72, width = 248, height = 187)
        AddSaleCanvas.create_rectangle(1, 1, 246,185, fill="#add8e6",width = 3,outline="grey")

        QuickAddFrame = LabelFrame(AddSaleCanvas,bg="#add8e6",bd=0)
        QuickAddFrame.place(x=6,y=7)
        Label(QuickAddFrame, text="Company",bg="#add8e6").grid(row=0)
        Label(QuickAddFrame, text="Client",bg="#add8e6").grid(row=1)
        Label(QuickAddFrame, text="Category",bg="#add8e6").grid(row=2)
        Label(QuickAddFrame, text="Item",bg="#add8e6").grid(row=3)
        Label(QuickAddFrame, text = "Quantity",bg="#add8e6").grid(row=4)
        Label(QuickAddFrame, text = "Unit Price",bg="#add8e6").grid(row=5)
        Label(QuickAddFrame, text = "Total",bg="#add8e6").grid(row=6)
        

        Sales.Item = ttk.Combobox(QuickAddFrame,state = DISABLED,width = 20)
        Sales.Name = ttk.Combobox(QuickAddFrame,state = DISABLED,width = 20)

        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()

        Sales.Company = ttk.Combobox(QuickAddFrame,width = 20)
        Companies = db.execute("SELECT Company FROM Customers")
        CompanyValues = []
        for x in Companies:
            if max(x) != "":
                CompanyValues.append(max(x))
        CompanyValues = sorted(list(set(CompanyValues)))
        Sales.Company["values"] = CompanyValues
        
        Sales.Company.bind("<Configure>",RepeatedFunctions.CheckWidth(CompanyValues))
        Sales.Company.bind("<<ComboboxSelected>>",Sales.ActivateAndFillNameBox)
        
        Sales.Category = ttk.Combobox(QuickAddFrame,width = 20)
        Categories = db.execute("SELECT Category FROM Inventory")
        StockCat = []
        for x in Categories:
            if max(x) != "" or max(x)!="None":
                StockCat.append(max(x))
        StockCat = sorted(list(set(StockCat)))
        Sales.Category["values"] = StockCat

        Sales.Category.bind("<Configure>",RepeatedFunctions.CheckWidth(StockCat))
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
        
    def CheckandConfirm(Sales,QuickAddFrame,Repeat):
        
        db = sqlite3.connect("Customers db.db")
        c = db.cursor()
        c.execute("SELECT * FROM Inventory")
        result = c.fetchall() 
        for Record in result:
            if Record[2] == Sales.Item.get():
                fetchPrice = float(Record[3])

        try:
            fetchQuan = int(Sales.Quantity.get())

            TotalPriceMoney = Decimal(str(fetchQuan*fetchPrice)).quantize(Decimal('.01'), rounding=ROUND_DOWN)

            Sales.UnitPrice.config(text ="£ "+ str(fetchPrice))
            Sales.Total.config(text = "£ "+ str(TotalPriceMoney))
            Sales.Company.config(state=DISABLED)
            Sales.Name.config(state=DISABLED)
            Sales.Category.config(state=DISABLED)
            Sales.Item.config(state=DISABLED)
            Sales.Quantity.config(state = DISABLED)

            Sales.CheckFlagStatus(Repeat,QuickAddFrame)
                
            

        except:
            Sales.StateLabel.config(text="**Error**",fg="red")

    def CheckFlagStatus(Sales,Repeat,QuickAddFrame):
        if Repeat:
            OrderID = RepeatedFunctions.ProduceUniqueOrderID(Sales.Name)
            Repeat = False
        else:
            db = sqlite3.connect("Customers db.db")
            Orders = db.execute("SELECT * FROM Orders")
            for x in Orders:
                Num = x[0]
            OrderID = Num
        Sales.ContinueToAdd(QuickAddFrame,OrderID,Repeat)
        
    def ContinueToAdd(Sales,QuickAddFrame,OrderID,Repeat):
        Sales.StateLabel.config(text = "")
        Sales.Confirm.config(state = ACTIVE,command = lambda:Sales.AddRecordToSalesDatabase
                             (QuickAddFrame,OrderID,Repeat))
        Sales.AddSale.config(text = "Edit",command = lambda:Sales.AddNew
                             (QuickAddFrame,Repeat))
        
    def AddRecordToSalesDatabase(Sales,QuickAddFrame,OrderID,Repeat):
        db = sqlite3.connect("Customers db.db")
        
        EachItem = db.execute("SELECT * FROM Inventory")
        for Record in EachItem:
            if Record[2] == Sales.Item.get():
                ProdID = Record[0]
                
        CSLCheck = "N"
        CheckValues = db.execute("SELECT * FROM Inventory WHERE Category = 'CoalSticksLogs'")
        for Record in CheckValues:
            if Record[2] == Sales.Item.get():
                CSLCheck = "Y"
        
        c = db.cursor()
        c.execute("INSERT INTO Sales(OrderID,ProductID,Quantity,CoalSticksLogs)Values (?,?,?,?)",
                  (OrderID,ProdID,Sales.Quantity.get(),CSLCheck))
        db.commit()
        db.close()

        Sales.Category.set("")
        Sales.Item.set("")
        Sales.Quantity.delete(0,END)
        Sales.UnitPrice.config(text = "")
        Sales.Total.config(text = "")
        Sales.AddSale.config(text = "Add New",command = lambda: Sales.AddNew(QuickAddFrame,Repeat))
        Sales.Confirm.config(state = DISABLED)
        Sales.StateLabel.config(text = "Sale Added!!",fg="black")

    def AddNew(Sales,QuickAddFrame,Repeat):
        
        Sales.Category.config(state=NORMAL)
        Sales.Item.config(state=NORMAL)
        Sales.Quantity.config(state = ACTIVE)
        Sales.UnitPrice.config(text = "")
        Sales.Total.config(text = "")
        Sales.StateLabel.config(text = "")
        Sales.AddSale.config(text = "Add Sale",command = lambda: Sales.CheckandConfirm
                             (QuickAddFrame,Repeat))
        
    def ActivateAndFillItemBox(Sales,event):
        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()

        Sales.StockItems = []
        StockDesc = db.execute("SELECT Description FROM Inventory WHERE Category = '%s'"%Sales.Category.get())
        for x in StockDesc:
            if max(x) != "":
                Sales.StockItems.append(max(x))
        Sales.StockItems = sorted(list(set(Sales.StockItems)))
        Sales.Item["values"] = Sales.StockItems
        Sales.Item.config(state = NORMAL)
        RepeatedFunctions.CheckWidth(Sales.StockItems)
        
    def ActivateAndFillNameBox(Sales,event):
        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()
        
        Sales.Names = []
        DbNames = db.execute("SELECT Firstname,Surname FROM Customers WHERE Company = '%s'"%Sales.Company.get())
        for x in DbNames:
            Name = x[0]+" "+x[1]
            if max(x)!="":
                Sales.Names.append(Name)
            
        Sales.Names = sorted(list(set(Sales.Names)))
        Sales.Name["values"] = Sales.Names
        Sales.Name.config(state=ACTIVE)
        RepeatedFunctions.CheckWidth(Sales.Names)
        
    def DisplayAllRecords(Sales):

        db = sqlite3.connect("Customers db.db")
        Info = db.execute("SELECT CustomerID,ProductID,Quantity FROM Sales")
        Data= ["","","","","","",""]
        Rep = False
        while Rep == False:
            for Record in Info:
                CustID = Record[0]
                ProdID = Record[1]
                Quantity = Record[2]
                Data[5] = Quantity
                
                
            GatherCustomerInfo = db.execute("SELECT CustomerID,Firstname,Surname FROM Customers WHERE CustomerID = '%s';"%CustID)
            for EachLine in GatherCustomerInfo:
                if EachLine[0] == CustID:
                    Data[0]= EachLine[1]
                    Data[1] = EachLine[2]
            Sales.Tree.insert('', 'end', values=Data)
            Rep = True
         
class EditFormWindow:
    def __init__(FormWindow,master,items):
        FormWindow.master = master
        
        RepeatedFunctions.WindowConfig(master,320,280,100,100)
        RepeatedFunctions.ProduceTitleCanvas(master,"Edit Form")
        FormWindow.ProduceEditForm(master,items)

        master.mainloop()

    def ProduceEditForm(FormWindow,master,items):

        FormWindow.Canv = Canvas(master)
        FormWindow.Canv.place(x=37,y=72,width = 245,height=200)
        FormWindow.Canv.create_rectangle(1,1,243,198,fill="#add8e6",width = 3,outline="grey")
        FormWindow.EditForm = LabelFrame(master,bg="#add8e6",bd=0)
        FormWindow.EditForm.place(x=47,y=83)

        Label(FormWindow.EditForm, text="First Name",bg="#add8e6").grid(row=0)
        Label(FormWindow.EditForm, text="Last Name",bg="#add8e6").grid(row=1)
        Label(FormWindow.EditForm, text="Company",bg="#add8e6").grid(row=2)
        Label(FormWindow.EditForm, text="Contact Number",bg="#add8e6").grid(row=3)
        Label(FormWindow.EditForm, text="Email",bg="#add8e6").grid(row=4)
        Label(FormWindow.EditForm, text="Address",bg="#add8e6").grid(row=5)
        Label(FormWindow.EditForm, text="Postcode",bg="#add8e6").grid(row=6)
        FormWindow.Submit = ttk.Button(FormWindow.EditForm,text="Submit",command= lambda: RepeatedFunctions.InputMask(FormWindow,master,FormWindow.EditForm,items,"FormWindow"))
        FormWindow.Submit.grid(row=7,pady=5)
        
        FormWindow.Firstname = Entry(FormWindow.EditForm)
        FormWindow.Firstname.grid(row=0, column=1)
        FormWindow.Firstname.insert(0,items["values"][0])
        FormWindow.Lastname = Entry(FormWindow.EditForm)
        FormWindow.Lastname.grid(row=1, column=1)
        FormWindow.Lastname.insert(0,items["values"][1])
        FormWindow.CompanyEntry = Entry(FormWindow.EditForm)
        FormWindow.CompanyEntry.grid(row=2, column=1)
        FormWindow.CompanyEntry.insert(0,items["values"][2])
        FormWindow.ContactNum = Entry(FormWindow.EditForm)
        FormWindow.ContactNum.grid(row=3, column=1)
        FormWindow.ContactNum.insert(0,items["values"][3])
        FormWindow.Email = Entry(FormWindow.EditForm)
        FormWindow.Email.grid(row=4, column=1)
        FormWindow.Email.insert(0,items["values"][4])
        FormWindow.Address = Entry(FormWindow.EditForm)
        FormWindow.Address.grid(row=5, column=1)
        FormWindow.Address.insert(0,items["values"][5])
        FormWindow.Postcode = Entry(FormWindow.EditForm)
        FormWindow.Postcode.grid(row=6, column=1)
        FormWindow.Postcode.insert(0,items["values"][6])
        FormWindow.StateLabel = Label(FormWindow.EditForm,text = "",bg = "#add8e6")
        FormWindow.StateLabel.grid(row=7, column=1)

    def ChangeDatabase(FormWindow,master,Confirm,items):
        
        Confirm.destroy()
        FormWindow.StateLabel.config(text = "Client Updated!!",fg="black")
        FormWindow.Submit.config(state = ACTIVE,text = "Return >",command = master.destroy)

        db = sqlite3.connect("Customers db.db") 
        c = db.cursor()
        c.execute("SELECT* FROM Customers")
        Result = c.fetchall()
        for x in range(len(Result)):
            if Result[x][1] == items["values"][0] and Result[x][2] == items["values"][1] and Result[x][3] == items["values"][2]:  
                CustID = Result[x][0]
                
         
        db.execute("UPDATE Customers SET Firstname=?,Surname=?,Company=?,Telephone=?,Email=?,Address=?,Postcode=? WHERE CustomerID=?",
                   (FormWindow.Firstname.get(),FormWindow.Lastname.get(),FormWindow.CompanyEntry.get(),int(FormWindow.ContactNum.get()),
                    FormWindow.Email.get(),FormWindow.Address.get(),FormWindow.Postcode.get(),CustID))
        db.commit()
        
        
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================

        
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
##----------------
        ButtonFilters = LabelFrame(FilterCanvas,bg = "#add8e6",bd=0)
        ButtonFilters.place(x=4,y=4,width = 200,height=120)
        
        Label(ButtonFilters,text = "Filter",font = ("Georgia",15),bg = "#add8e6").pack(side = TOP)
        
        self.Company = ttk.Combobox(ButtonFilters,state=DISABLED,width=10)
        db = sqlite3.connect("Customers db.db")
        Link = db.cursor()
        Companies = db.execute("SELECT Company FROM Customers")
        data = []
        for x in Companies:
            if max(x) != "":
                data.append(max(x))
        self.Company["values"] = data
        self.Company.place(x=100,y=30)

        #self.ApplyButton = ttk.Button(ButtonFilters,state=DISABLED,text = "Apply",command = self.ApplyFilter)
        #self.ApplyButton.pack(side=BOTTOM,pady = 8)

        self.Radio = IntVar()
        self.Radio.set(1)
        Radiobutton(ButtonFilters, text="Company", variable=self.Radio, value=1,bg = "#add8e6", command = lambda:self.EnableFilters(self.Radio)).place(x=10,y=30)
        Radiobutton(ButtonFilters, text="ASC", variable=self.Radio, value=2,bg = "#add8e6",  command = lambda:self.EnableFilters(self.Radio)).place(x=40,y=55)
        Radiobutton(ButtonFilters, text="DSC", variable=self.Radio, value=3,bg = "#add8e6", command = lambda:self.EnableFilters(self.Radio)).place(x=110,y=55)      
    def EnableFilters(self,Choice):
        if int(Choice.get()) == 1:
            print("1")
        elif int(Choice.get()) == 2:
            print("2")
        elif int(Choice.get()) == 3:
            print("3")
##----------------

    def ProduceAddClientForm(self,master):

        ClientAdd = Canvas(master)
        ClientAdd.place(x=492,y=72, width = 238, height = 187)
        ClientAdd.create_rectangle(1, 1, 236, 185, fill="#add8e6",width = 3
                                   ,outline="grey")
        self.QuickAdd = LabelFrame(ClientAdd, bg = "#add8e6",bd=0)
        self.QuickAdd.place(x=4,y=6)

        Label(self.QuickAdd, text="First Name",bg = "#add8e6" ).grid(row=0)
        Label(self.QuickAdd, text="Last Name",bg = "#add8e6" ).grid(row=1)
        Label(self.QuickAdd, text="Company",bg = "#add8e6" ).grid(row=2)
        Label(self.QuickAdd, text="Contact Number",bg = "#add8e6" ).grid(row=3)
        Label(self.QuickAdd, text="Email",bg = "#add8e6" ).grid(row=4)
        Label(self.QuickAdd, text="Address",bg = "#add8e6" ).grid(row=5)
        Label(self.QuickAdd, text="Postcode",bg = "#add8e6" ).grid(row=6)
        self.Submit = ttk.Button(self.QuickAdd,text="Add Client",command =
                                 lambda:RepeatedFunctions.InputMask(self,master,
                                                                    self.QuickAdd,
                                                                    "","Customers"))
        self.Submit.grid(row=7,pady=3)
    
        self.Firstname = Entry(self.QuickAdd)
        self.Firstname.grid(row=0, column=1)
        self.Lastname = Entry(self.QuickAdd)
        self.Lastname.grid(row=1, column=1)
        self.CompanyEntry = Entry(self.QuickAdd)
        self.CompanyEntry.grid(row=2, column=1)
        self.ContactNum = Entry(self.QuickAdd)
        self.ContactNum.grid(row=3, column=1)
        self.Email = Entry(self.QuickAdd)
        self.Email.grid(row=4, column=1)
        self.Address = Entry(self.QuickAdd)
        self.Address.grid(row=5, column=1)
        self.Postcode = Entry(self.QuickAdd)
        self.Postcode.grid(row=6, column=1)
        self.StateLabel = Label(self.QuickAdd,bg="#add8e6")
        self.StateLabel.grid(column=1,row=7)
        
    def DisplayAllRecords(self):
        self.ShowRecordsButton.config(state=DISABLED)
        db = sqlite3.connect("Customers db.db")
        c = db.cursor()
        c.execute("SELECT * FROM Customers")
        Result = c.fetchall()
        EachRec = []
        for Record in Result:
            EachRec.append((Record[1],Record[2],Record[3],Record[4],Record[5],Record[6],Record[7]))
        for item in EachRec:
            self.tree.insert('', 'end', values=item)
        self.AmountOfClients.config(text="Amount of Clients: "+str(len(self.tree.get_children())))

    def DeleteClient(self):
        myExit =messagebox.askyesno(title="Quit",message="Are you sure you want to delete\nthis client?")
        if myExit > 0:       
            try:
                items = self.tree.item(self.tree.selection())
                selectedItem = self.tree.selection()[0]
                self.tree.delete(selectedItem)

                db = sqlite3.connect("Customers db.db")
                c = db.cursor()
                c.execute("SELECT* FROM Customers")
                Result = c.fetchall()
                for x in range(len(Result)):
                    if Result[x][1] == items["values"][0] and Result[x][2] == items["values"][1] and Result[x][3] == items["values"][2]:
                        CustID = Result[x][0]

                db = sqlite3.connect("Customers db.db")
                c = db.cursor()
                query = "DELETE FROM Customers WHERE CustomerID = '%s';"%CustID
                c.execute(query)
                db.commit()
                db.close()
                
            except:
                selectedItem = "Deleted: None"
            self.AmountOfClients.config(text="Records: "+str(len(self.tree.get_children())))
            self.RemoveClient.config(state=DISABLED)
            self.EditClient.config(state=DISABLED)
           
    def SelectClient(self):

        items = self.tree.item(self.tree.selection())
        self.CFirstname.config(text = "Firstname: "+items["values"][0][:15])
        self.CLastname.config(text = "Lastname: "+items["values"][1][:15])
        self.CCompany.config(text = "Company: "+items["values"][2][:15])
        self.CTelephone.config(text = "Telephone: "+str(items["values"][3]))
        self.CEmail.config(text = "Email: "+items["values"][4][:15])
        self.CAddress.config(text = "Address: "+items["values"][5][:15])
        self.CPostcode.config(text = "Postcode: "+items["values"][6][:15])

        if self.CFirstname != "Client: None":
            self.RemoveClient.config(state=ACTIVE)
            self.EditClient.config(state=ACTIVE)

    def AddRecordToCustomerDatabase(self,Grid,master):
        
        self.ConfirmButton.destroy()
        self.StateLabel.config(text = "Client Added!!",fg="black")
        self.Submit.config(state = ACTIVE,text = "Add New",command = lambda:self.Reset("Reset",Grid,master))
        
        db = sqlite3.connect("Customers db.db")
        db.execute('''INSERT INTO Customers(Firstname,Surname,Company,Telephone,
                   Email,Address,Postcode)Values (?,?,?,?,?,?,?)''',
                  (self.Firstname.get(),self.Lastname.get(),
                   self.CompanyEntry.get(),self.ContactNum.get(),
                   self.Email.get(),self.Address.get(),
                   self.Postcode.get()))
        db.commit()

        if str(self.ShowRecordsButton["state"]) == "disabled":
            self.tree.insert('', 'end', values=(self.Firstname.get(),self.Lastname.get(),
                                                self.CompanyEntry.get(),self.ContactNum.get(),
                                                self.Email.get(),self.Address.get(),self.Postcode.get()))

    def Reset(self,text,Grid,master):
        self.Firstname.config(state = NORMAL)
        self.Lastname.config(state = NORMAL)
        self.CompanyEntry.config(state = NORMAL)
        self.ContactNum.config(state = NORMAL)
        self.Email.config(state = NORMAL)
        self.Postcode.config(state = NORMAL)
        self.Address.config(state = NORMAL)
        self.ConfirmButton.destroy()
        self.StateLabel.config(text = "")
        self.Submit.config(text="Add Client",command =lambda:
                           RepeatedFunctions.InputMask(self,master,Grid,"","Customers"))
        if text == "Reset":
            self.Firstname.delete(0,END)
            self.Lastname.delete(0,END)
            self.CompanyEntry.delete(0,END)
            self.Email.delete(0,END)
            self.ContactNum.delete(0,END)
            self.Postcode.delete(0,END)
            self.Address.delete(0,END)
            
    def OpenEditForm(self):
        root = Tk()
        items = self.tree.item(self.tree.selection())
        EditFormWindow(root,items)
        
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
#============================================================================================================================
        
class Parent:
    def __init__(Parent,master):
        Parent.master = master
        RepeatedFunctions.WindowConfig(master,738,260,(master.winfo_screenwidth()-738)/2,
                                       (master.winfo_screenheight()-260)/2)
        RepeatedFunctions.ProduceMenuCanvas(master,"Parent")
        
        #Parent.PlaceSaleQuickAddBox(master)
        #Parent.PlaceDescription(master)

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
