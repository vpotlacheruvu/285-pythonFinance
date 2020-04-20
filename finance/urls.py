from django.urls import path
from . import views

urlpatterns = [
    path('', views.FinanceView.as_view()),
]
