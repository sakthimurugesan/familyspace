from django.shortcuts import render,redirect
from django.http import HttpResponse
from familyspace.settings import BASE_DIR
from users.models import User, UserManager
from django.contrib.auth.models import User as ModelUser
from django.contrib.auth.models import auth
import django.contrib.auth
from.form import MyForm



def home(request):
    print(BASE_DIR)
    return render(request,"index.html",{'name':'sakthi'})

def getvalue(request):
    if request.method=='POST':
        form=MyForm(request.POST)
        name=str(request.POST['name'])
        password=str(request.POST['password'])
        dob=str(request.POST['dob'])
        email=str(request.POST['email'])
        mobile=0
        try:
            mobile=int(request.POST['mobile'])
        except:
            pass
        # print(name)    
        if form.is_valid():
            gender=form.cleaned_data['gender']
            blood=form.cleaned_data['blood']
            print(mobile)
            try:
                my_checkbox_value = request.POST.get('superuser',False)
                if(my_checkbox_value=='on'):
                    my_checkbox_value=True
                user = User.objects.create_user(email=email, password=password, name=name, mobile=mobile, dob=dob, gender=gender, blood=blood,is_superuser=my_checkbox_value)
                print("created")
            except:
                print("not created")

    return redirect("/")

def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')


def login_try(request):
    if request.method=='POST':
        email=str(request.POST['email'])
        password=str(request.POST['password'])
        user=auth.authenticate(request,email=email,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            pass
    else:
        return redirect("register")

def logout(request):
    auth.logout(request)
    return redirect("/")