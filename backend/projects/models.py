import uuid
from django.db import models
from users.models import CustomUser

# Create your models here.
class Project(models.Model):
    """
    Project model used by django's built in ORM

    This model defines the fields and parameters that will be defined for
    the projects table

    Attributes:
        id (int): implicitly defined by django models that dont specify a pk (primary key)
        name (str): The text field name for the project (will likely be changed or removed later)
    """
    VISIBILITY = [
        ("PUBLIC", "public"),
        ("PRIVATE", "private"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField()
    visibility = models.CharField(choices=VISIBILITY, default="PRIVATE")
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # check whether this is cascading on user deletion or project deletion. reference Owners in diagram (probably not a User type)

    def __str__(self):
        return self.name
    

class ProjectTags(models.Model):
    """
    Project model used by django's built in ORM

    This model defines the fields and parameters that will be defined for
    the projects table

    Attributes:
        id (int): implicitly defined by django models that dont specify a pk (primary key)
        name (str): The text field name for the project (will likely be changed or removed later)
    """
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag_name = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "tag_name"],
                name="unique_project_tag_key_constraint"
            )
        ]

class Repository(models.Model):
    """
    """
    #TODO: no primary key
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name"],
                name="unique_project_repository_key_constraint"
            )
        ]

class Item(models.Model):
    """
    """
    #TODO: no primary key
    #TODO: test if item id will auto increment
    #TODO: add more status choices if needed
    #TODO: fill in owner id
    #TODO: fill in team name
    STATUS = [
        ("NOTAPPROVED", "notapproved"),
        ("INPROGRESS", "inprogress"),
        ("COMPLETED", "completed"),
    ]
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.ForeignKey(Repository, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    item_name = models.CharField()
    status = models.CharField(choices=STATUS, default="NOTAPPROVED")
    description = models.TextField()
    is_approved = models.BooleanField()
    due_date = 
    owner_id = ""
    team_name = ""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name", "item_id"],
                name="unique_project_repository_item_key_constraint"
            )
        ]

class PullRequest(models.Model):
    """
    """
    #TODO: no primary key
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.ForeignKey(Repository, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    branch_name = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name", "item_id"],
                name="unique_project_repository_item_pull_request_key_constraint"
            )
        ]

class Issue(models.Model):
    """
    """
    #TODO: no primary key
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.ForeignKey(Repository, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    issue_type = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name", "item_id"],
                name="unique_project_repository_item_issue_key_constraint"
            )
        ]

class CodeReview(models.Model):
    """
    """
    #TODO: no primary key
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.ForeignKey(Repository, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name", "item_id"],
                name="unique_project_repository_item_code_review_key_constraint"
            )
        ]

class Commits(models.Model):
    """
    """
    #TODO: no primary key
    #TODO: fill in commit id to be unique within project
    commit_id = ""
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.ForeignKey(Repository, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name", "item_id"],
                name="unique_project_repository_item_pull_commits_constraint"
            )
        ]

class Follows(models.Model):
    """
    """
    #TODO: no primary key
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

        class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "project_id"],
                name="unique_user_project_follows_constraint"
            )
        ]

class Owns(models.Model):
    """
    """
    #TODO: no primary key
    #TODO: fill in owner id
    owner_id = ""
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

        class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner_id", "project_id"],
                name="unique_owner_project_owns_constraint"
            )
        ]