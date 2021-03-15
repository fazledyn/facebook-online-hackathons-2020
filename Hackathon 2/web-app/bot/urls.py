from django.urls import path
from . import views

urlpatterns = [
    path('',            views.index,        name='index'),
    path('dashboard',   views.dashboard,    name='dashboard'),
    path('signup',      views.signup,       name='signup'),
    path('logout',      views.site_logout,  name='logout')
]