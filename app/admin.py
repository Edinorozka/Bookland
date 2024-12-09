from django.contrib import admin
from .models import User
from .models import Purchases
from .models import Purchases_books
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    def get_fieldsets(self, request, obj=None):
        if request.user.is_staff and not request.user.is_superuser:
            return [
                    (None, {'fields': ['username', 'email', 'is_active', 'last_login']})
                ]
        else:
            return self.fieldsets

class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status')
    
class Purchases_booksAdmin(admin.ModelAdmin):
    list_display = ('purchases_id', 'books_id', 'number')

admin.site.register(User, UserAdmin)
admin.site.register(Purchases, PurchasesAdmin)
admin.site.register(Purchases_books, Purchases_booksAdmin)