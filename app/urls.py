from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('about/', about, name='about'),
    path('prediction/', prediction, name='prediction'),
    path('model/', model, name='model'),
    path('view/', view, name='view'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('user_logout/', user_logout, name='user_logout')
]
