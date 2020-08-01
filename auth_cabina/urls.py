from django.urls import include, path
from rest_framework import routers
from .views import *

app_name = 'auth_cabina'

router = routers.DefaultRouter()
router.register(r'', UserViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('login/', LoginView.as_view(), name = 'LoginView'),
    path('logout/', LogoutView.as_view(), name = 'LoginView'),
    path('', include(router.urls)),
]
