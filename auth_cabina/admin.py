from django.contrib import admin
from django import forms
# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from auth_cabina.models import Client
from data_cabina.models import Company

admin.site.unregister(User)

admin.site.register(Client)


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

class UserForm(forms.ModelForm):
    company = forms.CharField()

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs['instance']
        '''
        self.fields['password'] = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))
        '''
        try:
            company_user = self.user.client.company
        except:
            company_user = None
        companies = Company.objects.all().order_by('name')
        companies_list = ([(company_user.id, company_user.name)] if company_user else [('-1','None')])+ [(company.id, company.name) for company in (companies.exclude(id=company_user.id) if company_user else companies)]
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
            client = Client.objects.get(user = user)
        except:
            client = Client(user = user, company = company)
        else:
            client.company = company
        client.save()

        return user

    class Meta:
        model = User
        fields = ['username','password','email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login','company']

@admin.register(User)
class UserAdmin(UserAdmin):
    view_on_site = False
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login')
    list_filter = (UserFilter,)
    form = UserForm
    fieldsets = [
        ('Data', {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        ('Activation/Deactivation', {'fields': ('is_active',)}),
        (None,{'fields': ()}),
        (None,{'fields': ()}),
    ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.fieldsets[2] = ('Permissions', {'fields': ('is_staff', 'groups', 'is_superuser',)})
            self.fieldsets[3] = ('Select company', {'fields': ('company',)})
        else:
            self.fieldsets[2] = ('Permissions', {'fields': ('is_staff',)})
            self.fieldsets[3] = (None,{'fields': ()})
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return super().save_model(request, obj, form, change)
        #Add permissions
        save_result = super().save_model(request, obj, form, change)
        if not change:
            permission_names = ['add_user','change_user','delete_user']
            for permission_name in permission_names:
                permission = Permission.objects.get(codename=permission_name)
                obj.user_permissions.add(permission)
            #Assign company to new user
            company = Client.objects.filter(user=request.user).first().company
            client = Client.objects.create(user = obj, company = company)
        return save_result
