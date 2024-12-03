from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    def get_fieldsets(self, request, obj=None):
        if request.user.is_staff and not request.user.is_superuser:
            return [
                    (None, {'fields': ['username', 'email', 'is_active', 'last_login']})
                ]
        else:
            return self.fieldsets

admin.site.register(User, UserAdmin)