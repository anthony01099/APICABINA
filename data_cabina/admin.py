from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from .models import *

admin.site.site_header = 'American Biosecurity'

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Cabin)
class CabinAdmin(admin.ModelAdmin):
    list_display = ('id','company',)
    search_fields = ('id','company',)

@admin.register(CabinToken)
class CabinTokenAdmin(admin.ModelAdmin):
    list_display = ('id','is_used',)
    search_fields = ('is_used',)
