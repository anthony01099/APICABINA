from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from data_cabina.models import Company

admin.site.unregister(User)


class UserFilter(SimpleListFilter):
    title = 'is_staff'
    parameter_name = 'is_staff'

    def lookups(self, request, model_admin):
        company = Company.objects.filter(users=request.user).first()
        related_objects = set(company.users.all())
        return [(related_obj.id, str(related_obj)) for related_obj in related_objects]

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            return queryset

        company = Company.objects.filter(users=request.user).first()
        return company.users.all()


@admin.register(User)
class UserAdmin(UserAdmin):
    view_on_site = False
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login')
    list_filter = (UserFilter,)
    fieldsets = (
        ('Data', {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        ('Activation/Deactivation', {'fields': ('is_active',)}),
        ('Permissions', {'fields': ('is_staff', 'groups',)})
    )

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return super().save_model(request, obj, form, change)

        save_result = super().save_model(request, obj, form, change)
        company = Company.objects.filter(users=request.user).first()
        company.users.add(obj)
        company.save()
        print(request.user)
        print(obj)

        return save_result
