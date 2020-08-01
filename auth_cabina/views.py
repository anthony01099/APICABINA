from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from .serializers import *

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoginView(APIView):
    """
        Allows user login
    """
    def get(self, request):
        return Response({'detail': 'Request not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = json.loads(request.body)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request,user)
            return Response({'detail': 'successful'})
        else:
            return Response({'detail': 'Credentials not valid'})

class LogoutView(APIView):
    """
        Allows user logout
    """
    def get(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'})
