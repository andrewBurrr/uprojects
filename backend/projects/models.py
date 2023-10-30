import uuid
from django.db import models
from users.models import CustomUser

#TODO: finish filling in comments for each

# Create your models here.
class Project(models.Model):
    """
    Project model used by django's built in ORM

    This model defines the fields and parameters that will be defined for
    the projects table

    Attributes:
        id (int): implicitly defined by django models that dont specify a pk (primary key)
        name (str): The text field name for the project (will likely be changed or removed later)
        visibility (str): The text field containing the projects visibility.
        description (str): The text field containing the projects descritiption.
        owner_id (int): The id of the owner of the project. Is a foreign key.
    """
    VISIBILITY = [
        ("PUBLIC", "public"),
        ("PRIVATE", "private"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField()
    visibility = models.CharField(choices=VISIBILITY, default="PRIVATE")
    description = models.TextField()
    #TODO: fill in owner id
    owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # check whether this is cascading on user deletion or project deletion. reference Owners in diagram (probably not a User type)

    def __str__(self):
        return self.name
    

class ProjectTags(models.Model):
    """

    This model defines the fields and parameters that will be defined for
    the project tags table

    Attributes:
        project_id (int): The id of the project this tag belong to. Is a foreign key.
        tag_name (str): The text field containing the tag name.
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

    This model defines the fields and parameters that will be defined for
    the repository table

    Attributes:
        project_id (int): The id of the project this repository belongs to. Is a foreign key.
        repo_name (str): The text field containing the name of this repository.
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

    This model defines the fields and parameters that will be defined for
    the item table

    Attributes:
        project_id (int): The id of the project this item belongs to. Is a foreign key.
        repo_name (str): The name of the repository this item belongs to. It is a foreign key.
        item_id (int): The id of this item.
        item_name (str): The text field containing the name of this item.
        status (str): The text field containing the status of this item.
        description (str): The text field containing this item's descritiption.
        is_approved (bool): The boolean value representing is this item is approved.
        due_date (): #TODO: what format is date in by defualt?
        owner_id (int):
        team_name (str):
    """
    #TODO: no primary key
    #TODO: test if item id will auto increment
    #TODO: add more status choices if needed
    #TODO: fill in owner id
    #TODO: fill in team name
    STATUS = [
        ("NOTAPPROVED", "notapproved"),
        ("INPROGRESS", "inprogress"),
        ("PENDINGAPPROVAL", "pendingapproval")
        ("COMPLETED", "completed"),
    ]
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.ForeignKey(Repository, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    item_name = models.CharField()
    status = models.CharField(choices=STATUS, default="NOTAPPROVED")
    description = models.TextField()
    is_approved = models.BooleanField()
    due_date = models.DateField()
    owner_id = ""       # Do we set this to null if owner gets deleted?
    team_name = ""      # Same as above? The primary key is technically (project_id, repo_name)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name", "item_id"],
                name="unique_project_repository_item_key_constraint"
            )
        ]

class PullRequest(models.Model):
    """

    This model defines the fields and parameters that will be defined for
    the pull request table

    Attributes:
        project_id (int): The id of the project this pull request refers to. Is a foreign key.
        repo_name (str): The name of the repository this pull request refers to. It is a foreign key.
        item_id (int): The id of the item this pull request belongs to. Is a foreign key.
        branch_name (str): The text field containing the name of this pull request.
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

    This model defines the fields and parameters that will be defined for
    the issue table

    Attributes:
        project_id (int): The id of the project this issue refers to. Is a foreign key.
        repo_name (str): The name of the repository this issue refers to. It is a foreign key.
        item_id (int): The id of the item this issue belongs to. Is a foreign key.
        issue_type (str): The text field containing the type of this issue.
    """
    #TODO: no primary key
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.ForeignKey(Repository, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    issue_type = models.CharField() #could this also be a choice?

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name", "item_id"],
                name="unique_project_repository_item_issue_key_constraint"
            )
        ]

class CodeReview(models.Model):
    """

        This model defines the fields and parameters that will be defined for
        the code review table

    Attributes:
        project_id (int): The id of the project this code review refers to. Is a foreign key.
        repo_name (str): The name of the repository this code review refers to. It is a foreign key.
        item_id (int): The id of the item this code review belongs to. Is a foreign key.
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

    This model defines the fields and parameters that will be defined for
    the commits table

    Attributes:
        commit_id ():
        project_id (int): The id of the project this commit refers to. Is a foreign key.
        repo_name (str): The name of the repository this commit refers to. It is a foreign key.
        item_id (int): The id of the item this commit belongs to. Is a foreign key.
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

    This model defines the fields and parameters that will be defined for
    the follows table

    Attributes:
        user_id (int): The id of the user that follows this project. Is a foreign key.
        project_id (int): The id of the project this user follows. Is a foreign key.
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

    This model defines the fields and parameters that will be defined for
    the owns table

    Attributes:
        owner_id (): The id of the owner of the project. #TODO: finish this comment
        project_id (int): The id of the project that is owned by the owner. Is a foreign key.
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