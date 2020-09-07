from django.contrib import admin
from django import forms
# Register your models here.
from django.http import HttpResponseForbidden
from django.contrib.admin import SimpleListFilter, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from auth_cabina.models import UserToken
from data_cabina.models import Client
from data_cabina.models import Company, Setting

admin.site.unregister(User)
admin.site.register(UserToken)

class UserFilter(SimpleListFilter):
    title = 'is_staff'
    parameter_name = 'is_staff'

    def lookups(self, request, model_admin):

        if request.user.is_superuser:
            return tuple([])
        company = Client.objects.filter(user=request.user).first().company
        clients = company.client_set.all()
        users = [client.user for client in clients]
        related_objects = set(users)
        return [(related_obj.id, str(related_obj)) for related_obj in related_objects]

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            return queryset
        company = Client.objects.filter(user=request.user).first().company
        clients = company.client_set.all()
        users = [client.user.username for client in clients]
        users = User.objects.filter(username__in=users)
        return users


class SettingFilter(SimpleListFilter):
    title = 'company'
    parameter_name = 'company'

    def lookups(self, request, model_admin):

        if request.user.is_superuser:
            return tuple([])
        company = Client.objects.filter(user=request.user).first().company

        setting = Setting.objects.get(company=company)
        print(setting)

        related_objects = (setting,)
        return [(related_obj.id, str(related_obj)) for related_obj in related_objects]

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            return queryset
        company = Client.objects.filter(user=request.user).first().company

        setting = Setting.objects.filter(company=company)
        print(setting)

        return setting


class GeneralUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                               help_text=("Raw passwords are not stored, so there is no way to see "
                                          "this user's password, but you can change the password "
                                          "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = '__all__'


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'


class UserForm(GeneralUserForm):
    company = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs['instance']
        try:
            company_user = self.user.client.company
        except:
            company_user = None
        companies = Company.objects.all().order_by('name')
        companies_list = ([(company_user.id, company_user.name)] if company_user else [('-1', 'None')]) + [(company.id, company.name) for company in
                                                                                                           (companies.exclude(id=company_user.id) if company_user else companies)]
        self.fields['company'] = forms.ChoiceField(choices=companies_list)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=commit)
        #
        company_id = int(self.cleaned_data.get('company', None))
        try:
            company = Company.objects.get(id=company_id)
        except:
            return user
        try:
            client = Client.objects.get(user=user)
        except:
            client = Client(user=user, company=company)
        else:
            client.company = company
        client.save()

        return user

    class Meta:
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'user_permissions', 'is_active', 'is_staff', 'date_joined', 'last_login', 'company']


@admin.register(Setting)
class SettingAdmin(ModelAdmin):
    list_filter = (SettingFilter,)
    list_display = ('save_all',)
    fieldsets = [(None, {'fields': ()})]

    basic_fieldsets = [('Activation/Deactivation', {'fields': ('save_all',)}), ]
    superuser_fieldsets = basic_fieldsets.copy() + [("Company", {"fields": ("company",)},), ]
    user_fieldsets = basic_fieldsets.copy()

    def change_view(self, request, object_id, form_url='', extra_context=None):
        user = User.objects.get(id=object_id)
        #
        if request.user.is_superuser:

            self.fieldsets = self.superuser_fieldsets
        else:
            if request.user.client.company.id == user.client.company.id:
                self.fieldsets = self.user_fieldsets
            else:
                return HttpResponseForbidden()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return super().save_model(request, obj, form, change)

        if not change:
            save_result = super().save_model(request, obj, form, change)
        else:
            if request.user.client.company.id == obj.company.id:
                save_result = super().save_model(request, obj, form, change)
            else:
                save_result = None

        return save_result


@admin.register(User)
class UserAdmin(UserAdmin):
    view_on_site = False
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login')
    list_filter = (UserFilter,)
    form = GeneralUserForm
    fieldsets = [(None, {'fields': ()})]
    basic_fieldsets = [
        ('Data', {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        ('Activation/Deactivation', {'fields': ('is_active',)}), ]
    superuser_fieldsets = basic_fieldsets.copy() + [('Permissions', {'fields': ('is_staff', 'user_permissions', 'is_superuser',)}), ('Select company', {'fields': ('company',)})]
    user_fieldsets = basic_fieldsets.copy() + [('Permissions', {'fields': ('is_staff',)})]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        user = User.objects.get(id=object_id)
        #
        if request.user.is_superuser:
            self.form = UserForm
            self.fieldsets = self.superuser_fieldsets
        else:
            if request.user.client.company.id == user.client.company.id:
                self.form = GeneralUserForm
                self.fieldsets = self.user_fieldsets
            else:
                return HttpResponseForbidden()
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        user = User.objects.get(id=object_id)
        #
        if request.user.is_superuser:
            return super().delete_view(request, object_id, extra_context)
        elif request.user.client.company.id == user.client.company.id:
            return super().delete_view(request, object_id, extra_context)
        else:
            return HttpResponseForbidden()

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return super().save_model(request, obj, form, change)

        if not change:
            save_result = super().save_model(request, obj, form, change)
            # Add permissions
            permission_names = ['add_user', 'change_user', 'delete_user', 'delete_client']
            for permission_name in permission_names:
                permission = Permission.objects.get(codename=permission_name)
                obj.user_permissions.add(permission)
            # Assign company to new user
            company = Client.objects.filter(user=request.user).first().company
            client = Client.objects.create(user=obj, company=company)
        else:
            if request.user.client.company.id == obj.client.company.id:
                save_result = super().save_model(request, obj, form, change)
            else:
                save_result = None

        return save_result
