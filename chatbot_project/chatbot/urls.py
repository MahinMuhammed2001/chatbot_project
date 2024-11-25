from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Main page
    path('chatbot/', views.chatbot_response, name='chatbot_response'),  # Chatbot API
    path('chatbot/', views.ask_chatbot, name='ask_chatbot'),
]
