from django.urls import path
from . import views
app_name = 'mailapp' 
urlpatterns = [
    path('', views.send_email, name='send_email'),
    path('history/', views.history, name='history'),  # remove for now
]
