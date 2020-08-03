from django.urls import path

from . import views

app_name = 'auth_cabina'

router = routers.DefaultRouter()
router.register(r'', CaptureViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]
