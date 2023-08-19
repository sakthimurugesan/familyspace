from django.shortcuts import render,redirect
from django.http import HttpResponse
from familyspace.settings import BASE_DIR
from users.models import User, UserManager
from django.contrib.auth.models import User as ModelUser
from django.contrib.auth.models import auth
import django.contrib.auth
from.form import MyForm



def home(request):
    alluser=User.objects.values_list('email')
    try:
        t=alluser[0]
        return render(request,"index.html")
    except:
        return redirect("/superuser")

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
        if form.is_valid():
            gender=form.cleaned_data['gender']
            blood=form.cleaned_data['blood']
            my_checkbox_value = request.POST.get('superuser',False)
            if(my_checkbox_value=='on'):
                my_checkbox_value=True
            alluser=User.objects.values_list('email')
            try:
                t=alluser[0]
                superuserpassword=str(request.POST['superuserpassword'])
                superuseremail=str(request.POST['superuseremail'])
                superuserdatas = User.objects.filter(email=superuseremail).values()
                if superuserpassword==superuserdatas.password:
                    user = User.objects.create_user(email=email, password=password, name=name, mobile=mobile, dob=dob, gender=gender, blood=blood,is_superuser=my_checkbox_value)
                    return redirect("/")

            except:
                user = User.objects.create_user(email=email, password=password, name=name, mobile=mobile, dob=dob, gender=gender, blood=blood,is_superuser=my_checkbox_value)
                return redirect("/")
            

    return redirect("register")

def superuser(request):
    return render(request,"superuser.html")

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

