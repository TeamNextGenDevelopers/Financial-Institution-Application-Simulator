from __future__ import annotations
from flask import Flask, render_template, request
from flask import Flask, request, jsonify
from flask_cors import CORS
from main import Bank
from cloud_database import Database


app = Flask(__name__)
CORS(app)
connection_string = "mongodb+srv://tahshinshahriar:i2NK6Sc0jmCnhjWO@cluster0.nafiayb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_name = "financial-data"
collection_name = "user-info-collection"
db = Database(connection_string, db_name, collection_name)
bank = Bank() 

#Login Page
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if db.get_password(email) == password:
        return jsonify({'message': 'Login successful!'}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401


# Teller Interface
@app.route('/teler')
def tellerInterface(tellerObj):
    name = tellerObj.getUserName()
    idd = tellerObj.employeeID
    return render_template('tellerInterface.html', name=name, ID=idd)

@app.route('/thome')
def tellerHome():
    return tellerInterface(teller)


@app.route('/register-client', methods=['POST'])
def reg():
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    addr = request.form['addr']

    if clientp != False or None:
        return render_template('regsuccess.html', name=clientp.username, email=clientp.e_mail, passwd=clientp._password, phone=clientp.phone, accno=clientp._accountNumber, addr=clientp.address)
    else:
        return 'Reg failed!'


@app.route('/find')
def find():
    return render_template('find.html')


@app.route('/findp', methods=['POST'])
def findp():
    accno = request.form['accno']
    clientp = teller.findClient(int(accno))

    if clientp != False or None:
        return render_template('regsuccess.html', name=clientp.name, email=clientp.e_mail, phone=clientp.phone_no, accno=clientp._accountNumber, addr=clientp.address)
    else:
        return 'Client is not in the system!'

#Teller Ends



#Client Starts

@app.route('/client')
def clientInterface(clientObj):
    name = clientObj.username
    checkingsBalance = clientObj.chequingAccount.balance
    checkingsAccno = clientObj.chequingAccount.accountNumber
    if len(clientObj.savingsAccounts) > 0:
        savingsAcc = clientObj.savingsAccounts[0]
        savingsBalance = savingsAcc.balance
        savingsAccno = savingsAcc.accountNumber
    else:
        savingsBalance = "NIL"
        savingsAccno = "You don't have a Savings Account" 

    if len(clientObj.creditAccounts) > 0:
        creditAcc = clientObj.creditAccounts[0]
        creditBalance = creditAcc.balance
        creditAccno = creditAcc.accountNumber
    else:
        creditBalance = "NIL"
        creditAccno = "You don't have a Credit Account"        
    
    return render_template('clientInt.html', name=name, cbalance = checkingsBalance, caccno = checkingsAccno, sbalance = savingsBalance, saccno = savingsAccno, ccbalance = creditBalance, ccaccno = creditAccno)

#Home Page
@app.route('/chome')
def chome():
    return clientInterface(client)

#Apply for a Loan
@app.route('/applyLoan')
def loanapp():
    return render_template('applyLoan.html')

@app.route('/loanProccess', methods = ['POST'])
def loanp():
    amount = request.form['amount']
    loanType = request.form['type']
    sDate = request.form['sdate']      
    startDate = datetime.strptime(sDate, "%Y-%m-%d")
    eDate = request.form['edate']
    endDate = datetime.strptime(eDate, "%Y-%m-%d")
    loanSuccess = client.applyLoan(amount, loanType, startDate, endDate)
    if loanSuccess == True:
        return render_template('applyLoanSuccess.html', balance=client.loans[-1].amount, loantype=client.loans[-1].type, sdate=client.loans[-1].startDate, edate=client.loans[-1].endDate)
    else:
        return render_template('applyLoan.html', errmsg = "Input the fields appropriately")

# Apply for a Credit Account
@app.route('/applyCredit')
def Credapp():
    return render_template('applyCredit.html')


@app.route('/creditProccess', methods=['POST'])
def Credp():
    credBalance = request.form['balance']
    credSuccess = client.openCreditAccount(float(credBalance))
    if float(credBalance) < 500:
        return render_template('applyCredit.html', errmsg="Amount must be atleast 500")
    if credSuccess == True:
        return render_template('applyCreditSuccess.html', accno=client.creditAccounts[0].accountNumber, cbalance=client.creditAccounts[0].balance, srate=client.creditAccounts[0].yearlyRate, cafee=client.creditAccounts[0].cashAdvanceFee)
    else:
        return render_template('applyCredit.html', errmsg="Input all the field correctly")
    

#addPayee
@app.route('/addPayee')
def addpayee():
    return render_template('addPayee.html')
@app.route('/payeeProc', methods=['POST'])
def payeeProc():
    name = request.form['name']
    desc = request.form['desc']
    payee = Payee.Payee(name,desc)
    status = client.addPayee(payee)

    if status:
        return render_template("addPayeesuccess.html", name = payee.name, id = payee.payeeID, desc = payee.description)
    else:
        return "Error, couldn't add payee, try again"
    





#Open SavingsAccount
@app.route('/openSavings')
def Savingsapp():
    return render_template('openSavings.html')


@app.route('/savingsProc', methods=['POST'])
def savingsProc():
    savingsBalance = request.form['amount']
    credSuccess = client.openSavingsAccount()
    if credSuccess == True:
        return render_template('openSavingsSuccess.html', name = client.username, accno = client.savingsAccounts[0].accountNumber, amount = client.savingsAccounts[0].balance)
    else:
        return render_template('openSavings.html', errmsg = "Input all the field correctly")
    

#settings
@app.route('/settings')
def settings():
    return render_template('Settings.html')

# Change Details
@app.route('/details')
def details():
    return render_template('ChangeDet.html')


@app.route('/phoneProc', methods = ['POST'])
def phonenoProc():
    phoneno = request.form['phoneno']
    status = client.changePhone(phoneno)
    if status == True:
        return render_template("changeDetSuccess.html")
    else:
        return render_template('ChangeDet.html', errmsg = "Input Phone No properly")


@app.route('/emailProc', methods=['POST'])
def Proc():
    email = request.form['email']
    status = client.changePhone(email)
    if status == True:
        return render_template("changeDetSuccess.html")
    else:
        return render_template('ChangeDet.html', errmsg="Input Email properly")


@app.route('/addrProc', methods=['POST'])
def addrProc():
    addr = request.form['addr']
    status = client.changePhone(addr)
    if status == True:
        return render_template("changeDetSuccess.html")
    else:
        return render_template('ChangeDet.html', errmsg="Input Address properly")

# Blockn Card
@app.route('/block')
def block():
    return render_template('BlockCard.html')


@app.route('/blockProc', methods = ['POST'])
def blockProc():
    type = request.form['type']
    if type == "Debit":
        client.chequingAccount.card.lockCard()
        client.savingsAccounts[0].card.lockCard()
        return render_template('BlockCardSuccess.html')
    elif type == "Credit":
        client.creditAccounts[0].card.lockCard()
        return render_template('BlockCardSuccess.html')
    else:
        return render_template('BlockCard.html', errmsg = "Select Card Type")



# Delete account
@app.route('/delete')
def delete():
    return render_template('DeleteAcc.html')


# @app.route('/delproc')
# def delProc():
#     type = request.form['type']
#     passwd = request.form['passwd']
#     if client._password == passwd:
#         if type == "Savings":
#             client.

    
# Checkings Account
@app.route('/checkings')
def checkings():
    name = client.username
    checkingsBalance = client.chequingAccount.balance
    checkingsAccno = client.chequingAccount.accountNumber
    transactions = []
    for trnsac in client.chequingAccount.transactions:
        transacDict = {'sender': trnsac.sender,
                       'receiver': trnsac.receiver,
                       'amount': trnsac.amount,
                       'type': trnsac.__class__.__name__}
        transactions.append(transacDict)

    return render_template('balanceAccount.html', name=name, caccno=checkingsAccno, cbalance=checkingsBalance, transactions=transactions)

# SavingsAccount


@app.route('/savings')
def savings():
    name = client.username
    checkingsBalance = client.savingsAccounts[0].balance
    checkingsAccno = client.savingsAccounts[0].accountNumber
    transactions = []
    for trnsac in client.savingsAccounts[0].transactions:
        transacDict = {'sender': trnsac.sender,
                       'receiver': trnsac.receiver,
                       'amount': trnsac.amount,
                       'type': trnsac.__class__.__name__}
        transactions.append(transacDict)
    print(transactions)

    return render_template('balanceAccount.html', name=name, caccno=checkingsAccno, cbalance=checkingsBalance, transactions=transactions)

# CreditAccounts


@app.route('/credits')
def credits():
    name = client.username
    checkingsBalance = client.creditAccounts[0].balance
    checkingsAccno = client.creditAccounts[0].accountNumber
    transactions = []
    for trnsac in client.creditAccounts[0].transactions:
        transacDict = {'sender': trnsac.sender,
                       'receiver': trnsac.receiver,
                       'amount': trnsac.amount,
                       'type': trnsac.__class__.__name__}
        transactions.append(transacDict)

    return render_template('balanceAccount.html', name=name, caccno=checkingsAccno, cbalance=checkingsBalance, transactions=transactions)

# TransferFunds


@app.route('/transferFunds')
def transferFunds():
    return render_template('TransFunds.html')
@app.route('/transfundProc' , methods=['POST'])
def transfundProc():
    fromAcc = request.form['fromAcc']
    toAcc = request.form['toAcc']
    amount = request.form['amount']
    if len(client.savingsAccounts) == 0:
        return "You dont have a savings account"
    if fromAcc == "Savings" and toAcc == "Checkings":
        client.savingsAccounts[0].transferBetweenAccounts(float(amount), client.chequingAccount)
        return chome()
    elif fromAcc == "Checkings" and toAcc == "Savings":
        client.chequingAccount.transferBetweenAccounts(float(amount),  client.savingsAccounts[0])
        return chome()
    else:
        return "Input fields properly"    


#AutoPayments

@app.route('/autoPayments')
def autoPayments():
    option_values = []
    for x in client.payees:
        option_values.append(x.payeeID)
    option_names = []
    for x in client.payees:
        option_names.append(x.name)
    app.jinja_env.globals.update(len=len)    
    return render_template('AutoPay.html', option_values=option_values, option_names=option_names)

@app.route('/autopaymentsProc' ,methods=['POST'])
def autopaymentsProcs():
    payeeID = request.form['payee']
    amount = request.form['amount']
    acctype = request.form['acctype']

    for p in client.payees:
        if p.payeeID == int(payeeID):
            payee = p
    
    if acctype == "Savings":
        client.savingsAccounts[0].setupAutoPayment(
            payee, float(amount))
        return chome()
    elif acctype == "Checkings":
        client.chequingAccount.setupAutoPayment(
            payee, float(amount))
        return chome()
    else:
        return "error"




#Send Money

@app.route('/sendMoney')
def sendMoney():
    option_values = []
    option_names = []
    for x in client.payees:
        if isinstance(x, EtransferPayee.EtransferPayee):
            option_values.append(x.payeeID)
            option_names.append(x.name)
    app.jinja_env.globals.update(len=len)
    return render_template('SendMoney.html', option_values=option_values, option_names=option_names)
@app.route('/sendmoneyProc', methods=['POST'])
def sendMoneyProc():
    id = request.form['payee']
    acctype = request.form ['acctype']
    amount = request.form['amount']
    payee =  None
    for x in client.payees:
        if x.payeeID == int(id):
            payee = x
    if acctype == "Savings":
        if not client.savingsAccounts[0].sendEtransfer(float(amount), payee.email, payee.phone):
            return "Not in payees"
        return chome()
    elif acctype == "Checkings":
        if not client.chequingAccount.sendEtransfer(float(amount), payee.email, payee.phone):
            return "Not in payees"
        return chome()
    else:
        return "error"


#WireTransfer

@app.route('/wireTransfer')
def WireTransfer():
    return render_template('WireT.html')


@app.route('/wiretransferProc', methods=['POST'])
def wiretransferProc():
    details = request.form['details']
    amount = request.form['amount']
    acctype = request.form['acctype']

    if acctype == "Savings":
        client.savingsAccounts[0].sendWireTransfer(
            float(amount), str(details))
        return chome()
    elif acctype == "Checkings":
        client.chequingAccount.sendWireTransfer(
            float(amount), str(details))
        return chome()
    else:
        return "error"





if __name__ == '__main__':
    app.run(debug=True, port=50029)
