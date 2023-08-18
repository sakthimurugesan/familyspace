from django.shortcuts import render,redirect
from django.http import HttpResponse
from familyspace.settings import BASE_DIR
from users.models import CustomUser, CustomUserManager

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
                    print(email)
                    print(password)
                    print(dob)
                    print(mobile)
                    print(name)
                    print(gender)
                    print(blood)
                user = CustomUser.objects.create_user(email=email, password=password, name=name, mobile=mobile, dob=dob, gender=gender, blood=blood,is_superuser=my_checkbox_value)
                print("created")
            except:
                print("not created")

    return redirect("/")

def form(request):
    return render(request,'form.html')