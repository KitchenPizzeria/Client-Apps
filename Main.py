from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re
from ttkthemes import ThemedTk
import numpy as np

BUTTON_FONT = ("Georgia",16)
TITLE_FONT = ("Georgia",28)

DB = sqlite3.connect("Customers.db")
CONN = DB.cursor()

class Parent():
    def __init__(self,master):
        # Define Tk Window
        self.master = master

        # Define windows properties
        self.WindowHeight = 530
        self.WindowWidth = 700
        master.resizable(0,0)
        master.geometry('%dx%d' % (self.WindowWidth, self.WindowHeight))
        master.title("DIY Digitised")

        # Style for Notebook
        style = ttk.Style()

        style.configure("TLabel", background = "#add8e6")
        style.configure("TNotebook", tabbackground = "#B7E9F7", tabposition = "N")
        style.configure(".", focuscolor = style.lookup('.', 'background'))
        style.configure('TNotebook.Tab',
            width = 15,
            bg = "red",
            foreground = "black",
            font = ("Helvetica", 13, "italic"),
            padding = (40, 10, 40, 10)
        )
        style.configure("Secondary.TreeView", rowheight=45)
        style.map("TNotebook", background = [("selected","#B7E9F7")])

        style.map("TNotebook.Tab",
            expand = [("selected", [-8, 0, -8, -2])],
        )

        self.notebook = ttk.Notebook(master, padding = 3)
        self.currentNotebooktab = 0
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
        self.notebook.add(self.CustomersFrame, text = "Customers", sticky = NE)
        self.notebook.add(self.SalesFrame, text = "Sales")
        self.notebook.add(self.InventoryFrame, text = "Inventory")
        self.notebook.add(self.InvoicesFrame, text = "Invoices")

    def loadOnClick(self,event):

        tabList = [
            self.CustomersFrame,
            self.SalesFrame,
            self.InventoryFrame,
            self.InvoicesFrame
        ]

        # clear all widgets from starting tab
        startTab = tabList[self.currentNotebooktab]

        for x in startTab.winfo_children():
            x.destroy()

        # then update current tab and initialise all new widgets in destination tab

        self.indexOfCurrentNotebooktab = self.notebook.index(self.notebook.select())

        if self.currentNotebooktab == 0:
            self.PopulateCustomersFrame(self.CustomersFrame)
        if self.currentNotebooktab == 1:
            self.PopulateSalesFrame(self.SalesFrame)
        if self.currentNotebooktab == 2:
            self.PopulateInventoryFrame(self.InventoryFrame)
        if self.currentNotebooktab == 3:
            self.PopulateInvoicesFrame(self.InvoicesFrame)

    def PopulateCustomersFrame(self, Window):

        width = 380
        height = 210

        result = DB.execute("SELECT * FROM Customers")
        fields = [description[0] for description in result.description]

        # Canvas Definitions
        background_canvas = self.RoundedCorneredCanvas(self.CustomersFrame, width, height, 15)
        info_canvas = Frame(background_canvas, bg = "#add8e6")
        button_canvas = Frame(background_canvas, bg = "#add8e6")
        #PictureCanvas = Canvas(rootCanvas)

        # Canvas Placements
        button_canvas.pack(side = BOTTOM, pady = 8, padx = 2)
        info_canvas.pack(anchor = NE, padx= 5, pady= 5)
        #PictureCanvas.pack(side = LEFT)

        # Label Definitions
        self.CFirstname = Label(info_canvas, text = "Firstname: None",bg = "#add8e6")
        self.CLastname = Label(info_canvas, text = "Lastname: None",bg = "#add8e6")
        self.CCompany = Label(info_canvas, text = "Company: None",bg = "#add8e6")
        self.CTelephone = Label(info_canvas, text = "Telephone: None",bg = "#add8e6")
        self.CEmail = Label(info_canvas, text = "Email: None",bg = "#add8e6")
        self.CAddress = Label(info_canvas, text = "Address: None",bg = "#add8e6")
        self.CPostcode = Label(info_canvas, text = "Postcode: None",bg = "#add8e6")
        self.AmountOfClients = Label(info_canvas, text = "Amount of Clients: 0  ",bg = "#add8e6")

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
        self.ShowRecordsButton = ttk.Button(button_canvas, width = 10,text = "Show Clients",command = lambda: self.DisplayAllRecords("Customers"))
        self.DeleteClientButton = ttk.Button(button_canvas,width = 8,text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.EditClientButton = ttk.Button(button_canvas, width = 8, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)

        # Button Placements
        self.ShowRecordsButton.grid(row=0,column=0, padx = 3)
        self.DeleteClientButton.grid(row=0,column=1, padx = 3)
        self.EditClientButton.grid(row=0,column=2, padx = 3)

        self.customers_treeview = self.TreeView(Window, fields[1:], self.WindowWidth)
        self.customers_treeview.pack(side = BOTTOM)

        self.AddClientForm(Window).pack(side = RIGHT, pady = 5)
        background_canvas.place(x = 5, y = 5 , width = 380, height = 210)
    
    def DefaultCustomerSelectedInfo(self):

        self.CFirstname.config(text = "Firstname: None")
        self.CLastname.config(text = "Lastname: None")
        self.CCompany.config(text = "Company: None")
        self.CTelephone .config(text = "Telephone: None")
        self.CEmail .config(text = "Email: None")
        self.CAddress.config(text = "Address: None")
        self.CPostcode.config(text = "Postcode: None")
        self.AmountOfClients.config(text = "Amount of Clients: 0  ")


    def PopulateSalesFrame(self, Window):

        c = DB.execute("SELECT * FROM Sales")
        fields = [description[0] for description in c.description]

        self.TreeView(Window, fields[1:], self.WindowWidth).pack(side = BOTTOM)
        self.AddSalesForm(Window).pack(side = RIGHT)

        self.height = 250
        self.width = 370
        self.roundedRectangleCanvas = Canvas(Window, highlightthickness = 0, bg= "#B7E9F7")

        self.RoundedCorneredCanvas(self.roundedRectangleCanvas, 5, 5, self.width - 5, self.height-5, 20, "#ffffff")
        self.SalesInformationPane().pack(side=LEFT, padx = 2, pady =2)

        self.roundedRectangleCanvas.place(x = 5, y = 5, height = self.height, width = self.width)

    def PopulateInventoryFrame(self, Window):

        c = DB.execute("SELECT * FROM Inventory")
        fields = [description[0] for description in c.description]

        PopularItemsCanvas = self.RoundedCorneredCanvas(self.InventoryFrame, 370, 215, 15, "#add8e6")

        # Popular Items Canvas
        # Definitions
        PopularItemsTitle = Label(PopularItemsCanvas, text = "Popular Items", bg = "#add8e6" , font = ("Helvetica", 15, "bold"))

        TableFrame = Frame(PopularItemsCanvas, bg = "#add8e6")
        EbayLowItem = self.TreeView(TableFrame, ["Item", "Quantity"], 175, height = 2.5, scrollpresent=False)
        ShopLowItem = self.TreeView(TableFrame, ["Item", "Quantity"], 175, height = 2.5, scrollpresent=False)

        ButtonFrame = Frame(PopularItemsCanvas, bg = "#add8e6" )
        ShowItemsButton = ttk.Button(ButtonFrame,width = 8,text = "Show",command = lambda: self.DisplayAllRecords("Customers"))
        SelectItemButton= ttk.Button(ButtonFrame,width = 8, text = "Select", state = DISABLED, command = self.SelectClient)
        DeleteItemButton = ttk.Button(ButtonFrame,width = 8, text = "Delete", state = DISABLED, command = self.DeleteClient)
        EditItemButton = ttk.Button(ButtonFrame, width = 8,text = "Edit info", state = DISABLED, command = self.PopulateEditForm)

        PopularItemsTitle.pack(side = TOP, fill = "x", padx = 6, pady = (5,0))

        TableFrame.pack(side = TOP)
        Label(TableFrame, text = "Ebay Low Items", bg = "#add8e6").grid(row = 0, column = 0)
        Label(TableFrame, text = "Store Low Items", bg = "#add8e6").grid(row = 0, column = 1)
        ShopLowItem.grid(row = 1, column = 1, padx = 5)
        EbayLowItem.grid(row = 1, column = 0, padx = 5)
        ttk.Separator(PopularItemsCanvas, orient = "horizontal").pack(pady = 2)
        ButtonFrame.pack(side = BOTTOM, padx = 5, pady = (0,10))
        ShowItemsButton.grid(row=0,column=0, padx = 3)
        SelectItemButton.grid(row=0,column=1, padx = 3)
        DeleteItemButton.grid(row=0,column=2, padx = 3)
        EditItemButton.grid(row=0,column=3, padx = 3)

        # Write Code to populate the low items tables

        # ADD ITEMS CANVAS
        AddItemCanvas = self.RoundedCorneredCanvas(self.InventoryFrame, 201, 215, 15, "#add8e6")
        Label(AddItemCanvas, text = "Add Item", font = "Helvetica 15 bold", bg = "#add8e6").grid(row = 0, columnspan=4, pady = 3)
        Label(AddItemCanvas, text = "Company", bg = "#add8e6").grid(row = 1, column = 0, columnspan=2, pady = (10,5))
        ttk.Combobox(AddItemCanvas, width = 8).grid(row = 1, column = 2, columnspan=2)
        Label(AddItemCanvas, text = "Other: ", bg = "#add8e6").grid(row = 2, column = 0, columnspan=2, pady = 5)
        ttk.Entry(AddItemCanvas, width = 8).grid(row = 2, column = 2, columnspan=2)
        Label(AddItemCanvas, text = "Description: ", bg = "#add8e6").grid(row = 3, column = 0, columnspan=2, padx = 5, pady = 5)
        ttk.Entry(AddItemCanvas, width = 8).grid(row = 3, column = 2, columnspan=2)
        Label(AddItemCanvas, text = "Unit Price: ", bg = "#add8e6").grid(row = 4, column = 0, columnspan=2, pady = 5)
        ttk.Entry(AddItemCanvas, width = 3).grid(row = 4, column= 2, columnspan = 1)
        Label(AddItemCanvas, text = "error", foreground= "red", bg = "#add8e6").grid(row = 4, column = 3)

        self.TreeView(Window, fields[1:], self.WindowWidth).pack(side = BOTTOM)
        PopularItemsCanvas.place(x = 1, y = 1, width = 371, height = 216)
        AddItemCanvas.place(x = 483, y = 1, width = 201, height = 216)

    def PopulateInvoicesFrame(self, Window):

        c = DB.execute("SELECT * FROM Invoices")
        fields = [description[0] for description in c.description]

        toBePaidWidth = 226
        toBePaidHeight = 217

        # WIDGET DEFINITIONS
        treeView = self.TreeView(Window, fields[1:], self.WindowWidth)
        LeftCanvas = self.RoundedCorneredCanvas(Window, toBePaidWidth, toBePaidHeight, 15, "#add8e6" )
        MiddleCanvas = self.RoundedCorneredCanvas(Window, toBePaidWidth, toBePaidHeight, 15, "#add8e6" )
        RightCanvas = self.RoundedCorneredCanvas(Window, toBePaidWidth, toBePaidHeight, 15, "#add8e6" )

        # LEFT CANVAS CONTENT
        # Definitions
        LeftCanvasTitle = Label(LeftCanvas, text = "To Be Paid", bg = "#add8e6" , font = ("Helvetica", 15, "bold"))
        treeViewFrame = Frame(LeftCanvas)
        toBePaidTreeView = self.TreeView(treeViewFrame, ["Date", "Company","Paid"], toBePaidWidth-20)
        AmountDueLabel = Label(LeftCanvas, text = "Amount Due: 0", bg = "#add8e6")

        # Placements
        LeftCanvasTitle.pack(side = TOP, pady = (10,10), padx = 2)
        toBePaidTreeView.pack()
        treeViewFrame.pack(side = TOP, pady = (0,10), padx = 13)
        AmountDueLabel.pack(side = TOP, pady = 5, padx = 2)

        # MIDDLE CANVAS CONTENT
        # Definitions
        Label(MiddleCanvas, text = "eBay To Be Paid", bg = "#add8e6", font = ("Helvetica", 15, "bold")).pack(side = TOP, pady = (3,0))

        self.TreeView(MiddleCanvas,["Item Sold", "Date", "Due"], 185, 1, scrollpresent=False).pack(side = TOP, pady = 3)


        filterCanvas = Frame(MiddleCanvas, bg = "#add8e6")
        CompanyLabel = Label(filterCanvas, text = "Company:", bg = "#add8e6")
        CompanyComboBox = ttk.Combobox(filterCanvas, width = 9)
        DateFromLabel = Label(filterCanvas, text = "Date:", bg = "#add8e6")
        DateFromEntry = Entry(filterCanvas, width = 2)
        DateToLabel = Label(filterCanvas, text = "To:", bg = "#add8e6")
        DateToEntry = Entry(filterCanvas, width = 2)
        showInvoicesButton = ttk.Button(filterCanvas, text = "Show")
        clearInvoicesButton = ttk.Button(filterCanvas, text = "Clear")

        # Placements

        #TableFrame.pack(side = TOP, fill = "both", expand = True, padx = 5, pady = 5)
        ttk.Separator(MiddleCanvas, orient= "horizontal").pack(side = TOP)

        filterCanvas.pack(side = TOP, padx = 6, pady = (0,10))

        CompanyLabel.grid(row = 1, column = 0, columnspan=2, padx = 2, pady = 2)
        CompanyComboBox.grid(row = 1, column = 2, columnspan=2, padx = 2, pady = 2, sticky = "ew")
        DateFromLabel.grid(row = 2, column = 0, padx = 2, pady = 2)
        DateFromEntry.grid(row = 2, column = 1, padx = 2, pady = 2)
        DateToLabel.grid(row = 2, column = 2, padx = 2, pady = 2)
        DateToEntry.grid(row = 2, column = 3, padx = 2, pady = 2)
        showInvoicesButton.grid(row = 3, column = 0, columnspan = 2, padx = 2, pady = 2)
        clearInvoicesButton.grid(row = 3, column = 2, columnspan = 2 , padx = 2, pady = 2)

        # RIGHT CANVAS
        # Definitions
        RightCanvasTitle = Label(RightCanvas, text = "Generate", bg = "#add8e6", font = ("Helvetica", 15, "bold"))
        formCanvas = Frame(RightCanvas, bg = "#add8e6")
        FilterTitle = Label(formCanvas, text = "Filter", bg = "#add8e6")
        CompanyLabel = Label(formCanvas, text = "Company:", bg = "#add8e6")
        CompanyComboBox = ttk.Combobox(formCanvas, width = 9)
        DateFromLabel = Label(formCanvas, text = "Date:", bg = "#add8e6")
        DateFromEntry = Entry(formCanvas, width = 2)
        DateToLabel = Label(formCanvas, text = "To:", bg = "#add8e6")
        DateToEntry = Entry(formCanvas, width = 2)
        previewInvoiceButton = ttk.Button(formCanvas, text = "Preview")
        TotalInvoicesLabel = Label(RightCanvas, text = "Total Invoices Generated: 0", bg = "#add8e6")
        TotalAmountDue = Label(RightCanvas, text = "Total Amount Due: 0", bg = "#add8e6")

        RightCanvasTitle.pack(side = TOP, pady = (5,0))

        CompanyLabel.grid(row = 0, column = 0, columnspan=2, padx = 2, pady = 2)
        CompanyComboBox.grid(row = 0, column = 2, columnspan=2, padx = 2, sticky = "ew")
        DateFromLabel.grid(row = 1, column = 0, padx = 2, pady = 2)
        DateFromEntry.grid(row = 1, column = 1, padx = 2, pady = 2)
        DateToLabel.grid(row = 1, column = 2, padx = 2, pady = 2)
        DateToEntry.grid(row = 1, column = 3, padx = 2, pady = 2, sticky = "ew")
        previewInvoiceButton.grid(row = 2, column = 0, columnspan=2, pady = 5, padx = 5)

        TotalAmountDue.pack(side = BOTTOM, pady = (0,10))
        TotalInvoicesLabel.pack(side = BOTTOM)
        ttk.Separator(RightCanvas, orient = "horizontal").pack(side = BOTTOM, fill = "x", pady = 10, padx = 15)
        formCanvas.pack(side = BOTTOM, padx = 5)
        ttk.Separator(RightCanvas, orient = "horizontal").pack(side = BOTTOM, fill = "x", pady = 5, padx = 15)


        # WIDGET PLACEMENTS
        treeView.pack(side = BOTTOM)
        LeftCanvas.pack(side = LEFT, fill = "both", padx = 2, pady = 2)
        MiddleCanvas.pack(side = LEFT, fill = "both", padx = 2, pady = 2)
        RightCanvas.pack(side = LEFT, fill = "both", padx = 2, pady = 2)


    def SalesInformationPane(self):

        infoFrame = Canvas(self.roundedRectangleCanvas, highlightthickness=0, bg = "#add8e6")

        PerformanceCanvas = Canvas(infoFrame,bg = "#add8e6", highlightthickness = 0, width = 375)

        PerformanceTitle = Label(PerformanceCanvas, text = "Performance", bg = "#add8e6", font = ("helvetica",15, "italic"))
        PerformanceNotebook = ttk.Notebook(PerformanceCanvas, padding = 3)
        self.dailyFrame = Frame(PerformanceNotebook, bg = "#add8e6")
        self.monthlyFrame = Frame(PerformanceNotebook, bg = "#add8e6")
        self.annualFrame = Frame(PerformanceNotebook, bg = "#add8e6")
        Label(self.dailyFrame, text = "daily").pack()
        Label(self.monthlyFrame, text = "monthly").pack()
        Label(self.annualFrame, text = "annual").pack()

        PerformanceNotebook.add(self.dailyFrame, text = "Daily")
        PerformanceNotebook.add(self.monthlyFrame, text = "Monthly")
        PerformanceNotebook.add(self.annualFrame, text = "Annual")

        PerformanceCanvas.pack(padx = 5, pady= (5,10))
        PerformanceTitle.pack(padx = 5, pady = 5)
        PerformanceNotebook.pack(fill = "x")
        self.dailyFrame.pack(fill = "both", expand = True)
        self.monthlyFrame.pack(fill = "both", expand = True)
        self.annualFrame.pack(fill = "both", expand = True)

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

        button_canvas = Canvas(infoFrame)

        # Button Definitions
        self.ShowRecordsButton = ttk.Button(button_canvas, text = "Show Sales", command = lambda: self.DisplayAllRecords("Sales"))
        self.SelectRecordButton= ttk.Button(button_canvas, text = "Select", state = DISABLED, command = self.SelectClient)
        self.DeleteClientButton = ttk.Button(button_canvas, text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.EditClientButton = ttk.Button(button_canvas, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)

        # Button Placements
        self.ShowRecordsButton.grid(row=0,column=0)
        self.SelectRecordButton.grid(row=0,column=1)
        self.DeleteClientButton.grid(row=0,column=2)
        self.EditClientButton.grid(row=0,column=3)

        button_canvas.pack(side=BOTTOM, pady = 10, padx = 5)

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
        button_canvas = Canvas(infoFrame)

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
        self.ShowRecordsButton = ttk.Button(button_canvas, text = "Show Inventory", command = lambda: self.DisplayAllRecords("Inventory"))
        self.SelectRecordButton= ttk.Button(button_canvas, text = "Select", state = DISABLED, command = self.SelectClient)
        self.DeleteClientButton = ttk.Button(button_canvas, text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.EditClientButton = ttk.Button(button_canvas, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)

        # Button Placements
        self.ShowRecordsButton.grid(row=0,column=0)
        self.SelectRecordButton.grid(row=0,column=1)
        self.DeleteClientButton.grid(row=0,column=2)
        self.EditClientButton.grid(row=0,column=3)

        # Canvas Placements
        PopularItemsCanvas.pack(padx = 5, pady= (5,10))
        FilterCanvas.pack(padx= 8, pady= 8)
        button_canvas.pack(pady = 10, padx = 5)

        return infoFrame

    # Populate Tableview for each tab
    def DisplayAllRecords(self, table):
        
        if self.ShowRecordsButton["text"] == "Return":
            # Change button back to saying "Show"
            self.ShowRecordsButton.config(text = "Show Clients")
            # Clear Treeview
            self.tree.delete(*self.tree.get_children())
            self.tree.delete(item for item in self.tree.get_children())
            # Clear Customer Selected Info Pane
            self.DefaultCustomerSelectedInfo()
            # Clear Customer Info Entry Widget
            self.Firstname.delete(0, END)
            self.Lastname.delete(0, END)
            self.CompanyEntry.delete(0, END)
            self.ContactNum.delete(0, END)
            self.Email.delete(0, END)
            self.Address.delete(0, END)
            self.Postcode.delete(0, END)
            # Clear Record from database
        

        self.ShowRecordsButton.config(text = "Return", state = ACTIVE)

        CONN.execute(f"SELECT * FROM {table}")
        Result = CONN.fetchall()
        for Record in Result:
            self.tree.insert('', 'end', values = Record[1:])
        self.AmountOfClients.config(text="Amount of Clients: "+ str(len(self.tree.get_children())))

    def DeleteClient(self):
        myExit = messagebox.askyesno(title="Quit",message="Are you sure you want to delete\nthis client?")
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

    def SelectClient(self, event):

        
        self.DeleteClientButton.config(state = ACTIVE)
        self.EditClientButton.config(state = ACTIVE)
        

        items = self.tree.item(self.tree.selection())
        
        self.CFirstname.config(text = "Firstname: "+items["values"][0][:20])
        self.CLastname.config(text = "Lastname: "+items["values"][1][:20])
        self.CCompany.config(text = "Company: "+items["values"][2][:20])
        self.CTelephone.config(text = "Telephone: "+str(items["values"][3]))
        self.CEmail.config(text = "Email: "+items["values"][4][:20])
        self.CAddress.config(text = "Address: "+items["values"][5][:20])
        self.CPostcode.config(text = "Postcode: "+items["values"][6][:20])

    def PopulateEditForm(self):

        self.Submit.config(text = "Modify" , state= ACTIVE)
        self.EditClientButton.config(state= DISABLED)
        self.DeleteClientButton.config(state = DISABLED)

        items = self.tree.item(self.tree.selection())
        # self.tree.delete(*self.self.tree.get_children())

        self.Firstname.insert(0,items["values"][0])
        self.Lastname.insert(0,items["values"][1])
        self.CompanyEntry.insert(0,items["values"][2])
        self.ContactNum.insert(0,items["values"][3])
        self.Email.insert(0,items["values"][4])
        self.Address.insert(0,items["values"][5])
        self.Postcode.insert(0,items["values"][6])

    def AddClientForm(self,master):

        AddClient = self.RoundedCorneredCanvas(master, 300, 240, 15, "#add8e6")

        # Label Definitions/Placements
        Label(AddClient, text="First Name",bg = "#add8e6" ).grid(row=0, pady=(5,0))
        Label(AddClient, text="Last Name",bg = "#add8e6" ).grid(row=1)
        Label(AddClient, text="Company",bg = "#add8e6" ).grid(row=2)
        Label(AddClient, text="Contact Number",bg = "#add8e6" ).grid(row=3, padx = (5,0))
        Label(AddClient, text="Email",bg = "#add8e6" ).grid(row=4)
        Label(AddClient, text="Address",bg = "#add8e6" ).grid(row=5)
        Label(AddClient, text="Postcode",bg = "#add8e6" ).grid(row=6)
        self.Submit = ttk.Button(AddClient, state = DISABLED, text="Add Client", command =
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
        self.Firstname.grid(row=0, column=1, pady = (2,0), padx = (0,5))
        self.Lastname.grid(row=1, column=1, pady = (1,0), padx = (0,5))
        self.CompanyEntry.grid(row=2, column=1,  pady = (1,0), padx = (0,5))
        self.ContactNum.grid(row=3, column=1, pady = (1,0), padx = (0,5))
        self.Email.grid(row=4, column=1, pady = (1,0), padx = (0,5))
        self.Address.grid(row=5, column=1, pady = (1,0), padx = (0,5))
        self.Postcode.grid(row=6, column=1,  pady = (1,0), padx = (0,5))
        self.StateLabel.grid(column=1,row=7,  pady = (1,0), padx = (0,5))

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

    def TreeView(self, master, fields, width, height = 10, scrollpresent = True):

        self.treeFrame = Frame(master)
        self.tree = ttk.Treeview(self.treeFrame, columns = fields, show = "headings", height = height)
        self.tree.bind("<Double-1>", self.SelectClient)
        if scrollpresent:
            self.scrollBar = ttk.Scrollbar(self.treeFrame, orient='vertical', command=self.tree.yview)
            self.scrollBar.grid(row = 0, column = 1 , sticky='ns', in_= self.treeFrame)
            self.tree.configure(yscrollcommand=self.scrollBar.set)

        self.tree.grid(row = 0, column=0, in_= self.treeFrame)

        HeaderLength = 0
        for x in fields:
            HeaderLength += len(x)

        for field in fields:
            # Set each column width
            self.tree.column(field, width = int(len(field)/HeaderLength*(width-50)))

            # Set each column heading
            self.tree.heading(field, text = field.title(), anchor = "n", command = lambda c = field: self.SortRecords(c,1,fields,self.tree))

        return self.treeFrame

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
        self.tree.heading(col, command=lambda c=field:self.SortRecords
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

    def toggleState(self):
        if self.CheckValue:
            self.Company['state'] = ACTIVE
            self.CheckValue.set(True)
        else:
            self.Company['state'] = DISABLED
            self.CheckValue.set(False)

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

        self.CheckValue = BooleanVar()
        self.CheckValue.set(False)

        self.CheckButton = Checkbutton(AddSaleCanvas, text = "Client?", bg="#add8e6", var = self.CheckValue, command = self.toggleState)
        self.Item = ttk.Combobox(AddSaleCanvas, state = DISABLED, width = 20)
        self.Name = ttk.Combobox(AddSaleCanvas, state = DISABLED, width = 20)

        db = sqlite3.connect("Customers.db")
        Link = db.cursor()

        self.Company = ttk.Combobox(AddSaleCanvas,state=DISABLED, width = 20)
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

    def RoundedCorneredCanvas(self, Window, x2, y2, feather, color = "#add8e6", x1 = 1, y1 = 1):

        x2 -= x1
        y2 -= y1
        points = []
        res = 10

        # top side
        points += [x1 + feather, y1,
                x2 - feather, y1]
        # top right corner
        for i in range(res):
            points += [x2 - feather + np.sin(i/res*2) * feather,
                    y1 + feather - np.cos(i/res*2) * feather]
        # right side
        points += [x2, y1 + feather,
                x2, y2 - feather]
        # bottom right corner
        for i in range(res):
            points += [x2 - feather + np.cos(i/res*2) * feather,
                    y2 - feather + np.sin(i/res*2) * feather]
        # bottom side
        points += [x2 - feather, y2,
                x1 + feather, y2]
        # bottom left corner
        for i in range(res):
            points += [x1 + feather - np.sin(i/res*2) * feather,
                    y2 - feather + np.cos(i/res*2) * feather]
        # left side
        points += [x1, y2 - feather,
                x1, y1 + feather]

        # top left corner
        for i in range(res):
            points += [x1 + feather - np.cos(i/res*2) * feather,
                    y1 + feather - np.sin(i/res*2) * feather]

        canvas = Canvas(Window, highlightthickness = 1)
        canvas.create_polygon(points, fill = color)

        return canvas

if __name__ == "__main__":
    root = ThemedTk(theme = "arc")
    MainWindow = Parent(root)
    root.mainloop()

##http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
##http://stackoverflow.com/questions/20588417/how-to-change-font-and-size-of-buttons-and-frame-in-tkinter-using-python
