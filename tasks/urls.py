from django.urls import path
from tasks import views
urlpatterns = [
    path('',views.task,name='task'),
    path('addtask/',views.addtask,name='addtask'),
    path('completed/',views.completedTask,name='completed'),
    path('inserttask/',views.inserttask,name='inserttask'),
    path('markAsDone/<int:id>',views.markAsDone,name='markAsDone'),
    path('shopingList/',views.shopingList,name='shopingList'),
    path('addShopingList/',views.addShopingList,name='addShopingList'),
    path('insertProducts/',views.insertProducts,name='insertProducts'),
]