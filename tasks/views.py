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

@csrf_protect
def task(request):
    email=0
    print(User.objects.get(email=request.session.get('email')).name)
    return render(request,"task.html",{"tasks":AddTask.objects.all().order_by('date','time').values(),"towhom":User.objects.get(email=request.session.get('email')).name})

@csrf_protect
def completedTask(request):
    return render(request,"completed.html",{"tasks":AddTask.objects.all().order_by('date','time').values(),"towhom":User.objects.get(email=request.session.get('email')).name})
    
def addtask(request):
    print(User.objects.values_list('name'))
    return render(request,"addtask.html",{'users':User.objects.values_list('name')})

def inserttask(request):
    if request.method=='POST':
        time=0
        taskname=str(request.POST['taskname'])
        date=str(request.POST['date'])
        time=str(request.POST['time'])
        desc=str(request.POST['desc'])
        form=MyForm(request.POST)
        private = request.POST.get('private',False)
        if form.is_valid():
            towhom=form.cleaned_data['towhom']
            if(private=='on'):
                private=True
        if(private==1 and towhom=='all'):
            print("all cannot have private task")
            messages.info(request,"all cannot have private task")
            return redirect("../addtask")

        if(time==''):
            AddTask.objects.create(taskname=taskname,
            date=date,
            towhom=towhom,
            desc=desc,private=private)
        else:
            AddTask.objects.create(taskname=taskname,
            date=date,
            towhom=towhom,
            time=time,
            desc=desc,
            private=private)
    return redirect("../")


def markAsDone(request,id):
    s=AddTask.objects.get(id=id)
    s.markasdone=1
    s.save()
    return redirect("../")

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
            

    return redirect("../shopingList")

def isShopped(request,id):
    s=ShoppingProducts.objects.get(id=id)
    s.isShopped=1
    s.save()
    return redirect("../../shopingList")

def completedProducts(request):
    products=ShoppingProducts.objects.values().all()
    return render(request,"completedProducts.html",{"products":products})