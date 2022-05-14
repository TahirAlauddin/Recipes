from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile


class CustomUserAdminConfig(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    search_fields = ('email', 'username')
    list_filter = ('email', 'username', 'is_active', 'is_staff')
    ordering = ['-created_since']
    list_display = ['email','username', 'is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields':('email', 'username', )}),
        ('Permissions', {'fields':('is_staff', 'is_active', )}),
        ('Personal', {'fields':('gender', 'postal_code',
                                'address', 'city', 'country')}),
        ('Important Dates', {'fields':('created_since', 'birth_date')})
    )

    add_fieldsets = (
        (None, {'fields':('email', 'username', 'password1', 'password2')}),
        ('Permissions', {'fields':('is_staff', 'is_active',)}),
        ('Personal', {'fields':('gender', 'postal_code',
                                'address', 'city', 'country')}),
        ('Important Dates', {'fields':('created_since', 'birth_date')})
    )
    
        
admin.site.register(CustomUser, CustomUserAdminConfig)
admin.site.register(Profile)
