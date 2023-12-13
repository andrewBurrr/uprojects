from django.contrib import admin
from .models import (CustomUser, Owner, CustomAccount, CustomAdmin, CustomAdminPermission,
                     Tag, Organization)
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class AccountAdminConfig(UserAdmin):
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
    model = CustomAccount
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
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()



class OwnerAdmin(admin.ModelAdmin):
    """
        Admin Definition for managing our Owner models

        This class extends the `admin.ModelAdmin` class provided by
        Django as a means of providing the builtin admin with the ability
        to modify the Owner table in the Database.

        Attributes:
            model Owner: Specified Owner model
            list_display (tuple): The list display of an Owner model is used to 
            instruct the admin site on how to display objects within the admin site
        """
    model = Owner
    list_display = ("id",)

# create a custom user admin model like AccountAdminConfig
class CustomUserAdmin(AccountAdminConfig):
    model = CustomUser

    search_fields = ('email', 'first_name', 'last_name', 'owner_id')
    list_filter = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'owner_id', 'tags')
    ordering = ('-start_date',)
    list_display = ('id', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'owner_id')
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
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'tags')}
         ),
    )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    


# class CustomAdminAdmin(admin.ModelAdmin):
#     model = CustomAdmin
#     list_display = ("id","email", "first_name", "last_name", "admin_type")


class CustomAdminPermissionAdmin(admin.ModelAdmin):
    """
    Admin Definition for managing our CustomAdminPermission models

        This class extends the `admin.ModelAdmin` class provided by
        Django as a means of providing the builtin admin with the ability
        to modify the CustomAdminPermission table in the Database.

        Attributes:
            model CustomAdminPermission: Specified CustomAdminPermission model
            list_display (tuple): The list display of an CustomAdminPermission 
            model is used to instruct the admin site on how to display objects 
            within the admin site 
    """
    model = CustomAdminPermission
    list_display = ("admin_id", "permission",)

def populate_tags(modeladmin, request, query_set):

    tag_names= ["Java", "C", "Python", "C++", "C#", "Visual Basic .NET",
    "JavaScript", "Swift", "PHP", "SQL", "Go", "Assembly language", "Ruby", "MATLAB",
    "Groovy", "Perl", "Rust", "R", "TypeScript", "Ada", "Lua", "Kotlin", "COBOL",
    "Fortran", "Julia", "Dart", "ABAP", "Shell", "SAS", "PL/SQL", "F#", "Objective-C",
    "Scala", "Pascal", "Apex", "LabVIEW", "D", "Transact-SQL", "Delphi/Object Pascal",
    "VBScript", "Logo", "Prolog", "Scratch", "REXX", "AWK", "Kotlin/Native", "RPG (OS/400)",
    "Swift (iOS)", "Python (Stackless)", "C (Embedded)", "JCL", "Scheme", "Groovy (Android)",
    "Go (Golang)", "Ruby (JRuby)", "Python (MicroPython)", "Lua (LuaJIT)", "Bash",
    "PowerShell", "R (GNU S)", "JavaScript (Emscripten)", "C++ (Embedded)", "Ruby on Rails",
    "COBOL (Micro Focus)", "Fortran (GFortran)", "LabVIEW (G)", "PHP (HHVM)", "SQL (PL/SQL)",
    "Hack (HHVM)", "Julia (JuliaLang)", "TypeScript (Deno)", "Ada (GNAT)", "Kotlin (JVM)",
    "Assembly language (NASM)", "Swift (Server Side)", "Go (GoLand)", "Groovy (Grails)",
    "Perl (ActiveState Perl)", "Rust (Mozilla)", "R (Microsoft R Open)", "TypeScript (TypeScript Node)",
    "Assembly language (WebAssembly)", "Swift (SwiftUI)", "Go (Revel)", "Groovy (Apache Groovy)",
    "Perl (Strawberry Perl)", "Rust (Redox)", "R (RStudio)", "TypeScript (Angular)",
    "Assembly language (ARM)", "Swift (React Native)", "Go (Fuchsia)", "Groovy (GroovyJS)",
    "Perl (Raku)", "Rust (RustOS)", "R (Bioconductor)", "TypeScript (Vue.js)",
    "Assembly language (MIPS)", "Swift (Perfect)", "Go (Android)", "Groovy (Grooscript)",
    "Perl (Perl6)", "Rust (Tock)","Assembly language (x86)" "Swift", "Go" "Groovy",
    "Perl", "Rust","R","TypeScript",]
    for tag_name in tag_names:
        Tag.objects.get_or_create(tag=tag_name)
    
