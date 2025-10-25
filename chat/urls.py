from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # path('', views.chat_view, name='chat_view'),  # This was missing!
    path('send/', views.chat_send, name='chat_send'),
    path('suggestions/', views.chat_suggestions, name='chat_suggestions'),
    # path('widget-init/', views.chat_widget_init, name='widget_init'),
]