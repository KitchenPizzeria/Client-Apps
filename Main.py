from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re
from ttkthemes import ThemedTk

BUTTON_FONT = ("Georgia",16)
TITLE_FONT = ("Georgia",28)
DB = sqlite3.connect("Customers.db")
CONN = DB.cursor()

class Parent():
    def __init__(self,master):
        # Define Tk Window
        self.master = master

        # Define windows properties
        master.resizable(0,0)
        master.geometry('%dx%d' % (700, 700))
        master.title("DIY Digitised")

        # Style for Notebook
        style = ttk.Style()
        
        style.configure("TLabel", background = "#add8e6")
        style.configure("TNotebook", tabbackground = "#B7E9F7", tabposition = "N")
        style.configure(".", focuscolor = style.lookup('.', 'background'))
        style.configure('TNotebook.Tab', 
            background = "black", 
            width = 15, 
            foreground = "black",
            font = ("Helvetica", 13, "italic"),
            padding = (25, 10, 25, 10)
        )
        style.map("TNotebook", background = [("selected","#B7E9F7")])
        style.map("TNotebook.Tab",
            expand = [("selected", [-5, 0, -5, 0])], 
            background = [("selected","red")]
        )
    
        # style.theme_create("custom_tabs", parent = "alt", settings = {
        #     "." : {
        #         "configure": {
        #             "focuscolor" : style.lookup('.', 'background')
        #         }
        #     },
        #     "TNotebook": {
        #         "configure": {
        #             "background" : "#B7E9F7"
        #         }
        #     },
        #     "TNotebook.tab" : {
        #         "configure" : {
        #             "padding" : [0,0,0,0]
        #         } ,
        #         "map": {
        #             "background": [("selected", '#ccffff')], # Tab color when selected
        #             "expand": [("selected", [-5, 1, -5, 0])] # text margins
        #         }
        #     }
        # })

        # style.theme_use("custom_tabs")
        

        # Parent Widget Definitions
        self.notebook = ttk.Notebook(master, padding = 3)
        self.notebook.bind("<<NotebookTabChanged>>", self.loadOnClick)

        self.CustomersFrame = Frame(self.notebook, bg = "#B7E9F7")
        self.SalesFrame = Frame(self.notebook, bg = "#B7E9F7")
        self.InventoryFrame = Frame(self.notebook, bg = "#B7E9F7")
        self.InvoicesFrame = Frame(self.notebook, bg = "#B7E9F7")

        # Notebook/Frame Placement Rules
        self.notebook.pack()
        self.CustomersFrame.pack(fill = 'both', expand= True)
        self.SalesFrame.pack(fill = 'both', expand= True)
        self.InvoicesFrame.pack(fill = 'both', expand= True)
        self.InventoryFrame.pack(fill = 'both', expand= True)

        # Add frames to the Notebook
        self.notebook.add(self.CustomersFrame, text = "Customers")
        self.notebook.add(self.SalesFrame, text = "Sales")
        self.notebook.add(self.InventoryFrame, text = "Inventory")
        self.notebook.add(self.InvoicesFrame, text = "Invoices")
        
    # Load tab data only when the tab is selected, Remove all other data
    def loadOnClick(self,event):

        # Customer Tab Selected
        if str(self.notebook.index(self.notebook.select())) == "0":  
            # Reset all other tabs before populating new tab
            for x in self.CustomersFrame.winfo_children():
                x.destroy()
            for x in self.SalesFrame.winfo_children():
                x.destroy()
            for x in self.InventoryFrame.winfo_children():
                x.destroy()

            self.PopulateCustomersFrame(self.CustomersFrame)

        # Sales Tab Selected
        elif str(self.notebook.index(self.notebook.select())) == "1":
            # Reset all other tabs before populating new tab
            for x in self.CustomersFrame.winfo_children():
                x.destroy()
            for x in self.InvoicesFrame.winfo_children():
                x.destroy()
            for x in self.InventoryFrame.winfo_children():
                x.destroy()
            self.PopulateSalesFrame(self.SalesFrame)
            
        # Inventory Tab Selected
        elif str(self.notebook.index(self.notebook.select())) == "2":
            # Reset all other tabs before populating new tab
            for x in self.CustomersFrame.winfo_children():
                x.destroy()
            for x in self.SalesFrame.winfo_children():
                x.destroy()
            for x in self.InvoicesFrame.winfo_children():
                x.destroy()
            self.PopulateInventoryFrame(self.InventoryFrame)

        # Invoices Tab Selected
        elif str(self.notebook.index(self.notebook.select())) == "3":
            # Reset all other tabs before populating new tab
            for x in self.CustomersFrame.winfo_children():
                x.destroy()
            for x in self.SalesFrame.winfo_children():
                x.destroy()
            for x in self.InventoryFrame.winfo_children():
                x.destroy()
            self.PopulateInvoicesFrame(self.InvoicesFrame)  

    def PopulateCustomersFrame(self, Window):

        c = DB.execute("SELECT * FROM Customers")
        fields = [description[0] for description in c.description]

        self.TreeView(Window, fields).pack(side = BOTTOM)
        self.CustomerInformationPane(Window).pack(side = LEFT, pady = 5, padx = 5)
        self.AddClientForm(Window).pack(side = RIGHT)
    
    def PopulateSalesFrame(self, Window):
    
        c = DB.execute("SELECT * FROM Sales")
        fields = [description[0] for description in c.description]

        self.TreeView(Window, fields).pack(side = BOTTOM)
        self.AddSalesForm(Window).pack(side = RIGHT)
        self.SalesInformationPane(Window).pack(side=LEFT, padx = 2, pady =2)
    
    def PopulateInventoryFrame(self, Window):

        c = DB.execute("SELECT * FROM Inventory")
        fields = [description[0] for description in c.description]

        self.TreeView(Window, fields).pack(side = BOTTOM)
        self.AddInventoryForm(Window).pack(side = RIGHT)
        self.InventoryInformationPane(Window).pack(anchor = NW, padx = 2, pady = 2)

    def PopulateInvoicesFrame(self, Window):

        c = DB.execute("SELECT * FROM Invoices")
        fields = [description[0] for description in c.description]

        self.TreeView(Window, fields).pack(side = BOTTOM)
        #self.AddInventoryForm(Window).pack(side = RIGHT)
        self.InvoiceInformationPane(Window).pack(anchor = NW, padx = 2, pady = 2)


    def CustomerInformationPane(self, master):
    
        # Canvas Definitions
        rootCanvas = Canvas(master, bg = "#add8e6", width = 450, height = 280)
        InfoCanvas = Canvas(rootCanvas, bg = "#add8e6", highlightthickness= 1)
        ButtonCanvas = Canvas(rootCanvas)
        #PictureCanvas = Canvas(rootCanvas)   

        # Canvas Placements
        ButtonCanvas.pack(side = BOTTOM, pady=8, padx = 20)
        InfoCanvas.pack(side= RIGHT, padx= 30, pady= 25)
        #PictureCanvas.pack(side = LEFT)

        # Label Definitions
        self.CFirstname = Label(InfoCanvas, text = "Firstname: None",bg = "#add8e6")
        self.CLastname = Label(InfoCanvas, text = "Lastname: None",bg = "#add8e6")
        self.CCompany = Label(InfoCanvas, text = "Company: None",bg = "#add8e6")
        self.CTelephone = Label(InfoCanvas, text = "Telephone: None",bg = "#add8e6")
        self.CEmail = Label(InfoCanvas, text = "Email: None",bg = "#add8e6")
        self.CAddress = Label(InfoCanvas, text = "Address: None",bg = "#add8e6")
        self.CPostcode = Label(InfoCanvas, text = "Postcode: None",bg = "#add8e6")
        self.AmountOfClients = Label(InfoCanvas, text = "Amount of Clients: 0  ",bg = "#add8e6")
    
        # Label Placements
        self.CFirstname.pack(side = TOP, pady = (5,0))
        self.CLastname.pack(side = TOP)
        self.CCompany.pack(side = TOP)
        self.CTelephone.pack(side = TOP)
        self.CEmail.pack(side = TOP)
        self.CAddress.pack(side = TOP)
        self.CPostcode.pack(side = TOP)
        self.AmountOfClients.pack(side = TOP, pady = (0,5), padx = 5)

        # Button Definitions
        self.ShowRecordsButton = ttk.Button(ButtonCanvas, text = "Show clients", command = lambda: self.DisplayAllRecords("Customers"))
        self.SelectRecordButton= ttk.Button(ButtonCanvas, text = "Select", state = DISABLED, command = self.SelectClient)
        self.DeleteClientButton = ttk.Button(ButtonCanvas, text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.EditClientButton = ttk.Button(ButtonCanvas, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)
        
        # Button Placements
        self.ShowRecordsButton.grid(row=0,column=0)
        self.SelectRecordButton.grid(row=0,column=1)
        self.DeleteClientButton.grid(row=0,column=2)
        self.EditClientButton.grid(row=0,column=3)

        return rootCanvas

    def SalesInformationPane(self, master):

        infoFrame = Canvas(master, bg = "#add8e6")

        PerformanceCanvas = Canvas(infoFrame,
            bg = "#add8e6", 
            highlightthickness = 1, 
            width = 375)

        PerformanceTitle = Label(PerformanceCanvas, text = "Performance",bg = "#add8e6", font = ("helvetica",18, "italic"))
        daily = LabelFrame(PerformanceCanvas, text = "day", bg = "#add8e6")
        dailytext = Label(daily, text = "daily stats", bg = "#add8e6")
        monthly = LabelFrame(PerformanceCanvas, text = "month", bg = "#add8e6")
        monthlytext = Label(monthly, text = "monthly stats", bg = "#add8e6")
        annual = LabelFrame(PerformanceCanvas, text = "annual", bg = "#add8e6")
        annualtext = Label(annual, text = "annual stats", bg = "#add8e6")

        PerformanceCanvas.pack(padx = 5, pady= (5,10))
        PerformanceTitle.pack(padx = 5, pady = 5)  
        daily.pack(side = LEFT, padx = 25)
        monthly.pack(side = LEFT, padx = 25, pady = 5)
        annual.pack(side = LEFT, padx = 25, pady = 5)
        dailytext.pack()
        monthlytext.pack()
        annualtext.pack()

        FilterCanvas = Canvas(infoFrame, 
            bg = "#add8e6", 
            highlightthickness = 1, 
            width = 375)
        
        FilterTitle = Label(FilterCanvas, text = "Filter", bg = "#add8e6", font = ("helvetica",18, "italic"))
        FilterTitle.grid(row = 0, column = 0, columnspan = 4, pady=2)
        ItemLabel = Label(FilterCanvas, text = "Item:", bg = "#add8e6")
        ItemLabel.grid(row = 1, column=0, padx=5, pady = 5)
        ItemCombobox = ttk.Combobox(FilterCanvas, width = 10)
        ItemCombobox.grid(row=1, column=1)
        CheckButton = Checkbutton(FilterCanvas, text = "CSL", bg="#add8e6")
        CheckButton.grid(row=2, column=1)
        CompanyLabel = Label(FilterCanvas, text = "Company:", bg = "#add8e6")
        CompanyLabel.grid(row = 1, column=2, padx=5, pady = 5)
        CompanyCombobox = ttk.Combobox(FilterCanvas, width = 10)
        CompanyCombobox.grid(row=1, column=3, padx=5, pady = 5)
        ApplyButton = ttk.Button(FilterCanvas, text = "Apply")
        ApplyButton.grid(row = 2, column = 2, columnspan=2, padx=5, pady = 5)

        FilterCanvas.pack(padx= 8, pady= 8)

        ButtonCanvas = Canvas(infoFrame)

        # Button Definitions
        self.ShowRecordsButton = ttk.Button(ButtonCanvas, text = "Show clients", command = lambda: self.DisplayAllRecords("Sales"))
        self.SelectRecordButton= ttk.Button(ButtonCanvas, text = "Select", state = DISABLED, command = self.SelectClient)
        self.DeleteClientButton = ttk.Button(ButtonCanvas, text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.EditClientButton = ttk.Button(ButtonCanvas, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)
        
        # Button Placements
        self.ShowRecordsButton.grid(row=0,column=0)
        self.SelectRecordButton.grid(row=0,column=1)
        self.DeleteClientButton.grid(row=0,column=2)
        self.EditClientButton.grid(row=0,column=3)

        ButtonCanvas.pack(side=BOTTOM, pady = 10, padx = 5)
    
        return infoFrame
    
    def InventoryInformationPane(self, master):
    
        infoFrame = Canvas(master, bg = "#add8e6")

        # Frame Definitions
        PopularItemsCanvas = Canvas(infoFrame,
            bg = "#add8e6", 
            highlightthickness = 1, 
            width = 375)
        FilterCanvas = Canvas(infoFrame, 
            bg = "#add8e6", 
            highlightthickness = 1, 
            width = 375,
            height = 50)
        ButtonCanvas = Canvas(infoFrame)

        # Widget Definitions
        PopularTitle = Label(PopularItemsCanvas, text = "Popular Items",bg = "#add8e6", font = ("helvetica",18, "italic"))
        WeeklyTop5 = LabelFrame(PopularItemsCanvas, text = "Weekly Sales Top 5", bg = "#add8e6")
        LowItemsCanvas = Canvas(PopularItemsCanvas, highlightthickness=1, bg = "#add8e6")
        TopSeller = Label(WeeklyTop5, text = "Screws: 284", bg = "#add8e6")
        SecondSeller = Label(WeeklyTop5, text = "Fans: 104", bg = "#add8e6")
        ThirdSeller = Label(WeeklyTop5, text = "Plumbing: 84", bg = "#add8e6")
        FourthSeller = Label(WeeklyTop5, text = "Door Stops: 39", bg = "#add8e6")
        FifthSeller = Label(WeeklyTop5, text = "Fertiliser: 20", bg = "#add8e6")
        LowItemsTitle = Label(LowItemsCanvas, text = "Low Items", bg = "#add8e6")
        LowItemsName = Label(LowItemsCanvas, text = "Item" , bg = "#add8e6")
        LowItemsQuantity = Label(LowItemsCanvas, text = "Quantity", bg = "#add8e6")

        FilterTitle = Label(FilterCanvas, text = "Filter", bg = "#add8e6", font = ("helvetica",18, "italic"))
        ItemLabel = Label(FilterCanvas, text = "Category:", bg = "#add8e6")
        ItemCombobox = ttk.Combobox(FilterCanvas, width = 10)
        ApplyButton = ttk.Button(FilterCanvas, text = "Apply")

        # Widget Placements
        PopularTitle.pack(padx = 5, pady = 5) 
        WeeklyTop5.pack(side = LEFT, padx = 25, pady = (5,10))
        LowItemsCanvas.pack(side = RIGHT, padx = 5, pady = 5)
        TopSeller.pack()
        SecondSeller.pack()
        ThirdSeller.pack()
        FourthSeller.pack()
        FifthSeller.pack()

        LowItemsTitle.grid(row = 0, column = 0, columnspan = 2, pady=5)
        LowItemsName.grid(row = 1, column = 0)
        LowItemsQuantity.grid(row = 1, column = 1, padx = 5)

        LowItemsDict = {
            "Wicks": 30,
            "Grub Screws": 10,
            "Seeds": 3,
            "Batteries": 6,
            "Wall Plugs":1
        }

        for x in range(5):
            for y in range(2):
                if y % 2 == 0:
                    itemname = list(LowItemsDict)[x]
                    TextLabel = Label(LowItemsCanvas, text = "{0}".format(itemname),bg = "#add8e6")
                else:
                    Quantity = LowItemsDict[itemname]
                    TextLabel = Label(LowItemsCanvas, text = "{0}".format(Quantity),bg = "#add8e6")
                TextLabel.grid(row = x+2, column = y, padx = 2, pady = 2)
                
                
        
        FilterTitle.grid(row = 0, column = 0, columnspan = 4, pady=2)
        ItemLabel.grid(row = 1, column=0, padx=5, pady = 5)
        ItemCombobox.grid(row = 1, column = 1)
        ApplyButton.grid(row = 1, column = 2, columnspan=2, padx=5, pady = 5)

        # Button Definitions
        self.ShowRecordsButton = ttk.Button(ButtonCanvas, text = "Show clients", command = lambda: self.DisplayAllRecords("Inventory"))
        self.SelectRecordButton= ttk.Button(ButtonCanvas, text = "Select", state = DISABLED, command = self.SelectClient)
        self.DeleteClientButton = ttk.Button(ButtonCanvas, text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.EditClientButton = ttk.Button(ButtonCanvas, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)
        
        # Button Placements
        self.ShowRecordsButton.grid(row=0,column=0)
        self.SelectRecordButton.grid(row=0,column=1)
        self.DeleteClientButton.grid(row=0,column=2)
        self.EditClientButton.grid(row=0,column=3)

        # Canvas Placements
        PopularItemsCanvas.pack(padx = 5, pady= (5,10))
        FilterCanvas.pack(padx= 8, pady= 8)
        ButtonCanvas.pack(pady = 10, padx = 5)

        return infoFrame
    
    def InvoiceInformationPane(self, master):
        
        # Canvas Definitions
        rootCanvas = Canvas(master, bg = "#add8e6", width = 450, height = 280)
        InfoCanvas = Canvas(rootCanvas, bg = "#add8e6", highlightthickness= 1)
        ButtonCanvas = Canvas(rootCanvas)
        #PictureCanvas = Canvas(rootCanvas)   

        # Canvas Placements
        ButtonCanvas.pack(side = BOTTOM, pady=8, padx = 20)
        InfoCanvas.pack(side= RIGHT, padx= 30, pady= 25)
        #PictureCanvas.pack(side = LEFT)

        # Label Definitions
        self.CFirstname = Label(InfoCanvas, text = "To be Paid",bg = "#add8e6")
    
        # Label Placements
        self.CFirstname.pack(side = TOP, pady = (5,0))

        # Button Definitions
        self.ShowRecordsButton = ttk.Button(ButtonCanvas, text = "Show clients", command = lambda: self.DisplayAllRecords("Invoices"))
        self.SelectRecordButton= ttk.Button(ButtonCanvas, text = "Select", state = DISABLED, command = self.SelectClient)
        self.DeleteClientButton = ttk.Button(ButtonCanvas, text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.EditClientButton = ttk.Button(ButtonCanvas, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)

        # Button Placements
        self.ShowRecordsButton.grid(row=0,column=0)
        self.SelectRecordButton.grid(row=0,column=1)
        self.DeleteClientButton.grid(row=0,column=2)
        self.EditClientButton.grid(row=0,column=3)

        return rootCanvas

    # Populate Tableview for each tab     
    def DisplayAllRecords(self, table):

        self.ShowRecordsButton.config(state = DISABLED)
        self.SelectRecordButton.config(state = NORMAL)

        CONN.execute("SELECT * FROM {0}".format(table))
        Result = CONN.fetchall()
        for Record in Result:
            self.tree.insert('', 'end', values=Record)
        self.AmountOfClients.config(text="Amount of Clients: "+str(len(self.tree.get_children())))

    def DeleteClient(self):
        myExit =messagebox.askyesno(title="Quit",message="Are you sure you want to delete\nthis client?")
        if myExit > 0:       
            try:
                items = self.self.tree.item(self.self.tree.selection())
                selectedItem = self.self.tree.selection()[0]
                self.self.tree.delete(selectedItem)

                db = sqlite3.connect("Customers.db")
                c = db.cursor()
                c.execute("SELECT* FROM Customers")
                Result = c.fetchall()
                for x in range(len(Result)):
                    if Result[x][1] == items["values"][0] and Result[x][2] == items["values"][1] and Result[x][3] == items["values"][2]:
                        CustID = Result[x][0]

                db = sqlite3.connect("Customers.db")
                c = db.cursor()
                query = "DELETE FROM Customers WHERE CustomerID = '%s';"%CustID
                c.execute(query)
                db.commit()
                db.close()
                
            except:
                selectedItem = "Deleted: None"
            self.AmountOfClients.config(text="Records: "+str(len(self.self.tree.get_children())))
            self.RemoveClient.config(state=DISABLED)
            self.EditClient.config(state=DISABLED)
     
    def SelectClient(self):
    
        self.tree.selection_clear()
        self.DeleteClientButton.config(state=ACTIVE)
        self.EditClientButton.config(state=ACTIVE)

        if self.SelectRecordButton["text"] == "Return":
            self.SelectRecordButton.config(text="Select")
        elif self.SelectRecordButton["text"] == "Select":
            self.SelectRecordButton.config(text="Return")

        items = self.self.tree.item(self.self.tree.selection())
        self.CFirstname.config(text = "Firstname: "+items["values"][0][:20])
        self.CLastname.config(text = "Lastname: "+items["values"][1][:20])
        self.CCompany.config(text = "Company: "+items["values"][2][:20])
        self.CTelephone.config(text = "Telephone: "+str(items["values"][3]))
        self.CEmail.config(text = "Email: "+items["values"][4][:20])
        self.CAddress.config(text = "Address: "+items["values"][5][:20])
        self.CPostcode.config(text = "Postcode: "+items["values"][6][:20])

    def PopulateEditForm(self):
    
        self.Submit.config(text="Modify")
        self.DeleteClientButton.config(state = DISABLED)
        
        items = self.self.tree.item(self.self.tree.selection())
        self.self.tree.delete(*self.self.tree.get_children())

        self.Firstname.insert(0,items["values"][0])
        self.Lastname.insert(0,items["values"][1])
        self.CompanyEntry.insert(0,items["values"][2])
        self.ContactNum.insert(0,items["values"][3])
        self.Email.insert(0,items["values"][4])
        self.Address.insert(0,items["values"][5])
        self.Postcode.insert(0,items["values"][6])
    
    def AddClientForm(self,master):
        
        AddClient = Canvas(master, bg = "#add8e6", width = 310, height = 240)

        # Label Definitions/Placements
        Label(AddClient, text="First Name",bg = "#add8e6" ).grid(row=0, pady=(5,0))
        Label(AddClient, text="Last Name",bg = "#add8e6" ).grid(row=1)
        Label(AddClient, text="Company",bg = "#add8e6" ).grid(row=2)
        Label(AddClient, text="Contact Number",bg = "#add8e6" ).grid(row=3, padx = (5,0))
        Label(AddClient, text="Email",bg = "#add8e6" ).grid(row=4)
        Label(AddClient, text="Address",bg = "#add8e6" ).grid(row=5)
        Label(AddClient, text="Postcode",bg = "#add8e6" ).grid(row=6)
        self.Submit = ttk.Button(AddClient, text="Add Client", command =
                                 lambda:self.InputMask(master, AddClient, "", "Customers"))
        self.Submit.grid(row=7,pady=(0,8))

        # Entry Definitions
        self.Firstname = ttk.Entry(AddClient)
        self.Lastname = ttk.Entry(AddClient)
        self.CompanyEntry = ttk.Entry(AddClient)
        self.ContactNum = ttk.Entry(AddClient)
        self.Email = ttk.Entry(AddClient)
        self.Address = ttk.Entry(AddClient)
        self.Postcode = ttk.Entry(AddClient)
        self.StateLabel = Label(AddClient, bg="#add8e6")

        # Entry Placement
        self.Firstname.grid(row=0, column=1, pady= (5,0), padx = (0,5))
        self.Lastname.grid(row=1, column=1, pady = (2,0), padx = (0,5))
        self.CompanyEntry.grid(row=2, column=1,  pady = (2,0), padx = (0,5))
        self.ContactNum.grid(row=3, column=1, pady = (2,0), padx = (0,5))
        self.Email.grid(row=4, column=1, pady = (2,0), padx = (0,5))
        self.Address.grid(row=5, column=1, pady = (2,0), padx = (0,5))
        self.Postcode.grid(row=6, column=1,  pady = (2,0), padx = (0,5))
        self.StateLabel.grid(column=1,row=7,  pady = (2,0), padx = (0,5))

        return AddClient
    
    def ActivateAndFillItemBox(self,event):
        db = sqlite3.connect("Customers.db")
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
        db = sqlite3.connect("Customers.db")
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
        db = sqlite3.connect("Customers.db")
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
        
        db = sqlite3.connect("Customers.db")
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
        c.execute('''INSERT INTO self(OrderID,ProductID,Quantity,CoalSticksLogs)Values
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
        
    def ProduceUniqueOrderID(Name):
        now = datetime.datetime.now()
        Date = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        
        db = sqlite3.connect("Customers.db")

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
     
        pass
        #NewWin = Invoices(Tk())
   
    def TreeView(self, master, fields):

        treeFrame = Frame(master)
        self.tree = ttk.Treeview(treeFrame, columns = fields, show = "headings")
        self.tree.grid(row = 0, column=0, in_= treeFrame)
        
        ScrollBar = ttk.Scrollbar(treeFrame, orient='vertical', command=self.tree.yview)
        ScrollBar.grid(row = 0, column = 1 , sticky='ns',in_= treeFrame)
        self.tree.configure(yscrollcommand=ScrollBar.set)

        width = 655
        HeaderLength = 0
        for x in fields:
            HeaderLength += len(x)
        
        for x in range(len(fields)):
            self.tree.column(fields[x],width=int(len(fields[x])/HeaderLength*width))
        
        for col in fields:
            self.tree.heading(col, text=col.title(), anchor = "n", command=lambda c=col: self.SortRecords(c,1,fields,self.tree))

        return treeFrame

    def SortRecords(self,col, descending,table_header, tree):
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
        self.tree.delete(*self.tree.get_children()) 
        for item in List:
            self.tree.insert('', 'end', values=item) 
        self.tree.heading(col, command=lambda c=col:self.SortRecords
                     (c,int(not descending),table_header,self.tree))

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
                                    self.StateLabel.config(text= "Error: Address", fg="red")
                            else:
                                self.StateLabel.config(text= "Error: Company", fg="red")
                        else:
                            self.StateLabel.config(text= "Error: Surname", fg="red")
                    else:
                        self.StateLabel.config(text= "Error: Firstname", fg="red")
                else:
                    self.StateLabel.config(text= "Error: Postcode", fg="red")
            else:
                self.StateLabel.config(text= "Error: Email", fg="red")
        else:
            self.StateLabel.config(text= "Error: Contact Number", fg="red")

    def AddSalesForm(self, master):
        
        AddSaleCanvas = Canvas(master, highlightthickness = 1, bg = "#add8e6", width = 300, height = 300)
        
        # Label Definitions
        Label(AddSaleCanvas, text="Company", bg="#add8e6").grid(row=1, pady = 2)
        Label(AddSaleCanvas, text="Client", bg="#add8e6").grid(row=2, pady = 2)
        Label(AddSaleCanvas, text="Category", bg="#add8e6").grid(row=3, pady = 2)
        Label(AddSaleCanvas, text="Item", bg="#add8e6").grid(row=4, pady = 2)
        Label(AddSaleCanvas, text = "Quantity", bg="#add8e6").grid(row=5, pady = 2)
        Label(AddSaleCanvas, text = "Unit Price", bg="#add8e6").grid(row=6, pady = 2)
        Label(AddSaleCanvas, text = "Total", bg="#add8e6").grid(row=7, pady = 2)

        self.CheckButton = Checkbutton(AddSaleCanvas, text = "CSL?", bg="#add8e6")
        self.Item = ttk.Combobox(AddSaleCanvas, state = DISABLED, width = 20)
        self.Name = ttk.Combobox(AddSaleCanvas, state = DISABLED, width = 20)

        db = sqlite3.connect("Customers.db")
        Link = db.cursor()

        self.Company = ttk.Combobox(AddSaleCanvas, width = 20)
        Companies = db.execute("SELECT Company FROM Customers")
        CompanyValues = []
        for x in Companies:
            if max(x) != "":
                CompanyValues.append(max(x))
        CompanyValues = sorted(list(set(CompanyValues)))
        self.Company["values"] = CompanyValues
        
        self.Company.bind("<Configure>",Parent.CheckWidth(CompanyValues))
        self.Company.bind("<<ComboboxSelected>>",self.ActivateAndFillNameBox)
        
        self.Category = ttk.Combobox(AddSaleCanvas,width = 20)
        Categories = db.execute("SELECT Category FROM Inventory")
        StockCat = []
        for x in Categories:
            if max(x) != "" or max(x)!="None":
                StockCat.append(max(x))
        StockCat = sorted(list(set(StockCat)))
        self.Category["values"] = StockCat

        self.Category.bind("<Configure>",Parent.CheckWidth(StockCat))
        self.Category.bind("<<ComboboxSelected>>",self.ActivateAndFillItemBox)

        self.Quantity = ttk.Entry(AddSaleCanvas,width = 20)
        self.UnitPrice = Label(AddSaleCanvas,bg="#add8e6")  
        self.Total = Label(AddSaleCanvas,bg="#add8e6")  
        self.StateLabel = Label(AddSaleCanvas,width = 10,bg="#add8e6")
        self.UniqueIDRepeat = True
        self.AddSale = ttk.Button(AddSaleCanvas,text="Add Sale",command = lambda: self.CheckandConfirm(QuickAddFrame,self.UniqueIDRepeat))
        self.Confirm = ttk.Button(AddSaleCanvas,state=DISABLED,text = "Confirm")

        self.CheckButton.grid(row = 0,column=1,columnspan = 2, pady = (5,0), padx = 2)
        self.Company.grid(row = 1,column=1,columnspan = 2, pady = 2, padx = 2)
        self.Name.grid(row = 2,column=1,columnspan = 2, pady = 2, padx = 2)
        self.Category.grid(row = 3,column=1,columnspan = 2, pady = 2, padx = 2)
        self.Item.grid(row = 4,column=1,columnspan = 2, pady = 2, padx = 2)
        self.Quantity.grid(row = 5,column=1,columnspan = 2, pady = 2, padx = 2)
        self.UnitPrice.grid(row = 6,column =1, pady = 2, padx = 2)
        self.Total.grid(row = 7,column=1, pady = 2, padx = 2)
        self.AddSale.grid(row=8, padx = 1, pady = 2)
        self.Confirm.grid(row=8,column=1, padx=(0,5), pady = 2)
        self.StateLabel.grid(row = 8,column=2, padx = 1, pady = 2)  

        return AddSaleCanvas  

    def AddInventoryForm(self, master):
        
        AddItemCanvas = Canvas(master, highlightthickness = 1, bg = "#add8e6", width = 300, height = 300)
        
        # Widget Definitions
        TotalItemsLabel = Label(AddItemCanvas, text = "Total Items: 0", bg = "#add8e6")
        AddItemsTitle = Label(AddItemCanvas, text = "Add Items",bg = "#add8e6", font = ("Helvetica", 18, "bold"))
        CategoryLabel = Label(AddItemCanvas, text = "Category", bg="#add8e6")
        DescriptionLabel = Label(AddItemCanvas, text= "Description", bg="#add8e6")
        UnitPriceLabel = Label(AddItemCanvas, text="Unit Price", bg="#add8e6")
        CategoryCombobox = ttk.Combobox(AddItemCanvas, state = DISABLED, width = 20)
        DescriptionEntry = ttk.Entry(AddItemCanvas,width = 20)
        UnitPriceEntry = ttk.Entry(AddItemCanvas,width = 20)
        StateLabel = Label(AddItemCanvas, width = 10, bg="#add8e6")
        self.UniqueIDRepeat = True
        AddSaleButton = ttk.Button(AddItemCanvas,text="Add Item")
        ConfirmButton= ttk.Button(AddItemCanvas,state=DISABLED,text = "Confirm")

        # Widget Placements
        TotalItemsLabel.grid(row=0, column = 1, pady = 5)
        AddItemsTitle.grid(row = 1, column=0, columnspan=3, pady = 5)
        CategoryLabel.grid(row=2,column = 0, pady = 2)
        DescriptionLabel.grid(row=3,column =0,  pady = 2)
        UnitPriceLabel.grid(row=4,column = 0, pady = 2)
        CategoryCombobox.grid(row = 2, column = 1, columnspan = 2, pady = 5)
        DescriptionEntry.grid(row = 3, column = 1, columnspan = 2, pady = 5)
        UnitPriceEntry.grid(row = 4, column = 1, columnspan = 2, pady = 5)
        AddSaleButton.grid(row = 5, column = 0 , pady = 10, padx = (10,0))
        ConfirmButton.grid(row = 5, column = 1, pady = 5)
        StateLabel.grid(row = 5, column = 2, pady = 5)
        

        # db = sqlite3.connect("Customers.db")
        # Link = db.cursor()

        # self.Company = ttk.Combobox(AddSaleCanvas, width = 20)
        # Companies = db.execute("SELECT Company FROM Customers")
        # CompanyValues = []
        # for x in Companies:
        #     if max(x) != "":
        #         CompanyValues.append(max(x))
        # CompanyValues = sorted(list(set(CompanyValues)))
        # self.Company["values"] = CompanyValues
        
        # self.Company.bind("<Configure>",Parent.CheckWidth(CompanyValues))
        # self.Company.bind("<<ComboboxSelected>>",self.ActivateAndFillNameBox)
        
        # self.Category = ttk.Combobox(AddSaleCanvas,width = 20)
        # Categories = db.execute("SELECT Category FROM Inventory")
        # StockCat = []
        # for x in Categories:
        #     if max(x) != "" or max(x)!="None":
        #         StockCat.append(max(x))
        # StockCat = sorted(list(set(StockCat)))
        # self.Category["values"] = StockCat

        # self.Category.bind("<Configure>",Parent.CheckWidth(StockCat))
        # self.Category.bind("<<ComboboxSelected>>",self.ActivateAndFillItemBox)

        
        
        return AddItemCanvas  

if __name__ == "__main__":
    root = ThemedTk(theme = "arc")
    MainWindow = Parent(root)
    root.mainloop()

##http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
##http://stackoverflow.com/questions/20588417/how-to-change-font-and-size-of-buttons-and-frame-in-tkinter-using-python
