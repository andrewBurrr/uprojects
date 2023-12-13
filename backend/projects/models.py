import uuid
from django.db import models
from users.models import CustomAdmin, CustomUser, Organization, Owner, Tag
from users.storage import OverwriteStorage
from datetime import date


# Create your models here.
class BugReport(models.Model):
    """
    Model representing a bug report in the system.

    Each bug report has a unique identifier, a timestamp of creation,
    a description of the bug, and is associated with a user.

    Attributes:
        bug_id (UUID): Unique identifier for the bug report.
        time_stamp (DateTimeField): Date and time when the bug report was created (auto-generated).
        description (TextField): Description of the bug.
        Watching for file changes with StatReloader
        user_id (ForeignKey to CustomUser): Foreign key to the user associated with the bug report.

    Methods:
        None
    """
    bug_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_stamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)


class BugResponse(models.Model):
    """
    Model representing a response to a bug report in the system.

    Each response has an administrator associated with it, the bug report it responds to,
    a timestamp of creation, and a comment providing additional information.

    Attributes:
        admin_id (ForeignKey to CustomAdmin): Foreign key to the administrator associated with the response.
        bug_id (ForeignKey to BugReport): Foreign key to the bug report being responded to.
        time_stamp (DateTimeField): Date and time when the response was created (auto-updated).
        comment (TextField): Comment providing additional information about the response.

    Meta:
        constraints (list): List of constraints applied to the model.
            - UniqueConstraint: Ensures the combination of admin, bug report, and timestamp is unique.

    Methods:
        None
    """
    admin_id = models.ForeignKey(CustomAdmin, on_delete=models.SET_NULL, null=True)
    bug_id = models.ForeignKey(BugReport, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now=True)
    comment = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["admin_id", "bug_id", "time_stamp"],
                name="unique_admin_bug_respond_constraint"
            )
        ]


class Team(models.Model):
    """
    Model representing a team in the system.

    Each team has an owner, a team name, and can be associated with tags.

    Attributes:
        owner_id (ForeignKey to Owner): Foreign key to the owner associated with the team.
        team_name (CharField): Name of the team.
        tags (ManyToManyField to Tag): Many-to-many relationship with tags associated with the team.

    Meta:
        constraints (list): List of constraints applied to the model.
            - UniqueConstraint: Ensures the combination of owner and team name is unique.

    Methods:
        None
    """
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
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
    Model representing a member's association with a team in the system.

    Each member is associated with a user, a team, and has a specific role within the team.

    Attributes:
        user_id (ForeignKey to CustomUser): Foreign key to the user associated with the member.
        team (ForeignKey to Team): Foreign key to the team associated with the member.
        role (CharField): Role of the member within the team.

    Meta:
        constraints (list): List of constraints applied to the model.
            - UniqueConstraint: Ensures the combination of user and team is unique.

    Methods:
        None
    """
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)  # let's assume it only retrieves unique pairs from collaborator.
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
        project_id (int): implicitly defined by django models that dont specify a pk (primary key)
        name (str): The text field name for the project (will likely be changed or removed later)
        visibility (str): The text field containing the projects visibility.
        description (str): The text field containing the projects description.
        owner_id (int): The id of the owner of the project. Is a foreign key.
        tags (ManyToManyField to Tag): Many-to-many relationship with tags associated with the project.

    Methods:
        __str__: Returns a string representation of the project based on its name.
    """
    VISIBILITY = [
        ("PUBLIC", "public"),
        ("PRIVATE", "private"),
    ]
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60)
    visibility = models.CharField(max_length=60, choices=VISIBILITY, default="PRIVATE")
    description = models.TextField()
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Model representing an event in the system.

    Each event has a unique identifier, is hosted by an organization,
    has an event type, start and end dates, a name, and can be associated with tags.

    Attributes:
        id (UUID): Unique identifier for the event.
        organization (ForeignKey to Organization): Foreign key to the organization hosting the event.
        event_type (CharField): Type or category of the event.
        start_date (DateTimeField): Date and time when the event starts.
        end_date (DateTimeField): Date and time when the event ends.
        name (CharField): Name of the event.
        tags (ManyToManyField to Tag): Many-to-many relationship with tags associated with the event.

    Methods:
        None
    """
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)  # events need to be hosted by an organization
    event_type = models.CharField(max_length=60)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=60)
    tags = models.ManyToManyField(Tag)


class Hosts(models.Model):
    """
    Model representing the hosting relationship between events and organizations in the system.

    Each entry in this model signifies that an organization hosts a specific event.

    Attributes:
        event_id (ForeignKey to Event): Foreign key to the event being hosted.
        org_id (ForeignKey to Organization): Foreign key to the organization hosting the event.

    Meta:
        constraints (list): List of constraints applied to the model.
            - UniqueConstraint: Ensures that a specific organization hosts a specific event only once.

    Methods:
        None
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
    """
    Model representing a submission to a Dropbox for a specific event and team in the system.

    Each entry in this model signifies a submission made by a team for a specific event.

    Attributes:
        event_id (ForeignKey to Event): Foreign key to the event associated with the submission.
        team (ForeignKey to Team): Foreign key to the team making the submission.
        comment (TextField): Additional comments or information related to the submission (optional).
        submission_date (DateTimeField): Date and time when the submission was made (auto-generated).

    Meta:
        constraints (list): List of constraints applied to the model.
            - UniqueConstraint: Ensures that a specific team can make a submission for a specific event only once.

    Methods:
        None
    """
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
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
    """
    Model representing a file associated with a submission in the system.

    Each entry in this model signifies a file uploaded as part of a submission.

    Attributes:
        submission (ForeignKey to DropboxSubmission): Foreign key to the submission associated with the file.
        file (FileField): Field to store the uploaded file.
            - The files are stored in the "submission/files/" directory using OverwriteStorage.

    Methods:
        None
    """
    submission = models.ForeignKey(DropboxSubmission, on_delete=models.CASCADE)  # trusting django magic
    file = models.FileField(upload_to="submission/files/", storage=OverwriteStorage(), blank=True)


