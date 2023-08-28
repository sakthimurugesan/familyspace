from django.urls import path
from tasks import views
urlpatterns = [
    path('',views.task,name='task'),
    path('addtask/',views.addtask,name='addtask'),
    path('inserttask/',views.inserttask,name='inserttask'),
]