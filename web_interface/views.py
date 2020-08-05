from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from data_cabina.models import CabinToken

class CreateToken(View):
    """
        Web interface for creating an registering a cabin token.
    """
    def get(self, request):
        if request.user.is_superuser:
            return render(request,'web_interface/create_token.html')
        else:
            HttpResponseForbidden()

    def post(self, request):
        if request.user.is_superuser:
            token = CabinToken()
            token.save()
            context = {
                        'cabin_token': token.id,
            }
            return render(request,'web_interface/visualize_token.html',context)
        else:
            HttpResponseForbidden()
