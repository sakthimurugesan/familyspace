from django.urls import path
from users import views
urlpatterns = [
    path('',views.home,name='index'),
    path('getvalue',views.getvalue,name='getvalue'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('login_try',views.login_try,name='login_try'),
    path('superuser',views.superuser,name='superuser'),
    #path('createsuperuser',views.createsuperuser,name='createsuperuser'),
]