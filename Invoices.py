from RepeatedFunctions import RepeatedFunctions


class Invoices(RepeatedFunctions):
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
      