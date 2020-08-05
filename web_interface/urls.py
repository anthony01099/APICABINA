from django.urls import path, include
from .views import *

app_name = 'web_interface'

urlpatterns = [
    path('create_token/', CreateToken.as_view(), name = 'CreateToken'),
]
