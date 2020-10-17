from rest_framework import serializers
from .models import *



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','name','description']

class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = ['id','company']

class CompanyCabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = ['id','token','wifi_ssid']
        depth = 1

class CaptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capture
        fields = ['id','cabin','temp','is_wearing_mask','is_image_saved','image_base64','created_at']

class SimpleCaptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capture
        fields = ['id','cabin','temp','is_wearing_mask','is_image_saved','created_at']

class CaptureImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capture
        fields = ['id','image_base64']
