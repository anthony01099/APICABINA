import json, io
from django.http import Http404, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from api_cabina.permissions import IsSuperUser
from .serializers import *
from .models import *

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cabin companies to be seen.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]

class CompanyData(APIView):
    """
        Returns data for the user's company
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):           
        company = request.user.client.company
        serializer = CompanySerializer(company)
        return Response(serializer.data)

class CompanyCabins(APIView):
    """
        Returns cabins for a particular company
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        company = request.user.client.company
        cabins = Cabin.objects.filter(company=company)
        serializer = CabinSerializer(cabins, many=True)
        return Response(serializer.data)


class CompanyCaptures(APIView):
    """
        Returns captures for a particular company
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        company = request.user.client.company
        captures = Capture.objects.filter(cabin__company=company)
        serializer = CaptureSerializer(captures, many=True)
        return Response(serializer.data)


class CabinCaptures(APIView):
    """
        Returns captures for a particular cabin
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cabin_id):
        company = request.user.client.company
        cabin = Cabin.objects.filter(id=cabin_id)

        if not cabin.exists():
            return Response({"detail": "You do not have access to this"})

        if company != cabin.first().company:
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
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]

@method_decorator(csrf_exempt, name='dispatch')
class CreateCapture(View):
    """
        Create a capture with a post request.
    """
    def get(self, request):
        return JsonResponse({'detail': 'Error. Must use post to create a capture'})

    def post(self, request):
        data = json.loads(request.body)
        # Get cabin instance
        try:
            cabin = Cabin.objects.get(token__id = data['token'])
        except:
            return JsonResponse({'detail': 'failed, invalid token'})
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
            return JsonResponse({'detail': 'successful'})

class RegisterCabin(APIView):
    """
        Register a cabin using a token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'detail': 'Error. Must use post to register a cabin'})

    def post(self, request):
        #Retrieve data
        company = request.user.client.company
        token_str = request.data['token']
        try:
            token = CabinToken.objects.get(id=token_str)
        except:
            return Response({'detail': 'Token not valid'})
        else:
            if token.is_used:
                return Response({'detail': 'Token already used'})
            else:
                cabin = Cabin(company= company, token = token)
                cabin.save()
                token.is_used = True
                token.save()
                return Response({'detail': 'successful', 'cabin_id': cabin.id})
