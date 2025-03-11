from django.contrib import admin
from django.urls import path,include
from .views import *
import dashboard.urls
app_name = 'employer'
urlpatterns = [
    path('',employer_login,name='employer_login'),
    path('employer_register',employer_register,name='employer_register'),
    path('employer_dashboard',employer_dashboard,name='employer_dashboard'),
    path('employer_logout',employer_logout,name='employer_logout'),
    path('search_candidates',search_candidates,name='search_candidates'),
]
