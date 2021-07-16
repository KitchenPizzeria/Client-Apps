from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re

# from Sales import Sales
# from Customers import Customers
# from CoalSticksLogs import CoalSticksLogs
# from Invoices import Invoices
# from EditFormWindow import EditFormWindow

BUTTON_FONT = ("Georgia",16)
TITLE_FONT = ("Georgia",28)

class Parent():
    def __init__(self,master):
        self.master = master

        windowWidth = (master.winfo_screenwidth() - 738) / 2
        windowHeight = (master.winfo_screenheight() - 260) / 2

        self.WindowConfig(738,260,windowWidth,windowHeight, master)
        self.ProduceMenuCanvas(master,"Parent")
        self.PlaceSaleQuickAddBox(master)
        self.PlaceDescription(master)

        master.mainloop()

    def WindowConfig(self,w,h,x,y,master):
        master.config(bg="#ffca00")
        master.resizable(0,0)
        master.geometry('%dx%d+%d+%d' % (w,h,x,y))
    
    def ProduceMenuCanvas(self,master,text):
        MenuCanvas = Canvas(master)
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
        ClientButton = ttk.Button(MenuCanvas,text = "Clients",width=15)
        #,command = Customers(Tk()))
        ClientButton.pack(pady=2)
        SalesButton = ttk.Button(MenuCanvas,text = "Sales",width=15)
        SalesButton.pack(pady = 2)
        #,command = Sales(Tk())).pack(pady=2)
        CoalSticksLogsButton = ttk.Button(MenuCanvas,text = "Coal Sticks Logs",width = 15)
        CoalSticksLogsButton.pack(pady = 2)
        #,command = CoalSticksLogs(Tk())).pack(pady=2)
        InvoicesButton = ttk.Button(MenuCanvas,text = "Invoices",width=15).pack(pady=2)


        Close = "Return >"
        if text == "Parent":
            Close = "Quit"
            
        ReturnButton = ttk.Button(MenuCanvas,text=Close,command = master.destroy).pack(side=BOTTOM,pady=7)
        
    def PlaceSaleQuickAddBox(self,master):

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

        db = sqlite3.connect("Customers.db")
        Link = db.cursor()

        Parent.Company = ttk.Combobox(QuickAddFrame,width = 6)
        Companies = db.execute("SELECT Company FROM Customers")
        CompanyValues = []
        for x in Companies:
            if max(x) != "":
                CompanyValues.append(max(x))
        CompanyValues = sorted(list(set(CompanyValues)))
        Parent.Company["values"] = CompanyValues

        Parent.Company.bind("<<ComboboxSelected>>", Parent.ActivateAndFillNameBox)

        Categories = db.execute("SELECT Category FROM Inventory")
        StockCat = []
        for x in Categories:
            if max(x) != "" or max(x)!="None":
                StockCat.append(max(x))
        Parent.Category = ttk.Combobox(QuickAddFrame,width = 6)
        StockCat = sorted(list(set(StockCat)))
        Parent.Category["values"] = StockCat

        Parent.Category.bind("<Configure>",self.CheckWidth(StockCat))
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

    def ActivateAndFillItemBox(self,event):
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
        self.CheckWidth(Parent.StockItems)
            
    def ActivateAndFillNameBox(self,event):
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
        self.CheckWidth(Parent.Names)

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

        
    def AddRecordToSalesDatabase(self,QuickAddFrame):
        Parent.Confirm.destroy()
        OrderID = self.ProduceUniqueOrderID(Parent.Name)
        
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
        pass
        #NewWin = Customers(Tk())
    def OpenSales():
        pass
        #NewWin = Sales(Tk())
    def OpenCSL():
        pass
        #NewWin = CoalSticksLogs(Tk())
    def OpenInvoices():
        pass
        #NewWin = Invoices(Tk())
   
    def TreeView(self,Header,tree,frame):

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
            tree.heading(col, text=col.title(), anchor = "w",command=lambda c=col: self.SortRecords(c,1,Header,tree))

    def SortRecords(self,col, descending,table_header,tree):
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
        tree.heading(col, command=lambda c=col:self.SortRecords
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
                                        self.ConfirmButton = ttk.Button(grid,text = "Confirm")
                                        #,command = lambda:Customers.AddRecordToCustomerDatabase(self,grid,master))
                                        self.ConfirmButton.grid(column = 1, row = 7)
                                        self.Submit.config(text = "Edit")
                                        #,command = lambda:Customers.Reset(self,"Edit",grid,master))
                                        
                                    elif text == "FormWindow":
                                        self.ConfirmButton = ttk.Button(grid,text = "Confirm")
                                        #,command = lambda:EditFormWindow.ChangeDatabase(self,master,self.ConfirmButton,items))
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
   
root = Tk()

backCanvas = Canvas(root, background = "#add8e6")
backCanvas.place(x=119,y=2, width = 375, height = 70)

MainWindow = Parent(root)

##http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
##http://stackoverflow.com/questions/20588417/how-to-change-font-and-size-of-buttons-and-frame-in-tkinter-using-python
