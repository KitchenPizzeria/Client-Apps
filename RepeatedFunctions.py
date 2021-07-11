from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re

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
