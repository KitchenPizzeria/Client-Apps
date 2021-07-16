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
        
       