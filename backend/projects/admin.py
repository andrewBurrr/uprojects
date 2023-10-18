from django.contrib import admin

from .models import Project


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin Definition for managing Projects

    This class extends the `admin.ModelAdmin` class provided by
    Django as a means of providing the built in admin with the ability
    to modify the Projects table in the Database.

    Attributes:
        list_display (tuple): The listdisplay of an admin model is used to instruct
        the admin site on how to display objects within the admin site
    """
    list_display = ('id', 'name')


admin.site.register(Project)
