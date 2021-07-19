from tkinter import *
from decimal import *
import tkinter.ttk as ttk
import sqlite3
import datetime
import re

class Customers():
    def __init__(self, master):
        self.master = master
        
        Headers = ['Firstname', 'Surname',"Company",'Contact Number',"Email","Address","Postcode"]
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        self.tree = ttk.Treeview(frame, columns = Headers, show = "headings")
        self.tree.grid(row = 0,column=0,in_= frame)
        
        self.TreeView(master,Headers,self.tree,frame)
        self.ProduceClientEditor(master)
        self.ProduceAddClientForm(master)
        
    def ProduceClientEditor(self,master):

        FilterCanvas = Canvas(master)
        FilterCanvas.place(x=2,y=2, width = 400, height = 190)
        FilterCanvas.create_rectangle(1, 1, 1000, 1000, fill="#add8e6",width = 3,outline="grey")        
        
        self.CFirstname = Label(FilterCanvas,text = "Firstname: None",bg = "#add8e6")
        self.CFirstname.place(x=180,y=8)
        self.CLastname = Label(FilterCanvas,text = "Lastname: None",bg = "#add8e6")
        self.CLastname.place(x=180,y=28)
        self.CCompany = Label(FilterCanvas,text = "Company: None",bg = "#add8e6")
        self.CCompany.place(x=180,y=48)
        self.CTelephone = Label(FilterCanvas,text = "Telephone: None",bg = "#add8e6")
        self.CTelephone.place(x=180,y=68)
        self.CEmail = Label(FilterCanvas,text = "Email: None",bg = "#add8e6")
        self.CEmail.place(x=180,y=88)
        self.CAddress = Label(FilterCanvas,text = "Address: None",bg = "#add8e6")
        self.CAddress.place(x=180,y=108)
        self.CPostcode = Label(FilterCanvas,text = "Postcode: None",bg = "#add8e6")
        self.CPostcode.place(x=180,y=128)   
        self.AmountOfClients = Label(FilterCanvas,text ="Amount of Clients: 0",bg = "#add8e6")
        self.AmountOfClients.place(x=23,y=128)

        Buttons = Canvas(FilterCanvas)
        Buttons.pack(side = BOTTOM, pady=8)

        self.ShowRecordsButton = ttk.Button(Buttons,text = "Show clients",command = self.DisplayAllRecords)
        self.ShowRecordsButton.grid(row=0,column=0)

        self.SelectRecordButton= ttk.Button(Buttons,text = "Select",state=DISABLED, command = self.SelectClient)
        self.SelectRecordButton.grid(row=0,column=1)

        self.DeleteClientButton = ttk.Button(Buttons, text = "Delete",state=DISABLED, command = self.DeleteClient)
        self.DeleteClientButton.grid(row=0,column=2)

        self.EditClientButton = ttk.Button(Buttons, text="Edit info", state=DISABLED,command = self.PopulateEditForm)
        self.EditClientButton.grid(row=0,column=3)

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
    
    def ProduceAddClientForm(self,master):
    
        ClientAdd = Canvas(master)
        ClientAdd.place(x=410,y=2, width = 310, height = 240)
        ClientAdd.create_rectangle(1, 1, 1000, 1000, fill="#add8e6")
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
                                 lambda:self.InputMask(master,self.QuickAdd,"","Customers"))
        self.Submit.grid(row=7,pady=5)
    
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
        self.SelectRecordButton.config(state=NORMAL)

        db = sqlite3.connect("Customers.db")
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

        self.tree.selection_clear()
        self.DeleteClientButton.config(state=ACTIVE)
        self.EditClientButton.config(state=ACTIVE)

        if self.SelectRecordButton["text"] == "Return":
            self.SelectRecordButton.config(text="Select")
        elif self.SelectRecordButton["text"] == "Select":
            self.SelectRecordButton.config(text="Return")

        items = self.tree.item(self.tree.selection())
        self.CFirstname.config(text = "Firstname: "+items["values"][0][:20])
        self.CLastname.config(text = "Lastname: "+items["values"][1][:20])
        self.CCompany.config(text = "Company: "+items["values"][2][:20])
        self.CTelephone.config(text = "Telephone: "+str(items["values"][3]))
        self.CEmail.config(text = "Email: "+items["values"][4][:20])
        self.CAddress.config(text = "Address: "+items["values"][5][:20])
        self.CPostcode.config(text = "Postcode: "+items["values"][6][:20])

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
                                                                        lambda:self.AddRecordToCustomerDatabase
                                                                        (grid,master))
                                        self.ConfirmButton.grid(column = 1, row = 7)
                                        self.Submit.config(text = "Edit",command =
                                                        lambda:self.Reset
                                                        (self,"Edit",grid,master))
                                        
                                    elif text == "FormWindow":
                                        self.ConfirmButton = ttk.Button(grid,text = "Confirm",command = lambda:EditFormWindow.ChangeDatabase
                                                                        (master,self.ConfirmButton,items))
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

    def AddRecordToCustomerDatabase(self,Grid,master):
        
        self.ConfirmButton.destroy()
        self.StateLabel.config(text = "Client Added!!",fg="black")
        self.Submit.config(state = ACTIVE,text = "Add New",command = lambda:self.Reset("Reset",Grid,master))
        
        db = sqlite3.connect("Customers.db")
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

    def PopulateEditForm(self):

        self.Submit.config(text="Modify")
        self.DeleteClientButton.config(state = DISABLED)
        
        items = self.tree.item(self.tree.selection())
        self.tree.delete(*self.tree.get_children())

        self.Firstname.insert(0,items["values"][0])
        self.Lastname.insert(0,items["values"][1])
        self.CompanyEntry.insert(0,items["values"][2])
        self.ContactNum.insert(0,items["values"][3])
        self.Email.insert(0,items["values"][4])
        self.Address.insert(0,items["values"][5])
        self.Postcode.insert(0,items["values"][6])
        
        

    def ChangeDatabase(self):

        items = self.tree.item(self.tree.selection())

        db = sqlite3.connect("Customers.db") 
        c = db.cursor()
        c.execute("SELECT * FROM Customers")
        Result = c.fetchall()
        for x in range(len(Result)):
            if Result[x][1] == items["values"][0] and Result[x][2] == items["values"][1] and Result[x][3] == items["values"][2]:  
                CustID = Result[x][0]
                
        db.execute("UPDATE Customers SET Firstname=?,Surname=?,Company=?,Telephone=?,Email=?,Address=?,Postcode=? WHERE CustomerID=?",
                   (self.Firstname.get(),self.Lastname.get(),self.CompanyEntry.get(),int(self.ContactNum.get()),
                    self.Email.get(),self.Address.get(),self.Postcode.get(),CustID))
        db.commit()
