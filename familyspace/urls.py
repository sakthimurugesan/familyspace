from django.contrib import admin
from django.urls import path
from django.urls import include
urlpatterns = [
    path('donteventrytologin/', admin.site.urls),
    path('',include('users.urls')),
    path('tasks/',include('tasks.urls')),
    
   
]
