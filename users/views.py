from django.shortcuts import render,redirect
from django.http import HttpResponse
from familyspace.settings import BASE_DIR
from users.models import User, UserManager
from django.contrib.auth.models import User as ModelUser
from django.contrib.auth.models import auth
import django.contrib.auth
import django.contrib.messages as messages
from .form import MyForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.urls import reverse

def home(request):
    '''

     this function will check whether a superuser is created
     if not created it will redirect to superuser page
    else to home page
    
    '''
    if(User.objects.filter(id=1).exists()):
        print(User.objects.values_list('name'))
        return render(request,"index.html")
    else:
        target_url = reverse('superuser')
        return redirect(target_url)

def emailexist(email):
    return User.objects.filter(email=email).exists()


def login_try(request):
    if request.method=='POST':
        email=str(request.POST['email'])
        password=str(request.POST['password'])
        if(emailexist(email)):

            user=auth.authenticate(request,email=email,password=password)
            print(user)
            if user is not None:
                auth.login(request,user)
                messages.info(request,"login successful")
                return set_username(request)
                
            else:
                messages.info(request,"invalid password")
                target_url = reverse('login')
                return redirect(target_url)
        else:
            messages.info(request,"invalid email")
            target_url = reverse('register', args=['login'])
            return redirect(target_url)

    else:
        target_url = reverse('register')
        return redirect(target_url)


def getvalue(request,rdirect):
    print(rdirect+"redirect")
    if request.method=='POST':

        # getvalue method is used to get values from forms to create user

        form=MyForm(request.POST)
        """
        the following lines are used to get name,password,dob,email,mobile
        """
        name=str(request.POST['name'])
        password=str(request.POST['password'])
        dob=str(request.POST['dob'])
        email=str(request.POST['email'])
        mobile=0 
        #some might not have mobile so assign 0 default
        try:
            mobile=int(request.POST['mobile'])
             #some times the mobile field will be so we cannot get it as number
             # if user entered the value this try block will get that value
        except:
            pass   
        if form.is_valid():
            # the following lines are used to get blood gender and superuser value

            gender=form.cleaned_data['gender']
            blood=form.cleaned_data['blood']
            my_checkbox_value = request.POST.get('superuser',False)

            """by default we set superuser as false if we get 
            the value on it is true so we use if 
            block to convert it into true"""

            if(my_checkbox_value=='on'):
                my_checkbox_value=True
            alluser=User.objects.values_list('email')

            """
            here we have the try block to check whether a superuser is 
            created or not. if we have indexerror then superuser is not created
            if not superuser is created

            we use this function to create both superuser and user

            if superuser is alreaady exist we need the mail and password 
            of superuser to create new user that is executed in try block

            superuser is not created we need not need additional parameters
            and superuser is created in except block

            """
            if(User.objects.filter(id=1).exists()):
                superuseremail=str(request.POST['superuseremail'])
                superuserpassword=str(request.POST['superuserpassword'])
                if(emailexist(email)):
                    messages.info(request,"mail taken")
                    target_url = reverse('register', args=[rdirect])
                    return redirect(target_url)
                if(emailexist(superuseremail)):
                    user=auth.authenticate(request,email=superuseremail,password=superuserpassword)
                    if user is not None:
                        user = User.objects.create_user(email=email, password=password, name=name, mobile=mobile, dob=dob, gender=gender, blood=blood,is_superuser=my_checkbox_value)
                        if(rdirect=="''"):
                            target_url = reverse('index')
                            return redirect(target_url)
                        target_url = reverse(rdirect)
                        return redirect(target_url)
                    else:
                        messages.info(request,"invalid superuser password")
                        target_url = reverse('register', args=[rdirect])
                        return redirect(target_url)
                else:
                    
                    messages.info(request,"invalid superuser email")
                    target_url = reverse('register', args=[rdirect])
                    return redirect(target_url)

            else:
                user = User.objects.create_user(email=email, password=password, name=name, mobile=mobile, dob=dob, gender=gender, blood=blood,is_superuser=my_checkbox_value)
                target_url = reverse('index')
                return redirect(target_url)

            
    target_url = reverse('register')
    return redirect(target_url)



def myfamily(request):   
    return get_username(request)

@csrf_protect
def set_username(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        if username:
            request.session['email'] = username
            print(username)
            target_url = reverse('index')
            return redirect(target_url)





@csrf_protect
def get_username(request):
    email = request.session.get('email')
    return render(request,"myfamily.html",{"members":User.objects.values().all(),"is_superuser":User.objects.get(email=email).is_superuser,"email":email})



def register(request,rdirect): 
    #used to display register page
    return render(request,'register.html',{"rdirect":rdirect})

def login(request): #used to display login page
    return render(request,'login.html')

def superuser(request): #used to display superuser page
    if(User.objects.filter(id=1).exists()):
        target_url = reverse('index')
        return redirect(target_url)
    else:
        return render(request,"superuser.html")

def logout(request): #used to logout
    auth.logout(request)
    target_url = reverse('index')
    return redirect(target_url)
def delete(request,id):
    item = get_object_or_404(User, id=id)
    item.delete()
    target_url = reverse('myfamily')
    return redirect(target_url)
def edit(request,id):
    return render(request,"edit.html",{"person":User.objects.get(id=id),'superuser':User.objects.get(id=id).is_superuser})

def save_edit(request,id):
    if request.method=='POST':
        print("post working")
        # getvalue method is used to get values from forms to create user

        form=MyForm(request.POST)
        """
        the following lines are used to get name,password,dob,email,mobile
        """
        name=str(request.POST['name'])
        dob=str(request.POST['dob'])
        email=str(request.POST['email'])
        mobile=0 
        #some might not have mobile so assign 0 default
        try:
            mobile=int(request.POST['mobile'])
             #some times the mobile field will be so we cannot get it as number
             # if user entered the value this try block will get that value
        except:
            pass   
        if form.is_valid():
            # the following lines are used to get blood gender and superuser value

            gender=form.cleaned_data['gender']
            blood=form.cleaned_data['blood']
            my_checkbox_value = request.POST.get('is_superuser',False)
            print(my_checkbox_value)

            """by default we set superuser as false if we get 
            the value on it is true so we use if 
            block to convert it into true"""

            if(my_checkbox_value=='on'):
                my_checkbox_value=True
            item = get_object_or_404(User, id=id)
            item.name=name
            item.email=email
            item.dob=dob
            item.gender=gender
            item.blood=blood
            item.mobile=mobile
            item.is_superuser=my_checkbox_value
            print(item.is_superuser)
            item.save()
            target_url = reverse('myfamily')
            return redirect(target_url)
