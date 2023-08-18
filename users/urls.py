from django.urls import path
from users import views
urlpatterns = [
    path('',views.home,name='index'),
    path('getvalue',views.getvalue,name='getvalue'),
    path('form',views.form,name='form'),
]