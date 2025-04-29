from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='example'),
    path('save-questions/', views.save_questions, name='save_questions'),
    path('get-topics/', views.get_topics, name='get_topics'),
    path('get-questions/', views.get_questions, name='get_questions'),
]