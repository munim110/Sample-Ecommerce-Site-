from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('new/',views.new, name='new'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.signin, name='login'),
    path('logout/',views.signout, name='logout'),
    path('userprofile/',views.userprofile, name='userprofile'),
    path('editinfo/',views.editinfo, name='editinfo'),
    path('changepassword/',views.changepassword, name='changepassword'),
]