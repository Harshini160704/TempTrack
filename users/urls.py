from django.urls import path
from .import views

urlpatterns=[
    path('write/', views.write ,name='write'),
    path('read/', views.read, name='read'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('track/', views.track, name='track'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
]