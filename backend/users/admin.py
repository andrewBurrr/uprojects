from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class UserAdminConfig(UserAdmin):
    """
        Admin Definition for managing our custom user models

        This class extends the `admin.ModelAdmin` class provided by
        Django as a means of providing the builtin admin with the ability
        to modify the Users table in the Database.

        Attributes:
            model CustomUser: the specified user model
            search_fields (tuple): specify the searchable fields
            list_filtering (tuple): specify fields that can be reordered or filtered to limit results
            ordering (tuple): gives the default ordering pattern for listing users
            list_display (tuple): The listdisplay of an admin model is used to instruct
            the admin site on how to display objects within the admin site
        """
    model = CustomUser
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about', 'profile_image')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(CustomUser, UserAdminConfig)