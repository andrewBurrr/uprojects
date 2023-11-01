from django.contrib import admin
from .models import (CustomUser, Owner, Interest, CustomAdmin, CustomAdminPermission,
                      Tag, Organization)
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

class AdminAdminConfig(UserAdmin):
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
    model = CustomAdmin
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
            'fields': ('email', 'first_name', 'last_name', 
                       'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


class OwnerAdmin(admin.ModelAdmin):
    model = Owner
    list_display = ("id",)
    

class InterestAdmin(admin.ModelAdmin):
    model = Interest
    list_display = ("interest",)
    

# class CustomUserAdmin(admin.ModelAdmin):
#     model = CustomUser
#     list_display =("id","email", "first_name", "last_name", "owner_id")


# class CustomAdminAdmin(admin.ModelAdmin):
#     model = CustomAdmin
#     list_display = ("id","email", "first_name", "last_name", "admin_type")


class CustomAdminPermissionAdmin(admin.ModelAdmin):
    model = CustomAdminPermission
    list_display = ("admin_id", "permission",)


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ("tag",)


class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ("org_id", "name", "owner_id",)



admin.site.register(Owner, OwnerAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(CustomAdmin, AdminAdminConfig)
admin.site.register(CustomAdminPermission, CustomAdminPermissionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Organization, OrganizationAdmin)