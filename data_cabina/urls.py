from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'auth_cabina'

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet)
router.register(r'captures', CaptureViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('company_data/', CompanyData.as_view(), name='CompanyData'),
    path('cabins_company/', CompanyCabins.as_view(), name='CompanyCabins'),
    path('captures_company/', CompanyCaptures.as_view(), name='CompanyCaptures'),
    path('captures_company/<int:capture_id>/', RetrieveCompanyCapture.as_view(), name='RetrieveCompanyCapture'),
    path('captures_cabin/<int:cabin_id>/', CabinCaptures.as_view(), name='CabinCaptures'),
    path('captures_create/', CreateCapture.as_view(), name='CreateCapture'),
    path('register_cabin/', RegisterCabin.as_view(), name='RegisterCabin'),
    path('cabin_wifi_info/', CabinWifiInfo.as_view(), name='CabinWifiInfo'),
    path('associate_token/', AssociateUserToken.as_view(), name='AssociateToken'),
    path('', include(router.urls)),
]
