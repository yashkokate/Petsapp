from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password ,check_password
from .models import *
from .forms import*
import datetime

def index(request):
    context={}
    context=product.objects.all()
    sessionvalue = request.session.get('email', None)
    

    return render(request, 'index.html', {'session': sessionvalue, 'context': context})
def signup(request):
    password1=False
    if request.method=='POST':
        name=request.POST.get('yourname')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        errormsg=False
        if password1==password2:
            password1=make_password(password1)
        else:
            errormsg="Passwords doesnot match"
            return render(request,'signup.html', {'error':errormsg})
           

        user=users(name=name,email=email,password=password1)
        if users.objects.filter(email=email):
            errormsg='Email already exists'
            return render(request,'signup.html', {'error':errormsg})
        else:
            user.save()
            return render(request,'login.html')
    return render(request,'signup.html')
   
    
def login(request):
    flag=False
    errormsg=False
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        obj=users.objects.filter(email=email)
        if obj:
            flag=check_password(users.password,password)
            if True:
                request.session.modified=True
                request.session['email']=email
                return redirect('../')
            else:
                errormsg="Invalid password"
                return render(request,'login.html',{'error':errormsg})
        else:
            errormsg="Invalid email"
            return render(request,'login.html',{'error':errormsg})
    else:
            return render(request,'login.html',{'error':errormsg})
       
    
def profile(request):
    if request.method=='POST':
        name=request.POST['yourname']
        email=request.POST['email']
        password=request.POST['password1']

        cust=user.objects.get(email=email)
        cust.name=name
        cust.email=email
        cust.password=password
        cust.save()
        return render(request,'index.html',{'user':cust,'msg':"Profile Updated"})
    else:
        email = request.session['email']
        user = user.objects.get(email=email)
        return render(request,'profile.html',{'user':user})

def addtocart(request):
    if request.method=='POST':
        sessionvalue=request.session['email']
        productid=request.POST.get('productid')
        customerobj=users.objects.get(email=sessionvalue)
        productobj=product.objects.get(pk=productid)
        success=False
        if cart.objects.filter(customer=customerobj.id,product=productobj.id):
            cartobj1=cart.objects.get(customer=customerobj.id,product=productobj.id)
            quantity1=cartobj1.quantity+1
            totalprice=quantity1*productobj.cost
            cartobj1.quantity=quantity1
            cartobj1.totalcost=totalprice
            cartobj1.save()
            success="Item Added to Cart"
            
        else:
            cartobj=cart(quantity=1,totalcost=productobj.cost,customer=customerobj,product=productobj)
            cartobj.save()
            success="Item Added to Cart"
    return render(request,'index.html',{'success':success})

def viewcart(request):
    sessionvalue=request.session['email']
    productobj=product.objects.all()
    customerobj=users.objects.get(email=sessionvalue)
    cartobj=cart.objects.filter(customer=customerobj.id)
    return render(request,'cart.html', {'product':productobj , 'session':sessionvalue , 'cart':cartobj})

def changequantity(request):
    if request.method=='POST':
        buttonvalue = request.POST.get('quantityvalue')
        productid=request.POST.get('productid')
        sessionvalue=request.session['email']
        customerobj=users.objects.get(email=sessionvalue)
        productobj=product.objects.get(id=productid)
       
        if buttonvalue=='+':
            cartobj=cart.objects.get(customer=customerobj.id,product=productobj.id)
            quantity=cartobj.quantity+1
            totalcost=cartobj.totalcost*quantity
            cartobj.quantity=quantity
            cartobj.totalcost=totalcost
            cartobj.save()
        else:
            cartobj=cart.objects.get(customer=customerobj.id,product=productobj.id)
            quantity=cartobj.quantity-1
            totalcost=cartobj.totalcost*quantity
            cartobj.quantity=quantity
            cartobj.totalcost=totalcost
            cartobj.save()
    return redirect('../viewcart')

def placeorder(request):
    # sessionvalue = request.session['email']
    sessionvalue=request.POST.get('session')
    customerobj = users.objects.get(email = sessionvalue)
    cartobj = cart.objects.filter(customer = customerobj.id)
    totalamount = 0
    for i in cartobj:
        totalamount = totalamount + i.totalcost
        
    form = orderform
    
    return render(request,'orders.html',{'form' : form,'session':sessionvalue, 'totalamount':totalamount})
def orderpayment(request):
    sessionvalue = request.POST.get('session')
    customerobj1 = users.objects.get(email = 'y@gmail.com')
   
    form = orderform(request.POST)
    orderdata = orders()
    orderdata.user = customerobj1
    orderdata.name = request.POST.get('name')
    orderdata.phone = request.POST.get('phone')
    orderdata.email = request.POST.get('email')
    orderdata.country = request.POST.get('country')
    orderdata.state = request.POST.get('state')
    orderdata.city = request.POST.get('city')
    orderdata.address = request.POST.get('address')
    orderdata.total = request.POST.get('totalamount')
    orderdata.status ='new'
    orderdata.save()
    today1 = datetime.date.today()
    today1 = str(today1)
    today1 = today1.replace('-','')

    print(today1)
    orderdata.order_number = str(orderdata.id) + today1
    orderdata.save()
    
    cartobj = cart.objects.filter(customer= customerobj1.id)
    
    for i in cartobj:
        i.delete()
    from django.core.mail import EmailMessage
    
    # send_mail = EmailMessage('hello','Order is placed',to=['yashkokate135@gmail.com'])
    # send_mail.send()
    return render(request,'payment.html',{'orderdata':orderdata,'session': sessionvalue })

def paymentview(request):
   
    if request.method=="POST":
        user = request.POST.get("session")
        tsid = request.POST.get("tsid")
       
        status = request.POST.get("status")
        amountpaid = request.POST.get("amountpaid")
        userobj = users.objects.get(email=user)
        paymentobj = payment()
        paymentobj.payment_id = tsid
        paymentobj.status=status
        paymentobj.amount_paid= amountpaid
        paymentobj.user = userobj
        paymentobj.save()
    return render(request,'index.html')  

def logout(request):
   del request.session['email'] 
   sessionvalue = ''
   return render(request,'index.html',{'sessionvalue':sessionvalue})


     
    
        
        


    


    

    