class PartOf(models.Model):
    """
    Model representing the relationship between a project and a team in the system.

    Each entry in this model signifies that a team is part of a specific project.

    Attributes:
        project_id (ForeignKey to Project): Foreign key to the project the team is part of.
        team (ForeignKey to Team): Foreign key to the team that is part of the project.

    Meta:
        constraints (list): List of constraints applied to the model.
            - UniqueConstraint: Ensures that a specific team is part of a specific project only once.

    Methods:
        None
    """
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
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
    the repository table. Each repository is associated with a specific project and has a unique identifier,
    a name, and a Git base path.

    Attributes:
        project_id (int): The id of the project this repository belongs to. Is a foreign key.
        repo_name (str): The text field containing the name of this repository.
        git_base_path (CharField): Path to the repository in Git (unique).

    Meta:
        constraints (list): List of constraints applied to the model.
            - UniqueConstraint: Ensures that a specific project has a repository with a unique name.

    Methods:
        None
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
        repo (ForeignKey to Repository): Foreign key to the repository this item belongs to.
        item_id (IntegerField): Unique identifier for the item (auto-incremented by default).
        item_name (CharField): Name of the item.
        status (CharField): Status of the item (chosen from predefined choices).
        description (TextField): Description of the item.
        is_approved (BooleanField): Approval status of the item.
        due_date (DateField): Due date for the item.
        team (ForeignKey to Team): Foreign key to the team assigned to this item.

    """

    # TODO: test if item id will auto increment
    STATUS = [
        ("NOTAPPROVED", "not approved"),
        ("INPROGRESS", "in progress"),
        ("PENDINGAPPROVAL", "pending approval"),
        ("COMPLETED", "completed"),
    ]
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)  # django magic
    item_id = models.IntegerField(default=1)
    item_name = models.CharField(max_length=60)
    status = models.CharField(max_length=60, choices=STATUS, default="NOTAPPROVED")
    description = models.TextField(default="")
    is_approved = models.BooleanField()
    due_date = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)  # django magic

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_id = self.objects.all().aggregate(largest=models.Max('item_id'))['largest']
            if last_id is not None:
                self.item_id = last_id + 1
        super(Item, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["repo", "item_id"],
                name="%(class)s_unique_project_repository_item_key_constraint"
            )
        ]
        abstract = True


class PullRequest(Item):
    """

    This model defines the fields and parameters that will be defined for
    the pull request table

    Attributes:
        branch_name (CharField): The text field containing the name of this pull request.
    """
    branch_name = models.CharField(max_length=60)


class Issue(Item):
    """

    This model defines the fields and parameters that will be defined for
    the issue table

    Attributes:
        issue_type (CharField): The text field containing the type of this issue.

    """
    issue_type = models.CharField(max_length=60)  # could this also be a choice?


class Commit(models.Model):
    """
    Model representing a commit in the system.

    Each commit is an extension of the Item model and inherits its attributes.
    Additionally, it has a commit_id associated with it.

    Attributes:
        commit_id (CharField): Identifier for the commit.

    """
    commit_id = models.CharField(max_length=60)


class CodeReview(Item):
    """
    Model representing a code review in the system.

    Each code review is an extension of the Item model and inherits its attributes.
    Additionally, it has a relationship with multiple commits.

    Attributes:
        commits (ManyToManyField to Commit): Relationship with multiple commits associated with the code review.

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
