from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    def has_permission(self, request):
        # Use a different session key for admin to avoid conflicts
        request.session['is_admin'] = True
        return request.user.is_active and request.user.is_staff

admin_site = CustomAdminSite(name='custom_admin')



# Register your models here.
admin.site.register(Profile)
admin.site.register(Tweet)