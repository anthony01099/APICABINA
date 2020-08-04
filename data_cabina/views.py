import json, io
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

    def get(self, request):
        company = Company.objects.get(users=request.user)
        cabins = Cabin.objects.filter(company=company)
        serializer = CabinSerializer(cabins, many=True)
        return Response(serializer.data)


class CompanyCaptures(APIView):
    """
        Returns captures for a particular company
    """

    def get(self, request):
        company = Company.objects.get(users=request.user)
        captures = Capture.objects.filter(cabin__company=company)
        serializer = CaptureSerializer(captures, many=True)
        return Response(serializer.data)


class CabinCaptures(APIView):
    """
        Returns captures for a particular cabin
    """

    def get(self, request, cabin_id):
        company = Company.objects.get(users=request.user)
        if company != Cabin.objects.get(id=cabin_id).company:
            return Response({"detail": "You do not have access to this"})

        captures = Capture.objects.filter(cabin__id=cabin_id)
        serializer = CaptureSerializer(captures, many=True)
        return Response(serializer.data)


class CaptureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cabin captures to be seen.
    """
    queryset = Capture.objects.all().order_by('-created_at')
    serializer_class = CaptureSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateCapture(APIView):
    """
        Create a capture with a post request.
    """

    def get(self, request):
        return Response({'detail': 'Error. Must use post to create a capture'})

    def post(self, request):
        data = request.data
        # Get cabin instance
        try:
            cabin = Cabin.objects.get(id=data['cabin_id'])
        except:
            return Response({'detail': 'failed, invalid cabin_id'})
        else:
            # Create capture object
            capture = Capture(cabin=cabin,
                              temp=data['temp'],
                              is_wearing_mask=data['is_wearing_mask'],
                              is_image_saved=data['is_image_saved'])
            capture.save()
            # Create image file
            if data['is_image_saved']:
                image_bytes = io.BytesIO()
                image_bytes.write(data['image_base64'].encode())
                capture.image.save(str(capture.id) + '.txt', image_bytes)
            return Response({'detail': 'successful'})
