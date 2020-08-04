import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from .models import *


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cabin companies to be seen.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyCabins(APIView):
    """
        Returns cabins for a particular company
    """
    def get(self, request, company_id):
        cabins = Cabin.objects.filter(company__id=company_id)
        serializer = CabinSerializer(cabins, many=True)
        return Response(serializer.data)

class CompanyCaptures(APIView):
    """
        Returns captures for a particular company
    """
    def get(self, request, company_id):
        captures = Capture.objects.filter(cabin__company__id=company_id)
        serializer = CaptureSerializer(captures, many=True)
        return Response(serializer.data)

class CabinCaptures(APIView):
    """
        Returns captures for a particular cabin
    """
    def get(self, request, cabin_id):
        captures = Capture.objects.filter(cabin__id=cabin_id)
        serializer = CaptureSerializer(captures, many=True)
        return Response(serializer.data)

class CaptureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cabin captures to be seen.
    """
    queryset = Capture.objects.all().order_by('-created_at')
    serializer_class = CaptureSerializer
    permission_classes = [permissions.IsAuthenticated]
