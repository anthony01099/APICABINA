from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required


class CreateToken(View):
    """
        Web interface for creating an registering a cabin token.
    """
    def get(self, request):
        return render(request,'web_interface/create_token.html',{})

    def post(self, request):
        pass
