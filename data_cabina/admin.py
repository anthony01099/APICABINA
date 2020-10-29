from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.admin import SimpleListFilter, ModelAdmin
from django.http import HttpResponseForbidden
from .models import *

admin.site.site_header = 'American Biosecurity'

class BoothFilter(SimpleListFilter):
    title = 'booth'
    parameter_name = 'company'

    def lookups(self, request, model_admin):

        if request.user.is_superuser:
            return tuple([])

        return [('all','All')]

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            return queryset
        booths = Cabin.objects.filter(company=request.user.client.company)
        return booths


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Cabin)
class CabinAdmin(admin.ModelAdmin):
    list_filter = (BoothFilter,)
    list_display = ('id', 'company',)
    search_fields = ('id', 'company',)
    fieldsets = [('Data', {'fields': ('token', 'wifi_ssid', 'wifi_password', 'language')}) ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        booth = Cabin.objects.get(id=object_id)
        #
        if not request.user.is_superuser:
            if request.user.client.company.id != booth.company.id:
                return HttpResponseForbidden()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        booth = Cabin.objects.get(id=object_id)
        #
        if not request.user.is_superuser:
            if request.user.client.company.id != booth.company.id:
                return HttpResponseForbidden()
        return super().delete_view(request, object_id, extra_context)


@admin.register(CabinToken)
class CabinTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_used',)
    search_fields = ('is_used',)
