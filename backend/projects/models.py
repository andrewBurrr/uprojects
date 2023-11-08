import uuid
from django.db import models
from django.utils import timezone
from users.models import CustomAdmin, CustomUser, Organization, Owner

# TODO: finish filling in comments for each

# Create your models here.
class BugReport(models.Model):
    """
    """
    bug_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    time_stamp = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)


class Respond(models.Model):
    """
    """
    admin_id = models.ForeignKey(CustomAdmin, on_delete=models.SET_NULL, null=True)
    bug_id = models.ForeignKey(BugReport, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["admin_id", "bug_id"],
                name="unique_admin_bug_respond_constraint"
            )
        ]

class Tag(models.Model):
    """

    This model defines the fields and parameters that will be defined for
    the tag table

    Attributes:
        tag_name (str): The text field containing the tag name.
    """
    tag_name = models.CharField(max_length=60, primary_key=True)


class Collaborator(models.Model):
    """
    TODO: comment
    """
    owner_id = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    team_name = models.CharField(max_length=60)
    tags = models.ManyToManyField(Tag)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner_id", "team_name"],
                name="unique_owner_team_collaborator_constraint"
            )
        ]


# TODO: make note somewhere saying that we changed how permissions for collaborators work
class CollaboratorPermission(models.Model):
    """
    TODO: comment
    """
    PERMISSIONS = [
        ("R", "read"),
        ("W", "write"),
        ("X", "execute")
    ]
    collaborator_id = models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    permission = models.CharField(max_length=1, choices=PERMISSIONS, default="R")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["collaborator_id", "permission"],
                name="unique_collaborator_permission_constraint"
            )
        ]


class Member(models.Model):
    """
    TODO: comment
    """
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    team_name = models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    role = models.CharField(max_length=60)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "owner_id", "team_name"],
                name="unique_user_owner_team_member_constraint"
            )
        ]


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
    name = models.CharField(max_length=60)
    visibility = models.CharField(max_length=60, choices=VISIBILITY, default="PRIVATE")
    description = models.TextField()
    owner_id = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Event(models.Model):
    """
    """
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    event_type = models.CharField(max_length=60)
    start_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField()
    name = models.CharField(max_length=60)
    tags = models.ManyToManyField(Tag)

class Hosts(models.Model):
    """
    """
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event_id", "org_id"],
                name="unique_event_org_host_constraint"
            )
        ]

class ProjectSubmission(models.Model):
    """
    """
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event_id", "owner_id"],
                name="unique_event_owner_project_submission_constraint"
            )
        ]

class FileSubmission(models.Model):
    """
    """
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    #TODO: figure out how to deal with both of these using primary key and not attr we want
    owner_id = models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    team_name = models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    file = models.FileField()
    file_type = models.CharField(20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event_id", "owner_id", "team_name"],
                name="unique_event_owner_name_file_submission_constraint"
            )
        ]

class PartOf(models.Model):
    """
    TODO: comment
    """
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    team_name = models.ForeignKey(Collaborator, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "owner_id", "team_name"],
                name="unique_project_owner_team_partof_constraint"
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
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=60)

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
        description (str): The text field containing this item's description.
        is_approved (bool): The boolean value representing is this item is approved.
        due_date (): default django date format see docs
        owner_id (int): foreign key of the owner of the project this belongs to
        team_name (str): name of the team assigned to this.
    """

    # TODO: test if item id will auto increment
    STATUS = [
        ("NOTAPPROVED", "not approved"),
        ("INPROGRESS", "in progress"),
        ("PENDINGAPPROVAL", "pending approval"),
        ("COMPLETED", "completed"),
    ]
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    repo_name = models.ForeignKey(Repository, on_delete=models.CASCADE)
    item_id = models.IntegerField(default=1)
    item_name = models.CharField(max_length=60)
    status = models.CharField(max_length=60, choices=STATUS, default="NOTAPPROVED")
    description = models.TextField()
    is_approved = models.BooleanField()
    due_date = models.DateField()
    owner_id = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    team_name = models.ForeignKey(Collaborator, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_id = self.objects.all().aggregate(largest=models.Max('item_id'))['largest']
            if last_id is not None:
                self.item_id = last_id + 1
        super(Item, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "repo_name", "item_id"],
                name="unique_project_repository_item_key_constraint"
            )
        ]


class PullRequest(Item):
    """

    This model defines the fields and parameters that will be defined for
    the pull request table

    Attributes:
        branch_name (str): The text field containing the name of this pull request.
    """
    branch_name = models.CharField(max_length=60)


class Issue(Item):
    """

    This model defines the fields and parameters that will be defined for
    the issue table

    Attributes:
        issue_type (str): The text field containing the type of this issue.
    """
    issue_type = models.CharField(max_length=60)  # could this also be a choice?


class Commit(models.Model):
    """

    This model defines the fields and parameters that will be defined for
    the commit table

    Attributes:
        commit_id (str): #TODO: finish
    """
    commit_id = models.CharField(max_length=60)


class CodeReview(Item):
    """

    This model defines the fields and parameters that will be defined for
    the code review table

    Attributes:
        #TODO: fill in
    """
    commits = models.ManyToManyField(Commit)


class Follow(models.Model):
    """

    This model defines the fields and parameters that will be defined for
    the follows table

    Attributes:
        user_id (int): The id of the user that follows this project. Is a foreign key.
        project_id (int): The id of the project this user follows. Is a foreign key.
    """
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "project_id"],
                name="unique_user_project_follow_constraint"
            )
        ]


class Own(models.Model):
    """

    This model defines the fields and parameters that will be defined for
    the owns table

    Attributes:
        owner_id (int): The id of the owner of the project. Is a foreign key.
        project_id (int): The id of the project that is owned by the owner. Is a foreign key.
    """
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner_id", "project_id"],
                name="unique_owner_project_owns_constraint"
            )
        ]
