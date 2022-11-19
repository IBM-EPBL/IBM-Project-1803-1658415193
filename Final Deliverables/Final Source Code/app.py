from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=vvb92978;PWD=vO6OzCYS88jLOPTQ",'','')
print ("Database connection established", conn)

app = Flask(__name__)



@app.route('/')
def home():
  return render_template('index.html')
  
@app.route('/2')
def home2():
  return render_template('index1.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.route('/adlogin')
def adlogin():
  return render_template('adminlogin.html')

@app.route('/adsignup')
def adsignup():
  return render_template('adsignup.html')

@app.route('/adminnotify')
def adminnotify():
    message = Mail(from_email="dhanushraj1411@gmail.com",to_emails="rohansri2002@gmail.com",subject="Out of limit",html_content="<p>Some products are out of stock please check it out and add the corresponding products</p>")
    
    try:
     sg = SendGridAPIClient("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")
     response = sg.send(message)
     return render_template('dashboard.html',msg="Admin have been notified through mail")
    except Exception as e:
     print(e)
     return render_template('dashboard.html',msg="Error")


@app.route('/regsignup',methods = ['POST', 'GET'])#signup.html
def regsignup():
  if request.method == 'POST':

    name = request.form['username']
    email = request.form['loginUser']
    password = request.form['loginPassword']
    ConfirmPassword = request.form['confirmPassword']

    sql = "SELECT * FROM CUSTOMER_DATA WHERE email = ?"
    
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('msg.html', msg="Already Registered. Please wait we will redirect to the log in page.")
    else:
      insert_sql = "INSERT INTO CUSTOMER_DATA VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, ConfirmPassword)

      
      ibm_db.execute(prep_stmt)
      message = Mail(from_email="dhanushraj1411@gmail.com",to_emails=email,subject="User Registration",html_content="<p>You have been successfully registered as a Customer.Please Log in to see our Products.</p>")
    
    try:
     sg = SendGridAPIClient("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")
     response = sg.send(message)
     return render_template('login.html',msg="Registration successfull. Please login using your credentials")
    except Exception as e:
     print(e)
    
   
     return render_template('msg.html', msg=" Successfully Registered. Please wait we will redirect to the log in page.")



@app.route('/check',methods = ['POST', 'GET'])#login.html
def check():
    
   if request.method == 'POST':
    
    email = request.form['loginUser']
    password = request.form['loginPassword']

    sql = "SELECT * FROM CUSTOMER_DATA WHERE  email=? and password= ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      return render_template('dashboard.html')
    else:
      return render_template('msg.html' , msg="Invalid Username / Password" )

     
@app.route('/adminsignup',methods = ['POST', 'GET'])#adminsignup.html
def adminsignup():
  if request.method == 'POST':

    name = request.form['adusername']
    email = request.form['adloginUser']
    password = request.form['adloginPassword']
    ConfirmPassword = request.form['adconfirmPassword']

    sql = "SELECT * FROM ADMIN_DATA WHERE email = ?"
    
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('msg1.html', msg="Already Registered. Please wait we will redirect to the log in page.")
    else:
      insert_sql = "INSERT INTO ADMIN_DATA VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, ConfirmPassword)

      
      ibm_db.execute(prep_stmt)
    
   
    return render_template("msg1.html"  ,msg="Successfully Registered. Please wait we will redirect to the log in page.")


@app.route('/adminlogin',methods = ['POST', 'GET'])#adminlogin.html
def adminlogin():
    
   if request.method == 'POST':
    
    email = request.form['adloginUser']
    password = request.form['adloginPassword']

    sql = "SELECT * FROM ADMIN_DATA WHERE email=? and password= ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      return render_template('additem.html')

    else:
      return render_template('adsignup.html')



@app.route('/additem',methods = ['POST', 'GET'])#additem.html
def additem():
  if request.method == 'POST':

    id = request.form['pcode']
    name = request.form['pname']
    price = request.form['price']
    stock = request.form['stock']
   

    sql = "SELECT * FROM PRODUCT_DATA WHERE PRODUCT_NAME=? and PRODUCT_CODE=? "
    
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.bind_param(stmt,2,id)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('additem.html', msg="Product already added")
    else:
      insert_sql = "INSERT INTO PRODUCT_DATA VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, id)
      ibm_db.bind_param(prep_stmt, 2, name)
      ibm_db.bind_param(prep_stmt, 3, price)
      ibm_db.bind_param(prep_stmt, 4, stock)
      
      ibm_db.execute(prep_stmt)
    
   
    return render_template('additem.html',msg="Product successfully added" )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


