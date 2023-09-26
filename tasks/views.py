import time
import threading
from datetime import datetime, timedelta
from django.shortcuts import render,redirect
from django.http import HttpResponse
from familyspace.settings import BASE_DIR
from users.models import User
from tasks.models import AddTask,ShoppingProducts
from django.contrib.auth.models import auth
import django.contrib.auth
import django.contrib.messages as messages
from tasks.form import MyForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail


@csrf_protect
def task(request):
    email=0
    print(User.objects.get(email=request.session.get('email')).name)
    return render(request,"task.html",{"tasks":AddTask.objects.all().order_by('date','time').values(),"towhom":User.objects.get(email=request.session.get('email')).name})

@csrf_protect
def completedTask(request):
    return render(request,"completed.html",{"tasks":AddTask.objects.all().order_by('date','time').values(),"towhom":User.objects.get(email=request.session.get('email')).name})
    
def addtask(request):
    return render(request,"addtask.html",{'users':User.objects.values().all()})

def inserttask(request):
    if request.method=='POST':
        time=0
        taskname=str(request.POST['taskname'])
        date=str(request.POST['date'])
        time=str(request.POST['time'])
        desc=str(request.POST['desc'])
        form=MyForm(request.POST)
        private = request.POST.get('private',False)
        dateTime=date+" "+time
        towhom="all"
        towhom_email=""
        if(private=='on'):
            private=True
        try:
            if form.is_valid():
                # User.objects.get(email=email).is_superuser
                # form.cleaned_data['towhom']
                towhom=User.objects.get(id=form.cleaned_data['towhom']).name
                towhom_email=User.objects.get(id=form.cleaned_data['towhom']).email
        except:
            pass
            
        if(private==1 and towhom=='all'):
            print("all cannot have private task")
            messages.info(request,"all cannot have private task")
            target_url = reverse('addtask')

    
            return redirect(target_url) 

        if(time==''):
            AddTask.objects.create(taskname=taskname,
            date=date,
            towhom=towhom,
            desc=desc,private=private,
            towhom_email=towhom_email
            ,dateTime=dateTime)
        else:
            AddTask.objects.create(taskname=taskname,
            date=date,
            towhom=towhom,
            time=time,
            desc=desc,
            private=private,
            towhom_email=towhom_email,
            dateTime=dateTime
            )
    target_url = reverse('task')

    # Redirect to the target view's URL
    return redirect(target_url) 


def markAsDone(request,id):
    s=AddTask.objects.get(id=id)
    s.markasdone=1
    s.save()
    target_url = reverse('task')

    # Redirect to the target view's URL
    return redirect(target_url)

def shopingList(request):

    products=ShoppingProducts.objects.values().all()
    return render(request,"shoppingList.html",{"products":products})
def addShopingList(request):
    return render(request,"addShopingList.html")
def insertProducts(request):
    if request.method == 'POST':
        noOfProducts=int(request.POST["noOfProducts"])
        for i in range(1,noOfProducts+1):
            product=request.POST['product'+str(i)]
            quantity=request.POST['quantity'+str(i)]
            remarks=request.POST['remarks'+str(i)]
            ShoppingProducts.objects.create(
                productName=product,
                quantity=quantity,
                remarks=remarks
            )
    target_url = reverse('shopingList')

    # Redirect to the target view's URL
    return redirect(target_url)  


def isShopped(request,id):
    s=ShoppingProducts.objects.get(id=id)
    s.isShopped=1
    s.save()
    target_url = reverse('shopingList')

    # Redirect to the target view's URL
    return redirect(target_url)

def completedProducts(request):
    products=ShoppingProducts.objects.values().all()
    return render(request,"completedProducts.html",{"products":products})
@csrf_protect
def iwilldo(request,id):
    s=AddTask.objects.get(id=id)
    s.towhom=User.objects.get(email=request.session.get('email')).name
    s.towhom_email=request.session.get('email')
    s.save()
    target_url = reverse('task')
    return redirect(target_url)

def sayHi():
    k=1
    while True:
        tasks=AddTask.objects.values().all()
        today_time=datetime(datetime.today().year,datetime.today().month,datetime.today().day,datetime.today().hour,datetime.today().minute,0,0)
        delta_time=timedelta(days=1,hours=0,minutes=1)
        delta_time_1=timedelta(days=0,hours=1,minutes=1)
        delta_time_2=timedelta(days=0,hours=0,minutes=31)
        delta_time_3=timedelta(days=0,hours=0,minutes=6)

        for task in tasks:
            temp_date=datetime(task['dateTime'].year,task['dateTime'].month,task['dateTime'].day,task['dateTime'].hour,task['dateTime'].minute,0,0)

            email_subject="REMAINDER FROM FAMILYSPACE FOR YOUR TASK"

            message_text = "Please complete your task "+task['desc']+' on '+' '+str(task['dateTime'].day)+'/'+str(task['dateTime'].month)+"/"+str(task['dateTime'].day)
            from_email="msakthi150@outlook.com"
            reciever_email=[task['towhom_email']]

            if(today_time
            +delta_time==temp_date or today_time
            +delta_time_1==temp_date or today_time
            +delta_time_2==temp_date or today_time
            +delta_time_3==temp_date ):
                
                print(str(k)*50)
                send_mail(email_subject, message_text, from_email, reciever_email)
                k+=1
        time.sleep(60)



my_thread = threading.Thread(target=sayHi)
my_thread.start()