populate_tags.short_description = "Populate tags from list"

class TagAdmin(admin.ModelAdmin):
    actions =[populate_tags]
    """
    Admin Definition for managing our Tag models

        This class extends the `admin.ModelAdmin` class provided by
        Django as a means of providing the builtin admin with the ability
        to modify the Tag table in the Database.

        Attributes:
            model Tag: Specified Tag model
            list_display (tuple): The list display of an Tag model is used to 
            instruct the admin site on how to display objects within the admin site 
    """
    model = Tag
    list_display = ("tag",)

    tag_names= ["Java", "C", "Python", "C++", "C#", "Visual Basic .NET",
    "JavaScript", "Swift", "PHP", "SQL", "Go", "Assembly language", "Ruby", "MATLAB",
    "Groovy", "Perl", "Rust", "R", "TypeScript", "Ada", "Lua", "Kotlin", "COBOL",
    "Fortran", "Julia", "Dart", "ABAP", "Shell", "SAS", "PL/SQL", "F#", "Objective-C",
    "Scala", "Pascal", "Apex", "LabVIEW", "D", "Transact-SQL", "Delphi/Object Pascal",
    "VBScript", "Logo", "Prolog", "Scratch", "REXX", "AWK", "Kotlin/Native", "RPG (OS/400)",
    "Swift (iOS)", "Python (Stackless)", "C (Embedded)", "JCL", "Scheme", "Groovy (Android)",
    "Go (Golang)", "Ruby (JRuby)", "Python (MicroPython)", "Lua (LuaJIT)", "Bash",
    "PowerShell", "R (GNU S)", "JavaScript (Emscripten)", "C++ (Embedded)", "Ruby on Rails",
    "COBOL (Micro Focus)", "Fortran (GFortran)", "LabVIEW (G)", "PHP (HHVM)", "SQL (PL/SQL)",
    "Hack (HHVM)", "Julia (JuliaLang)", "TypeScript (Deno)", "Ada (GNAT)", "Kotlin (JVM)",
    "Assembly language (NASM)", "Swift (Server Side)", "Go (GoLand)", "Groovy (Grails)",
    "Perl (ActiveState Perl)", "Rust (Mozilla)", "R (Microsoft R Open)", "TypeScript (TypeScript Node)",
    "Assembly language (WebAssembly)", "Swift (SwiftUI)", "Go (Revel)", "Groovy (Apache Groovy)",
    "Perl (Strawberry Perl)", "Rust (Redox)", "R (RStudio)", "TypeScript (Angular)",
    "Assembly language (ARM)", "Swift (React Native)", "Go (Fuchsia)", "Groovy (GroovyJS)",
    "Perl (Raku)", "Rust (RustOS)", "R (Bioconductor)", "TypeScript (Vue.js)",
    "Assembly language (MIPS)", "Swift (Perfect)", "Go (Android)", "Groovy (Grooscript)",
    "Perl (Perl6)", "Rust (Tock)","Assembly language (x86)" "Swift", "Go" "Groovy",
    "Perl", "Rust","R","TypeScript",]


class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin Definition for managing our O models

        This class extends the `admin.ModelAdmin` class provided by
        Django as a means of providing the builtin admin with the ability
        to modify the Organization table in the Database.

        Attributes:
            model Organization: Specified Organization model
            list_display (tuple): The list display of an Organization model is used to 
            instruct the admin site on how to display objects within the admin site 
    """

    model = Organization
    list_display = ("org_id", "name", "owner_id",)


admin.site.register(Owner, OwnerAdmin)
admin.site.register(CustomAccount, AccountAdminConfig)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomAdmin, AccountAdminConfig)
admin.site.register(CustomAdminPermission, CustomAdminPermissionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Organization, OrganizationAdmin)
