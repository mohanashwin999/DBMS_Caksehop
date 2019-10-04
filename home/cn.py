import smtplib
import hashlib, binascii, os

def sendmailtoadmin(id,username,cakename,weight,address,price):
    s1="python3.smtp@gmail.com"
    p="python@123"
    r="mohanashwin999@gmail.com"
    m='''
        Subject: Order of {}

        ID:{}
        Cake Name:{}
        Cake Weight:{} kg
        Delivery Address:{}
        Price:{}
    '''.format(username,id,cakename,weight,address,price)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(s1,p) 
    s.sendmail(s1,r,m) 
    s.quit()

def sendmailtoreceiver(id,cakename,weight,price,receiver):
    s1="python3.smtp@gmail.com"
    p="python@123"
    r=receiver
    m='''
        Your order has been confirmed

        Your Order ID:{}
        Cake Name:{}
        Cake Weight:{} kg
        Price:{}

        Only COD option available
    '''.format(id,cakename,weight,price)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(s1,p) 
    s.sendmail(s1,r,m) 
    s.quit()


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password