
from django.urls import path

from Chat import views

urlpatterns = [
    path('<int:chat_id>', views.index)
]
