from api.auth.views import login
from django.urls import path

urlpatterns = [
    path('login', login)
]
