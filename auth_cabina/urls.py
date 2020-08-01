from django.urls import include, path
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'auth_cabina'

router = routers.DefaultRouter()
router.register(r'', UserViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    #path('', include(router.urls)),
    path('login/', csrf_exempt(LoginView.as_view()), name = 'LoginView'),
    path('logout/', LogoutView.as_view(), name = 'LoginView'),
]
