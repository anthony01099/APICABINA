import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import Http404, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from .serializers import *
from .models import *

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    """
        Allows user login
    """
    def get(self, request):
        return JsonResponse({'detail': 'Request not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if not request.user.is_authenticated:
            data = json.loads(request.body)
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request,user)
                return JsonResponse({'detail': 'successful'})
            else:
                return JsonResponse({'detail': 'Credentials not valid'})
        else:
            return JsonResponse({'detail': 'There is an user active. Logout first.'})

class LogoutView(APIView):
    """
        Allows user logout
    """
    def get(self, request):
        logout(request)
        return Response({'detail': 'Logout successful'})
