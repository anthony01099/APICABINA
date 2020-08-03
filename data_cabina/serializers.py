from rest_framework import serializers
from .models import *



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name','description','users']

class CabinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabin
        fields = ['id','company']

class CaptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capture
        fields = ['id','cabin','temp','is_wearing_mask','is_image_saved','image']
