from django.urls import path
from users import views
urlpatterns = [
    path('',views.home,name='index'),
    path('getvalue/<str:rdirect>',views.getvalue,name='getvalue'),
    path('register/<str:rdirect>',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('login_try',views.login_try,name='login_try'),
    path('superuser',views.superuser,name='superuser'),
    path('myfamily/',views.myfamily,name='myfamily'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('edit/<int:id>/',views.edit,name='edit'),
    path('save_edit/<int:id>/',views.save_edit,name='save_edit'),
    
]