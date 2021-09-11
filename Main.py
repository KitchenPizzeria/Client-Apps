#-*- coding: utf-8 -*-
from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re
from ttkthemes import ThemedTk
import numpy as np

TITLE_FONT = ("Georgia",20)
BACKGROUND_COLOUR = "#cdeefd"

DB = sqlite3.connect("Customers.db")
CONN = DB.cursor()

class Parent():
    """
    This is a module which generates the program for the Tkinter GUI Application
    """
    def __init__(self,master):
        # Define Tk Window
        self.master = master

        # Define windows properties
        self.window_height = 550
        self.window_width = 720
        master.resizable(0,0)
        master.geometry('%dx%d' % (self.window_width, self.window_height))
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
        self.current_notebook_tab = 0
        self.notebook.bind("<<NotebookTabChanged>>", self.loadOnClick)

        self.customers_frame = Frame(self.notebook, bg = BACKGROUND_COLOUR)
        self.sales_frame = Frame(self.notebook, bg = BACKGROUND_COLOUR)
        self.inventory_frame = Frame(self.notebook, bg = BACKGROUND_COLOUR)
        self.invoices_frame = Frame(self.notebook, bg = BACKGROUND_COLOUR)

        # Notebook/Frame Placement Rules
        self.notebook.pack()
        self.customers_frame.pack(fill = 'both', expand= True)
        self.sales_frame.pack(fill = 'both', expand= True)
        self.invoices_frame.pack(fill = 'both', expand= True)
        self.inventory_frame.pack(fill = 'both', expand= True)

        # Add frames to the Notebook
        self.notebook.add(self.customers_frame, text = "Customers", sticky = NE)
        self.notebook.add(self.sales_frame, text = "Sales")
        self.notebook.add(self.inventory_frame, text = "Inventory")
        self.notebook.add(self.invoices_frame, text = "Invoices")

    def loadOnClick(self,event):

        tabList = [
            self.customers_frame,
            self.sales_frame,
            self.inventory_frame,
            self.invoices_frame
        ]

        # clear all widgets from starting tab
        startTab = tabList[self.current_notebook_tab]

        for x in startTab.winfo_children():
            x.destroy()

        # then update current tab and initialise all new widgets in destination tab

        self.current_notebook_tab = self.notebook.index(self.notebook.select())

        if self.current_notebook_tab == 0:
            self.PopulateCustomersFrame(self.customers_frame)
        if self.current_notebook_tab == 1:
            self.PopulateSalesFrame(self.sales_frame)
        if self.current_notebook_tab == 2:
            self.PopulateInventoryFrame(self.inventory_frame)
        if self.current_notebook_tab == 3:
            self.PopulateInvoicesFrame(self.invoices_frame)

    def PopulateCustomersFrame(self, Window):

        width = 380
        height = 220

        result = DB.execute("SELECT * FROM Customers")
        fields = [description[0] for description in result.description]

        # Canvas Definitions
        background_canvas = self.RoundedCorneredCanvas(self.customers_frame, width, height, 15)
        info_canvas = Frame(background_canvas, bg = "#add8e6")
        button_canvas = Frame(background_canvas, bg = "#add8e6")
        #PictureCanvas = Canvas(rootCanvas)

        # Canvas Placements
        button_canvas.pack(side = BOTTOM, pady = 8, padx = 2)
        info_canvas.pack(anchor = NE, padx = 5, pady= 5)
        #PictureCanvas.pack(side = LEFT)

        # Label Definitions
        self.firstname = Label(info_canvas, text = "Firstname: None",bg = "#add8e6")
        self.lastname = Label(info_canvas, text = "Lastname: None",bg = "#add8e6")
        self.company = Label(info_canvas, text = "Company: None",bg = "#add8e6")
        self.telephone = Label(info_canvas, text = "Telephone: None",bg = "#add8e6")
        self.email = Label(info_canvas, text = "Email: None",bg = "#add8e6")
        self.address = Label(info_canvas, text = "Address: None",bg = "#add8e6")
        self.postcode = Label(info_canvas, text = "Postcode: None",bg = "#add8e6")
        self.amount_of_clients = Label(info_canvas, text = "Amount of Clients: 0  ",bg = "#add8e6")

        # Label Placements
        self.firstname.pack(side = TOP)
        self.lastname.pack(side = TOP)
        self.company.pack(side = TOP)
        self.telephone.pack(side = TOP)
        self.email.pack(side = TOP)
        self.address.pack(side = TOP)
        self.postcode.pack(side = TOP)
        self.amount_of_clients.pack(side = TOP, padx = 5)

        # Button Definitions
        self.show_records = ttk.Button(button_canvas, width = 10,text = "Show Clients",command = lambda: self.DisplayAllRecords("Customers"))
        self.delete_records = ttk.Button(button_canvas,width = 8,text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.edit_clients = ttk.Button(button_canvas, width = 8, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)

        # Button Placements
        self.show_records.grid(row=0,column=0, padx = 3)
        self.delete_records.grid(row=0,column=1, padx = 3)
        self.edit_clients.grid(row=0,column=2, padx = 3)

        self.customers_treeview = self.TreeView(Window, fields, self.window_width)
        self.customers_treeview.pack(side = BOTTOM)

        background_canvas.place(x = 5, y = 5 , width = width, height = height)
        self.AddClientForm(Window).pack(side = RIGHT, pady= 2, padx = (0,10))

    def AddClientForm(self,master):

        self.add_client = self.RoundedCorneredCanvas(master, 290, 235, 15, "#add8e6")

        # Label Definitions/Placements
        Label(self.add_client, text="First Name",bg = "#add8e6" ).grid(row=0, pady=(5,0))
        Label(self.add_client, text="Last Name",bg = "#add8e6" ).grid(row=1)
        Label(self.add_client, text="Company",bg = "#add8e6" ).grid(row=2)
        Label(self.add_client, text="Contact Number",bg = "#add8e6" ).grid(row=3, padx = (5,0))
        Label(self.add_client, text="Email",bg = "#add8e6" ).grid(row=4)
        Label(self.add_client, text="Address",bg = "#add8e6" ).grid(row=5)
        Label(self.add_client, text="Postcode",bg = "#add8e6" ).grid(row=6)
        self.submit = ttk.Button(self.add_client, text = "Add Client", command = self.InputMask)
        self.submit.grid(row=7,pady=5, padx = (5,0))

        # Entry Definitions
        self.firstname_entry = ttk.Entry(self.add_client, width = 17)
        self.lastname_entry = ttk.Entry(self.add_client, width = 17)
        self.company_entry = ttk.Entry(self.add_client, width = 17)
        self.contact_num_entry = ttk.Entry(self.add_client, width = 17)
        self.email_entry = ttk.Entry(self.add_client, width = 17)
        self.address_entry = ttk.Entry(self.add_client, width = 17)
        self.postcode_entry = ttk.Entry(self.add_client, width = 17)
        self.StateLabel = Label(self.add_client, bg="#add8e6")

        # Entry Placement
        self.firstname_entry.grid(row=0, column=1, sticky = W, pady = (5,0), padx = (0,5))
        self.lastname_entry.grid(row=1, column=1, pady = (3,0), padx = (0,5))
        self.company_entry.grid(row=2, column=1,  pady = (3,0), padx = (0,5))
        self.contact_num_entry.grid(row=3, column=1, pady = (3,0), padx = (0,5))
        self.email_entry.grid(row=4, column=1, pady = (3,0), padx = (0,5))
        self.address_entry.grid(row=5, column=1, pady = (3,0), padx = (0,5))
        self.postcode_entry.grid(row=6, column=1,  pady = (3,0), padx = (0,5))
        self.StateLabel.grid(column=1,row=7,  pady = (3,0), padx = (0,5))

        return self.add_client

    def ResetCustomerSelectedInfo(self):

        self.firstname.config(text = "Firstname: None")
        self.lastname.config(text = "Lastname: None")
        self.company.config(text = "Company: None")
        self.telephone .config(text = "Telephone: None")
        self.email .config(text = "Email: None")
        self.address.config(text = "Address: None")
        self.postcode.config(text = "Postcode: None")
        self.amount_of_clients.config(text = "Amount of Clients: 0  ")

    def PopulateSalesFrame(self, Window):

        c = DB.execute("SELECT * FROM Sales")
        fields = [description[0] for description in c.description]

        self.TreeView(Window, fields[1:], self.window_width).pack(side = BOTTOM, pady = (20,0))
        
        self.height = 230
        self.width = 370

        self.add_sale_canvas = self.RoundedCorneredCanvas(self.sales_frame,330,220,20)
        self.AddSalesForm()
        
        self.info_pane = self.RoundedCorneredCanvas(self.sales_frame, self.width, self.height, 20)
        self.SalesInformationPane()

        self.info_pane.place(x = 5, y = 5, height = self.height, width = self.width)
        self.add_sale_canvas.place(x = 380, y = 5, height = self.height, width = 400)

    def PopulateInventoryFrame(self, Window):

        c = DB.execute("SELECT * FROM Inventory")
        fields = [description[0] for description in c.description]

        popular_items_canvas = self.RoundedCorneredCanvas(self.inventory_frame, 370, 230, 15, "#add8e6")

        # Popular Items Canvas
        # Definitions
        PopularItemsTitle = Label(popular_items_canvas, text = "Popular Items", bg = "#add8e6" , font = ("Helvetica", 15, "bold"))

        table_frame = Frame(popular_items_canvas, bg = "#add8e6")
        ebay_low_item = self.TreeView(table_frame, ["Item", "Quantity"], 175, height = 2.5, scrollpresent=False)
        shop_low_item = self.TreeView(table_frame, ["Item", "Quantity"], 175, height = 2.5, scrollpresent=False)

        button_frame = Frame(popular_items_canvas, bg = "#add8e6" )
        ShowItemsButton = ttk.Button(button_frame,width = 8,text = "Show",command = lambda: self.DisplayAllRecords("Customers"))
        SelectItemButton= ttk.Button(button_frame,width = 8, text = "Select", state = DISABLED, command = self.SelectClient)
        DeleteItemButton = ttk.Button(button_frame,width = 8, text = "Delete", state = DISABLED, command = self.DeleteClient)
        PopularItemsTitle.pack(side = TOP, fill = "x", padx = 6, pady = (5,0))

        table_frame.pack(side = TOP)
        Label(table_frame, text = "Ebay Low Items", bg = "#add8e6").grid(row = 0, column = 0)
        Label(table_frame, text = "Store Low Items", bg = "#add8e6").grid(row = 0, column = 1)
        shop_low_item.grid(row = 1, column = 1, padx = 5)
        ebay_low_item.grid(row = 1, column = 0, padx = 5)
        ttk.Separator(popular_items_canvas, orient = "horizontal").pack(pady = 2)
        button_frame.pack(side = BOTTOM, padx = 5, pady = (0,5))
        ShowItemsButton.grid(row=0,column=0, padx = 3)
        SelectItemButton.grid(row=0,column=1, padx = 3)
        DeleteItemButton.grid(row=0,column=2, padx = 3)

        # Write Code to populate the low items tables

        self.company_list = ["Other"]
        result= DB.execute("SELECT Category FROM Inventory ")
        for x in result:
            if max(x) != "":
                self.company_list.append(max(x))
        self.company_list = sorted(list(set(self.company_list))) 



        # ADD ITEMS CANVAS
        AddItemCanvas = self.RoundedCorneredCanvas(self.inventory_frame, 201, 215, 15, "#add8e6")
        Label(AddItemCanvas, text = "Add Item", font = "Helvetica 15 bold", bg = "#add8e6").grid(row = 0, columnspan=4, pady = 3)
        Label(AddItemCanvas, text = "Category", bg = "#add8e6").grid(row = 1, column = 0, columnspan=2, pady = (10,5))
        self.combobox = ttk.Combobox(AddItemCanvas, values = self.company_list,width = 8)
        self.combobox.grid(row = 1, column = 2, columnspan=2)
        self.combobox.bind("<<ComboboxSelected>>", self.CategoryOptionSelected)


        self.other_label = Label(AddItemCanvas, text = "Other: ", state = DISABLED, bg = "#add8e6")
        self.other_label.grid(row = 2, column = 0, columnspan=2, pady = 5)
        self.other_entry = ttk.Entry(AddItemCanvas, width = 8, state = DISABLED)
        self.other_entry.grid(row = 2, column = 2, columnspan=2)
        self.description_label = Label(AddItemCanvas, text = "Description: ", bg = "#add8e6", state=DISABLED)
        self.description_label.grid(row = 3, column = 0, columnspan=2, padx = 5, pady = 5)
        self.description_entry = ttk.Entry(AddItemCanvas, state = DISABLED, width = 8)
        self.description_entry.grid(row = 3, column = 2, columnspan=2)
        self.unitprice_label = Label(AddItemCanvas, text = "Unit Price: ", bg = "#add8e6", state=DISABLED)
        self.unitprice_label.grid(row = 4, column = 0, columnspan=2, pady = 5)
        self.unitprice_entry = ttk.Entry(AddItemCanvas, state = DISABLED,width = 8)
        self.unitprice_entry.grid(row = 4, column= 2, columnspan = 2)
        
        self.add_item_button = ttk.Button(AddItemCanvas, text = "Add", width = 5)
        self.add_item_button.grid(row = 5, padx = 5)
        #Label(AddItemCanvas, text = "error", foreground= "red", bg = "#add8e6").grid(row = 4, column = 3)

        self.TreeView(Window, fields[1:], self.window_width).pack(side = BOTTOM)
        popular_items_canvas.place(x = 10, y = 2, width = 371, height = 230)
        AddItemCanvas.place(x = 453, y = 10, width = 201, height = 216)
    
    def CategoryOptionSelected(self, event):

        if self.combobox.get() == "Other":
            self.other_label.config(state= ACTIVE)
            self.other_entry.config(state= ACTIVE)
        else:
            self.other_label.config(state= DISABLED)
            self.other_entry.config(state= DISABLED)
        
        self.unitprice_label.config(state = ACTIVE)
        self.unitprice_entry.config(state = ACTIVE)
        self.description_entry.config(state = ACTIVE)
        self.description_label.config(state = ACTIVE)

    def PopulateInvoicesFrame(self, Window):

        c = DB.execute("SELECT * FROM Invoices")
        fields = [description[0] for description in c.description]

        toBePaidWidth = 235
        toBePaidHeight = 230

        # WIDGET DEFINITIONS
        treeView = self.TreeView(Window, fields[1:], self.window_width)
        LeftCanvas = self.RoundedCorneredCanvas(Window, toBePaidWidth, toBePaidHeight, 15, "#add8e6" )
        MiddleCanvas = self.RoundedCorneredCanvas(Window, 225, 230, 15, "#add8e6" )
        RightCanvas = self.RoundedCorneredCanvas(Window, toBePaidWidth, toBePaidHeight, 15, "#add8e6" )

        # LEFT CANVAS CONTENT
        # Definitions
        LeftCanvasTitle = Label(LeftCanvas, text = "To Be Paid", bg = "#add8e6" , font = ("Helvetica", 15, "bold"))
        treeViewFrame = Frame(LeftCanvas)
        toBePaidTreeView = self.TreeView(treeViewFrame, ["Date", "Company","Paid"],toBePaidWidth-20,height=2.5 )
        AmountDueLabel = Label(LeftCanvas, text = "Amount Due: 0", bg = "#add8e6")

        # Placements
        LeftCanvasTitle.pack(side = TOP, pady = (10,10), padx = 2)
        toBePaidTreeView.pack()
        treeViewFrame.pack(side = TOP, pady = (0,10), padx = 13)
        AmountDueLabel.pack(side = TOP, pady = 5, padx = 2)

        # MIDDLE CANVAS CONTENT
        # Definitions
        Label(MiddleCanvas, text = "eBay To Be Paid", bg = "#add8e6", font = ("Helvetica", 15, "bold")).pack(side = TOP, pady = (3,0))

        self.ebay_payments_due = self.TreeView(MiddleCanvas,["Item Sold", "Date", "Due"], 185, 1, scrollpresent=True)
        self.ebay_payments_due.pack(side = TOP, pady = 3)

        filterCanvas = Frame(MiddleCanvas, bg = "#add8e6")
        CompanyLabel = Label(filterCanvas, text = "Company:", bg = "#add8e6")
        CompanyComboBox = ttk.Combobox(filterCanvas, width = 9)
        DateFromLabel = Label(filterCanvas, text = "Date:", bg = "#add8e6")
        DateFromEntry = Entry(filterCanvas, width = 2)
        DateToLabel = Label(filterCanvas, text = "To:", bg = "#add8e6")
        DateToEntry = Entry(filterCanvas, width = 2)
        showInvoicesButton = ttk.Button(filterCanvas, text = "Show", width = 8)
        clearInvoicesButton = ttk.Button(filterCanvas, text = "Clear", width = 8)

        # Placements

        #table_frame.pack(side = TOP, fill = "both", expand = True, padx = 5, pady = 5)
        ttk.Separator(MiddleCanvas, orient= "horizontal").pack()

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
        formCanvas = Frame(RightCanvas, bg = "#add8e6", width = 30)
        FilterTitle = Label(formCanvas, text = "Filter", bg = "#add8e6")
        CompanyLabel = Label(formCanvas, text = "Company:", bg = "#add8e6")
        CompanyComboBox = ttk.Combobox(formCanvas, width = 5)
        DateFromLabel = Label(formCanvas, text = "Date:", bg = "#add8e6")
        DateFromEntry = Entry(formCanvas, width = 5)
        DateToLabel = Label(formCanvas, text = "To:", bg = "#add8e6")
        DateToEntry = Entry(formCanvas, width = 6)
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
        RightCanvas.pack(side = RIGHT, fill = "both", pady = 2)
        MiddleCanvas.pack(side = LEFT, fill = "both", pady = 2, padx = (4,0))

    def SalesInformationPane(self):

        PerformanceCanvas = Canvas(self.info_pane, bg = "#add8e6", highlightthickness = 0, width = 375)

        PerformanceTitle = Label(PerformanceCanvas, text = "Performance", bg = "#add8e6", font = "helvetica 17 italic")
        PerformanceNotebook = ttk.Notebook(PerformanceCanvas, padding = 3)
        self.daily_frame = Frame(PerformanceNotebook, bg = "#add8e6")
        self.monthly_frame = Frame(PerformanceNotebook, bg = "#add8e6")
        self.annual_frame = Frame(PerformanceNotebook, bg = "#add8e6")
        Label(self.daily_frame, bg = "#add8e6", text = "daily").pack(side = LEFT)
        Label(self.monthly_frame, bg = "#add8e6", text = "monthly").pack()
        Label(self.annual_frame, bg = "#add8e6", text = "annual").pack(side = RIGHT)

        PerformanceNotebook.add(self.daily_frame, text = "Daily")
        PerformanceNotebook.add(self.monthly_frame, text = "Monthly")
        PerformanceNotebook.add(self.annual_frame, text = "Annual")

        PerformanceCanvas.pack(padx = 5, pady= (5,10))
        PerformanceTitle.pack(padx = 5, pady = 5)
        PerformanceNotebook.pack(fill = "x")
        self.daily_frame.pack(side = LEFT,fill = "both", expand = True)
        self.monthly_frame.pack(side = LEFT,fill = "both", expand = True)
        self.annual_frame.pack(side = LEFT,fill = "both", expand = True)

        FilterCanvas = Canvas(self.info_pane,
            bg = "#add8e6",
            highlightthickness = 1,
            width = 375)

        FilterTitle = Label(FilterCanvas, text = "Filter", bg = "#add8e6", font = "helvetica 17 italic")
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

        FilterCanvas.pack(padx= 8)

        button_canvas = Canvas(self.info_pane, bg="#add8e6")

        # Button Definitions
        self.show_records = ttk.Button(button_canvas, text = "Show Sales", command = lambda: self.DisplayAllRecords("Sales"))
        self.delete_records = ttk.Button(button_canvas, text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.edit_clients = ttk.Button(button_canvas, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)

        # Button Placements
        self.show_records.grid(row=0,column=0)
        self.delete_records.grid(row=0,column=1)
        self.edit_clients.grid(row=0,column=2)

        button_canvas.pack(side=BOTTOM, pady = (0,8), padx = 5)

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
        self.show_records = ttk.Button(button_canvas, text = "Show Inventory", command = lambda: self.DisplayAllRecords("Inventory"))
        self.delete_records = ttk.Button(button_canvas, text = "Delete", state = DISABLED, command = self.DeleteClient)
        self.edit_clients = ttk.Button(button_canvas, text = "Edit info", state = DISABLED, command = self.PopulateEditForm)

        # Button Placements
        self.show_records.grid(row=0,column=0)
        self.delete_records.grid(row=0,column=1)
        self.edit_clients.grid(row=0,column=2)

        # Canvas Placements
        PopularItemsCanvas.pack(padx = 5, pady= (5,10))
        FilterCanvas.pack(padx= 8, pady= 8)
        button_canvas.pack(pady = 10, padx = 5)

        return infoFrame

    def DisplayAllRecords(self, table):

        if self.show_records["text"] == "Return":
            # Change button back to saying "Show"
            self.show_records.config(text = "Show Clients")
            # Clear Treeview
            self.tree.delete(*self.tree.get_children())
            self.tree.delete(item for item in self.tree.get_children())
            # Clear Customer Selected Info Pane
            self.ResetCustomerSelectedInfo()
            # Clear Customer Info Entry Widget
            self.firstname_entry.delete(0, END)
            self.lastname_entry.delete(0, END)
            self.company_entry.delete(0, END)
            self.contact_num_entry.delete(0, END)
            self.email_entry.delete(0, END)
            self.address_entry.delete(0, END)
            self.postcode_entry.delete(0, END)
            # Clear Record from database


        self.show_records.config(text = "Return", state = ACTIVE)

        CONN.execute("SELECT * FROM Customers")
        Result = CONN.fetchall()
        for Record in Result:
            self.tree.insert('', 'end', values = Record)
        self.amount_of_clients.config(text="Amount of Clients: "+ str(len(self.tree.get_children())))

    def DeleteClient(self):
        self.ResetCustomerSelectedInfo()
        self.ClearTreeview()
        # myExit = messagebox.askyesno(title="Quit",message="Are you sure you want to delete\nthis client?")
        # if myExit > 0:
        #     try:
        #         items = self.self.tree.item(self.self.tree.selection())
        #         selectedItem = self.self.tree.selection()[0]
        #         self.self.tree.delete(selectedItem)

        #         db = sqlite3.connect("Customers.db")
        #         c = db.cursor()
        #         c.execute("SELECT* FROM Customers")
        #         Result = c.fetchall()
        #         for x in range(len(Result)):
        #             if Result[x][1] == items["values"][0] and Result[x][2] == items["values"][1] and Result[x][3] == items["values"][2]:
        #                 CustID = Result[x][0]

        #         db = sqlite3.connect("Customers.db")
        #         c = db.cursor()
        #         query = "DELETE FROM Customers WHERE CustomerID = '%s';"%CustID
        #         c.execute(query)
        #         db.commit()
        #         db.close()

        #     except:
        #         selectedItem = "Deleted: None"
        #     self.amount_of_clients.config(text="Records: "+str(len(self.self.tree.get_children())))

    def SelectClient(self, event):

        self.delete_records.config(state = ACTIVE)
        self.edit_clients.config(state = ACTIVE)

        items = self.tree.item(self.tree.selection())

        self.firstname.config(text = "Firstname: "+items["values"][1][:20])
        self.lastname.config(text = "Lastname: "+items["values"][2][:20])
        self.company.config(text = "Company: "+items["values"][3][:20])
        self.telephone.config(text = "Telephone: "+str(items["values"][4]))
        self.email.config(text = "Email: "+items["values"][5][:20])
        self.address.config(text = "Address: "+items["values"][6][:20])
        self.postcode.config(text = "Postcode: "+items["values"][7][:20])

    def ClearTreeview(self):

        self.tree.delete(*self.tree.get_children())
    
    def PopulateEditForm(self):

        self.submit.config(text = "Modify" , state= ACTIVE)
        self.edit_clients.config(state= DISABLED)
        self.delete_records.config(state = DISABLED)

        items = self.tree.item(self.tree.selection())
        # self.tree.delete(*self.self.tree.get_children())

        self.firstname_entry.insert(0,items["values"][1])
        self.lastname_entry.insert(0,items["values"][2])
        self.company_entry.insert(0,items["values"][3])
        self.contact_num_entry.insert(0,items["values"][4])
        self.email_entry.insert(0,items["values"][5])
        self.address_entry.insert(0,items["values"][6])
        self.postcode_entry.insert(0,items["values"][7])
        
        self.ResetCustomerSelectedInfo()
        self.ClearTreeview()

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

    # def CheckandConfirm(Parent,QuickAddFrame):
    #     db = sqlite3.connect("Customers.db")
    #     c = db.cursor()
    #     c.execute("SELECT * FROM Inventory")
    #     result = c.fetchall()
    #     for Record in result:
    #         if Record[2] == Parent.Item.get():
    #             fetchPrice = float(Record[3])

    #     try:
    #         fetchQuan = float(Parent.Quantity.get())
    #         TotalPriceMoney = Decimal(str(fetchQuan*fetchPrice)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    #         NetMoney = Decimal(str(fetchQuan*fetchPrice*0.8)).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    #         VatMoney = TotalPriceMoney - NetMoney
    #         if fetchQuan > 0 and fetchPrice > 0:

    #             Parent.UnitPrice.config(text = "£ " + str(fetchPrice))
    #             Parent.Gross.config(text ="£ "+ str(TotalPriceMoney))
    #             Parent.NetTotal.config(text = "£ "+ str(NetMoney))
    #             Parent.Vat.config(text = "£ "+ str(VatMoney))

    #             Parent.Company.config(state = DISABLED)
    #             Parent.Name.config(state = DISABLED)
    #             Parent.Category.config(state = DISABLED)
    #             Parent.Item.config(state = DISABLED)
    #             Parent.Quantity.config(state = DISABLED)

    #             Parent.Confirm = ttk.Button(QuickAddFrame,text = "Confirm Sale",command =
    #                                         lambda:Parent.AddRecordToSalesDatabase(QuickAddFrame))
    #             Parent.Confirm.grid(row=7,column=1)
    #             Parent.AddSale.config(text = "Edit",command = lambda:Parent.AddNew(QuickAddFrame))
    #         else:
    #             Parent.StateLabel.config(text="**Error**",fg="red")
    #     except:
    #         Parent.StateLabel.config(text="**Error**",fg="red")

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

    def InputMask(self):

        TelephoneRegEx = r"\d+[ ]{0,1}\d*$"
        NamesCompanyRegEx = r"[a-zA-Z]+"
        PostcodeRegEx = r"[a-zA-Z0-9]{2,4}[ ]{1}[0-9]{1}[a-zA-Z]{2}$"
        EmailRegEx = r"[a-zA-z0-9]+[@]{1}[a-zA-Z0-9.]+$"
        AddressRegEx = r"\d{1,3}[ ]{1}[a-zA-Z]+[ ]{1}[a-zA-Z]+"

        if re.match(TelephoneRegEx,self.contact_num_entry.get()):
            if re.match(EmailRegEx,self.email_entry.get()):
                if re.match(PostcodeRegEx,self.postcode_entry.get()):
                    if re.match(NamesCompanyRegEx,self.firstname_entry.get()):
                        if re.match(NamesCompanyRegEx,self.lastname_entry.get()):
                            if re.match(NamesCompanyRegEx,self.company_entry.get()):
                                if re.match(AddressRegEx,self.address_entry.get()):

                                    self.firstname_entry.config(state = DISABLED)
                                    self.lastname_entry.config(state = DISABLED)
                                    self.company_entry.config(state = DISABLED)
                                    self.email_entry.config(state = DISABLED)
                                    self.contact_num_entry.config(state = DISABLED)
                                    self.postcode_entry.config(state = DISABLED)
                                    self.address_entry.config(state = DISABLED)
                                    self.StateLabel.config(text="")

                                    self.confirm_button = ttk.Button(self.add_client,text = "Confirm",command = self.AddRecordToCustomerDatabase)
                                    self.confirm_button.grid(column = 1, row = 7)
                                    self.submit.config(text = "Edit", command = self.ResetEditForm)

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

    def ResetEditForm(self):
        self.firstname_entry.config(state = ACTIVE)
        self.lastname_entry.config(state = ACTIVE)
        self.email_entry.config(state = ACTIVE)
        self.postcode_entry.config(state = ACTIVE)
        self.company_entry.config(state = ACTIVE)
        self.contact_num_entry.config(state = ACTIVE)
        self.address_entry.config(state = ACTIVE)
        self.confirm_button.destroy()
        self.submit.config(text = "Modify", command = self.InputMask)

    def toggleState(self):
        if self.CheckValue:
            self.Company['state'] = ACTIVE
            self.CheckValue.set(True)
        else:
            self.Company['state'] = DISABLED
            self.CheckValue.set(False)

    def AddSalesForm(self):

        # Label Definitions
        Label(self.add_sale_canvas, font = "Helvetica 12",text="Company", bg="#add8e6").grid(row=1)
        Label(self.add_sale_canvas, font = "Helvetica 12",text="Client", bg="#add8e6").grid(row=2)
        Label(self.add_sale_canvas, font = "Helvetica 12",text="Category", bg="#add8e6").grid(row=3)
        Label(self.add_sale_canvas, font = "Helvetica 12",text="Item", bg="#add8e6").grid(row=4)
        Label(self.add_sale_canvas, font = "Helvetica 12",text = "Quantity", bg="#add8e6").grid(row=5)
        Label(self.add_sale_canvas, font = "Helvetica 12",text = "Unit Price £0.00", bg="#add8e6").grid(row=5, column = 2, sticky = W)
        Label(self.add_sale_canvas, font = "Helvetica 12",text = "Total", bg="#add8e6").grid(row = 6, column = 2)


        self.CheckValue = BooleanVar()
        self.CheckValue.set(False)

        self.CheckButton = Checkbutton(self.add_sale_canvas, font = "Helvetica 12",text = "Client?", bg="#add8e6", var = self.CheckValue, command = self.toggleState)
        self.Item = ttk.Combobox(self.add_sale_canvas, state = DISABLED, width = 20)
        self.Name = ttk.Combobox(self.add_sale_canvas, state = DISABLED, width = 20)

        db = sqlite3.connect("Customers.db")
        Link = db.cursor()

        self.Company = ttk.Combobox(self.add_sale_canvas,state=DISABLED, width = 20)
        Companies = db.execute("SELECT Company FROM Customers")
        CompanyValues = []
        for x in Companies:
            if max(x) != "":
                CompanyValues.append(max(x))
        CompanyValues = sorted(list(set(CompanyValues)))
        self.Company["values"] = CompanyValues

        self.Company.bind("<Configure>",Parent.CheckWidth(CompanyValues))
        self.Company.bind("<<ComboboxSelected>>",self.ActivateAndFillNameBox)

        self.Category = ttk.Combobox(self.add_sale_canvas,width = 20)
        Categories = db.execute("SELECT Category FROM Inventory")
        StockCat = []
        for x in Categories:
            if max(x) != "" or max(x)!="None":
                StockCat.append(max(x))
        StockCat = sorted(list(set(StockCat)))
        self.Category["values"] = StockCat

        self.Category.bind("<Configure>",Parent.CheckWidth(StockCat))
        self.Category.bind("<<ComboboxSelected>>",self.ActivateAndFillItemBox)

        self.Quantity = ttk.Entry(self.add_sale_canvas, width = 5)
        self.UnitPrice = Label(self.add_sale_canvas,bg="#add8e6")
        self.Total = Label(self.add_sale_canvas,text = "Total: ", bg="#add8e6")
        self.StateLabel = Label(self.add_sale_canvas,width = 10,bg="#add8e6")
        self.UniqueIDRepeat = True

        self.AddSale = ttk.Button(self.add_sale_canvas, text="Add Sale",command = lambda: self.CheckandConfirm(QuickAddFrame,self.UniqueIDRepeat))
        self.Confirm = ttk.Button(self.add_sale_canvas, state=DISABLED , text = "Confirm")

        self.CheckButton.grid(row = 0,column = 0,columnspan = 1, pady = (5,0), padx = 2)
        self.Company.grid(row = 1, column=1, columnspan = 2, pady = 2, padx = 2)
        self.Name.grid(row = 2,column=1,columnspan = 2, pady = 2, padx = 2)
        self.Category.grid(row = 3,column=1,columnspan = 2, pady = 2, padx = 2)
        self.Item.grid(row = 4,column=1,columnspan = 2, pady = 2, padx = 2)
        self.Quantity.grid(row = 5,column = 1,columnspan = 1, pady = 2, padx = 2)
        
        self.AddSale.grid(row = 6, column = 0, pady = 2, padx = (5,0))
        self.Confirm.grid(row = 6, column = 1, padx=(5,0))
        self.Total.grid(row = 6, column= 2 , pady = 2, padx = 2)
        #self.StateLabel.grid(row = 6, column=2, padx = 1, pady = 2)

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

    def ResetEntireScreen(self):
        # Reactivate Entry Boxes
        self.ResetEditForm()

        # Clear Entry Boxes
        self.firstname_entry.delete(0, END)
        self.lastname_entry.delete(0, END)
        self.company_entry.delete(0, END)
        self.contact_num_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.postcode_entry.delete(0, END)

        # Reset all the info labels to None
        self.ResetCustomerSelectedInfo()
        # Change display button to show
        self.show_records.config(text = "Show Clients")
        # Remove Client added Label
        self.StateLabel.grid_remove()

        # Clear TreeView
        self.ClearTreeview()

        

    def AddRecordToCustomerDatabase(self):
        
        # # Update Database With New Info
        db = sqlite3.connect("Customers.db")
        c = db.cursor()

        first_name = self.firstname_entry.get()
        sur_name = self.lastname_entry.get()
        company = self.company_entry.get()
        telephone = self.contact_num_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        postcode = self.postcode_entry.get()
        id = 11

        Update = "UPDATE Customers set Firstname='%s', Surname='%s', Company='%s', Telephone='%s', Email='%s', Address='%s', Postcode = '%s' where CustomerID='%s'" %(first_name,sur_name,company,telephone,email,address,postcode,id)

        c.execute(Update)
        db.commit()

        self.confirm_button.destroy()
        self.StateLabel.config(text = "Client Added!!",fg = "green")
        self.submit.config(state = ACTIVE,text = "Return", command = self.ResetEntireScreen)


    def RoundedCorneredCanvas(self, Window, x2, y2, feather, color = "#add8e6", x1 = 1, y1 = 1):

        x2 -= x1
        y2 -= y1
        points = []
        res = 30

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

        canvas = Canvas(Window, highlightthickness = 0, bg = BACKGROUND_COLOUR)
        canvas.create_polygon(points, fill = color)

        return canvas

if __name__ == "__main__":
    root = ThemedTk(theme = "arc")
    MainWindow = Parent(root)
    root.mainloop()

##http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
##http://stackoverflow.com/questions/20588417/how-to-change-font-and-size-of-buttons-and-frame-in-tkinter-using-python
