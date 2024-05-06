# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('oscillators/', views.OscillatorsView.as_view(), name='oscillators'),
]