from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('user','message',)
    search_fields = ('user',)
