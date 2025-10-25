# resumebuild/urls.py

from django.urls import path
from . import views

app_name = 'resumebuild'

urlpatterns = [
    # The main builder page
    path('build/', views.build_resume_view, name='build_form'),
    
    
    # The live preview endpoint
    path('preview/<int:template_id>/', views.preview_resume_view, name='preview_resume'),
    
    # The download endpoint
    path('download/<int:template_id>/<str:format>/', views.download_resume_view, name='download_resume'),
]