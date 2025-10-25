from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include

app_name = "ARDAA" 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),  
    path("aboutus/", views.aboutus, name="aboutus"),
    # path("result/", views.result, name="result"),
    # path("login/", views.login_view, name="login"),
    path("analyze/", views.analyze, name="analyze"),
    path("accounts/", include("accounts.urls")),  
    # path('chat/ask/', views.chat_ask, name='chat_ask'),
    path('result/', views.result_view, name='result_page'),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("resumebuild/", include("resumebuild.urls")),
    path("chat/", include("chat.urls")),
    # path('chat/send/', views.send_message, name='chat_send'),
    # path('chat/health/', views.chat_health, name='chat_health'),


]
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include
import json

app_name = "ARDAA" 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),  
    path("aboutus/", views.aboutus, name="aboutus"),
    path("analyze/", views.analyze, name="analyze"),
    path("accounts/", include("accounts.urls")),  
    path('result/', views.result_view, name='result_page'),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("resumebuild/", include("resumebuild.urls")),
    path("chat/", include("chat.urls")),
    path('after-login/', views.after_login, name='after_login'),
]
