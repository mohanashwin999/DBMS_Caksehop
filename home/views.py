from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.db import connection
from .cn import *

current_user={'username':'', 'email':'','address':'', 'fname':'', 'lname':'', 'status':False,'cake':''}


def signup(req):
    if req.method=='POST':
        user1=user()
        user1.email=req.POST.get('email')
        user1.fname=req.POST.get('fname')
        user1.lname=req.POST.get('lname')
        user1.username=req.POST.get('username')
        user1.password=hash_password(req.POST.get('password'))
        user1.address=req.POST.get('address')
        s_user=user.objects.raw('select * from home_user')
        for i in s_user:
            if user1.username in i.username:
                return render(req,'home/signup.html',{'error':'This username has already been taken'})
        else:
            user1.save()
            return redirect('home:login')
    else:
        return render(req,'home/signup.html')

def login(req):
    if req.method=='POST':
        uname=req.POST.get('username')
        pswrd=req.POST.get('password')
        try:
            login_user=user.objects.raw('select * from home_user where username=%s',[uname])[0]
        except:
            return render(req,'home/login.html',{'error':'No such username present!'})
        if login_user:
            if verify_password(login_user.password,pswrd):
                current_user['username']=login_user.username
                current_user['email']=login_user.email
                current_user['fname']=login_user.fname
                current_user['lname']=login_user.lname
                current_user['status']=True
                current_user['address']=login_user.address
                return redirect('home:landingpage2')
            else:
                return render(req,'home/login.html',{'error':'The password is incorrect!'})
        
    else:
        return render(req,'home/login.html')


def cakes(req):
    if current_user['status']==True:
        if req.method=='POST':
            pass
        else:
            return(render(req,'home/cakes.html'))
    else:
        return redirect('home:login')

def logout(req):
    current_user['username']=''
    current_user['email']=''
    current_user['fname']=''
    current_user['lname']=''
    current_user['status']=False
    current_user['address']=''
    return redirect('home:login')

def orders(req):
    if current_user['status']==True:
        o=order.objects.raw("select * from home_order as h inner join home_price_calculate as p  on h.weight=p.weight where h.delivered_status=0 and h.username=%s order by h.id desc",[current_user['username']])
        od=order.objects.raw("select * from home_order as h inner join home_price_calculate as p  on h.weight=p.weight where h.delivered_status=1 and h.username=%s order by h.id desc",[current_user['username']])
        return render(req,"home/orders.html",{'orders':o,'order_d':od})
    else:
        return redirect('home:login')

def weight(req):
    if current_user['status']==True:
        if req.method=='POST':
            p=order()
            op=req.POST.get('optradio')
            price1=price_calculate.objects.raw('select * from home_price_calculate where id=%s',[op])[0]
            p.cake_name=current_user['cake']
            p.weight=price1.weight
            p.price=price1.price
            p.username=current_user['username']
            p.save()
            return redirect('home:orderconf')
            
        else:
            current_user['cake']=req.GET['name']
            return(render(req,'home/weight.html'))

    else:
        return redirect('home:login')

def landingpage(req):
    return render(req,"home/landingpage.html")


def landingpage2(req):
    if current_user['status']==True:
        return render(req,"home/landingpage2.html",{'user':current_user['username']})
    else:
        return redirect('home:login')

def orderconf(req):
    if current_user['status']==True:
        l=order.objects.raw('select * from home_order order by id desc')[0]
        u=user.objects.raw('select * from home_user where username=%s',[current_user['username']])[0]
        c=p=order.objects.raw('select * from home_price_calculate where weight =%s',[l.weight])[0]
        try:
            sendmailtoadmin(l.id,l.username,l.cake_name,l.weight,u.address,c.price)
            sendmailtoreceiver(l.id,l.cake_name,l.weight,l.price,current_user['email'])
        except:
            pass
        return render(req,"home/orderconf.html",{'id':l.id,'cake_name':l.cake_name,'price':c.price})
    else:
        return redirect('home:login')

def feedback1(req):
    if current_user['status']==True:
        if req.method=='POST':
            f=feedback()
            f.username=current_user['username']
            f.text=req.POST.get('feedback')
            print(req.POST.get('feedback'))
            f.save()
            return redirect('home:landingpage2')
        else:
            return render(req,'home/feedback.html')
    else:
        return redirect('home:login')

def profile(req):
    if current_user['status']==True:
        if req.method=='POST':
            pass
        else:
            return render(req,'home/profile.html',{'fname':current_user['fname'],'lname':current_user['lname'],'email':current_user['email'],'address':current_user['address'],'user':current_user['username']})
    else:
        return redirect('home:login')

def update(req):
    if current_user['status']==True:
        if req.method=='POST':
            current_user['email']=req.POST.get('email')
            current_user['fname']=req.POST.get('fname')
            current_user['lname']=req.POST.get('lname')
            current_user['address']=req.POST.get('address')
            pswd=req.POST.get('password')
            with connection.cursor() as cursor:
                cursor.execute('update home_user set email = %s, fname=%s,lname=%s,address=%s,password=%s where username=%s',[current_user['email'],current_user['fname'],current_user['lname'],current_user['address'],hash_password(pswd),current_user['username']])
            return render(req,'home/message.html',{'message':'Your profile has been updated!'})
        else:
            return render(req,'home/update.html')
            
    else:
        return redirect('home:login')

def delete(req):
    if current_user['status']==True:
        if req.method=="POST":
            pswd=req.POST.get('password')
            login_user=user.objects.raw('select * from home_user where username=%s',[current_user['username']])[0]
            if verify_password(login_user.password,pswd):
                    with connection.cursor() as cursor:
                        cursor.execute('delete from home_user where username=%s',[current_user['username']])
                    return render(req,'home/landingpage.html',{'message':'Your profile has been successfully deleted'})
            else:
                return render(req,'home/delete.html',{'error':'The password is incorrect'})
        else:
            return render(req,'home/delete.html')
    else:
        return redirect('home:login')
