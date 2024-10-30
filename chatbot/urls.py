from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('api/chat/', views.chat_view, name='chat_view'),
    path('login/', views.login_view, name='login'),
]
