"""Pydate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Pydate import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base),
    path('register/', views.register),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('chat/', include('Chat.urls')),
    path('personal_questionnaire/', views.personal_questionnaire, name="personal_questionnaire"),
    url(r'^logout/$', views.logout_view, name='logout'),
    path('profile/', views.profile)
]
urlpatterns += staticfiles_urlpatterns()
