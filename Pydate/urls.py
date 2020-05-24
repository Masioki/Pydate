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
from Pydate import views, settings
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base),
    path('register/', views.register),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('chat/', include('Chat.urls')),
    path('<str:username>/personal_questionnaire/', views.personal_questionnaire, name="personal_questionnaire"),
    path('my_matches/', views.my_matches, name="my_matches"),
    path('view_answers/', views.view_answers, name="view_answers"),
    url(r'^view_answers/(?P<id>\d+)/delete$', views.question_delete, name='question_delete'),
    url(r'^view_answers/(?P<id>\d+)/delete_match$', views.match_delete, name='match_delete'),
    url(r'^view_answers/(?P<id>\d+)/accept_match$', views.match_accept, name='match_accept'),
    url(r'^logout/$', views.logout_view, name='logout')

]
from django.conf import settings
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
