from django.contrib import admin

from .models import (
    Team, TeamPermission,
    Member, Project, PartOf, Repository,
    PullRequest, Issue, Commit, CodeReview,
    Follow, Own
)


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

admin.site.register(Team)
admin.site.register(TeamPermission)
admin.site.register(Member)
admin.site.register(Project)
admin.site.register(PartOf)
admin.site.register(Repository)
admin.site.register(PullRequest)
admin.site.register(Issue)
admin.site.register(Commit)
admin.site.register(CodeReview)
admin.site.register(Follow)
admin.site.register(Own)
