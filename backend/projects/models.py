import uuid
from django.db import models
from django.utils import timezone
from users.models import CustomAdmin, CustomUser, Organization, Owner, Tag #, image_to_path
from users.storage import OverwriteStorage

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
    time_stamp = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    time_stamp = models.DateTimeField(default=timezone.now)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["admin_id", "bug_id", "time_stamp"],
                name="unique_admin_bug_respond_constraint"
            )
        ]



class Team(models.Model):
    """
    TODO: comment, verify unique constraint actually works
    """
    owner_id = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    team_name = models.CharField(max_length=60)
    tags = models.ManyToManyField(Tag)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner_id", "team_name"],
                name="unique_owner_team_constraint"
            )
        ]




# TODO: make note somewhere saying that we changed how permissions for Teams work
class TeamPermission(models.Model):
    """
    TODO: comment
    """
    PERMISSIONS = [
        ("R", "read"),
        ("W", "write"),
        ("X", "execute")
    ]
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    permission = models.CharField(max_length=1, choices=PERMISSIONS, default="R")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["team_id", "permission"],
                name="unique_team_permission_constraint"
            )
        ]


class Member(models.Model):
    """
    TODO: comment, if unique constraint causes issues try team.etc
    """
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #team = models.ForeignKey(Team, on_delete=models.CASCADE, to_fields=['owner_id', 'team_name'])
    team = models.ForeignKey(Team, on_delete=models.CASCADE) # let's assume it only retrieves unique pairs from collaborator.
    role = models.CharField(max_length=60)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "team"],
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
        description (str): The text field containing the projects description.
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
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name




class Event(models.Model):
    """
    """
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)  # events need to be hosted by an organization
    event_type = models.CharField(max_length=60)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
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


class DropboxSubmission(models.Model):
    # TODO verify unique constraint is unique
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    #collaborator = models.ForeignKey(Team, on_delete=models.CASCADE, to_fields=['owner_id', 'team_name'])
    team = models.ForeignKey(Team, on_delete=models.CASCADE) # let's assume it only retrieves unique pairs from collaborator.
    comment = models.TextField(blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event_id", "team"],
                name="unique_event_owner_team_dropbox_submission_constraint"
            )
        ]



class SubmissionFile(models.Model):
    #submission = models.ForeignKey(DropboxSubmission, on_delete=models.CASCADE, to_fields=['event_id', 'collaborator'])
    submission = models.ForeignKey(DropboxSubmission, on_delete=models.CASCADE) # trusting django magic
    #file = models.FileField(upload_to=lambda instance, filename: image_to_path(instance, filename, "submission_file"), storage=OverwriteStorage(), blank=True)  # TODO figure out file paths
    file = models.FileField(upload_to="submission/files/",storage=OverwriteStorage(), blank=True)


class PartOf(models.Model):
    """
        # TODO verify unique constraint is unique

    """
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    #team = models.ForeignKey(Team, on_delete=models.CASCADE, to_fields=['owner_id', 'team_name'])
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "team"],
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
    git_base_path = models.CharField(max_length=255, unique=True)

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
    #repository = models.ForeignKey(Repository, on_delete=models.CASCADE, to_fields=['project_id', 'repo_name'])
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE) # django magic
    item_id = models.IntegerField(default=1)
    item_name = models.CharField(max_length=60)
    status = models.CharField(max_length=60, choices=STATUS, default="NOTAPPROVED")
    description = models.TextField()
    is_approved = models.BooleanField()
    due_date = models.DateField()

    #team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, to_fields=['owner_id', 'team_name'])
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True) #django magic

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_id = self.objects.all().aggregate(largest=models.Max('item_id'))['largest']
            if last_id is not None:
                self.item_id = last_id + 1
        super(Item, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["repository", "item_id"],
                name="%(class)s_unique_project_repository_item_key_constraint"
            )
        ]
        abstract = True


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


class Commit(Item):
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

