from rest_framework import serializers
from projects.models import (Project, Team, Follow, Event, Item,
                             Issue, PullRequest, CodeReview, Commit, Repository,
                             Member, DropboxSubmission, SubmissionFile, BugReport)
from users.models import CustomUser, Tag, Organization


"""
What do serializers do? 
Converts a model's data to JSON/XML format.

There are two types of serializers commonly used: 
- ModelSerializers and HyperLinkedModelSerializer.

We are using Django's ModelSerializer serializers for our application.
- It automatically generates a set of fields based on the model.
- generates validators for the serializer such as unique_together validators
- it includes simple default implementations of .create() and .update
    (info from: https://www.geeksforgeeks.org/serializers-django-rest-framework/)

"""


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag',]


class UserSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    # TODO: We need to figure out how to update a users tag via a django method.

    # TODO: Should id be something that we present to the front end?
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_image', 'about', 'start_date', 'tags']


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.
    TODO update serializer and model schema to match data requirements
    TODO Figure out how updating, adding and removing project tags works.

    This serializer is used to convert Project model instances to JSON
    representations and vice versa. It specifies the fields to include
    in the serialized output.

    Attributes:
        id (int): The unique identifier for the project.
        name (str): The name of the project.

    Note:
        This serializer is used in conjunction with views to provide a
        RESTful API for managing Project instances.
        """
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'visibility', 'description', 'owner_id', 'tags']


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the users/models.Team model.

    Necessary Team fields:
    - owner_id : users/model.Owner
    - team_name
    - tags: users/model.Tag
    """
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Team
        fields = ['owner_id', 'team_name', 'tags']

    # TODO: create owner_id with creation of Organization.
class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for the users/models.Organization model

    Necessary Organization fields:
    - org_id
    - logo
    - name 
    - description
    - owner_id: users/models.Owner
    - tags: Tag
    """
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Organization
        fields = ['org_id', 'logo', 'name', 'description', 'owner_id', 'tags']


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['user_id', 'project_id']


class EventSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = ['event_id', 'event_type', 'start_date', 'end_date', 'name', 'tags']

# TODO: This doesn't work. Will will handle querries in views.
# class BaseSearchSerializer(serializers.ModelSerializer):
#     query = serializers.CharField(required=False, allow_blank=True)
#     tags = serializers.ListField(child=serializers.CharField(), required=False)
    
#     class meta:
#         model = Tag

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['project_id', 'repo_name', 'git_base_path']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['project_id', 'repo_name', 'item_id', 'item_name', 'status',
                  'description', 'is_approved', 'due_date', 'owner_id', 'team_name']


class IssueSerializer(ItemSerializer):
    model = Issue
    fields = ItemSerializer.Meta.fields + ['issue_type',]


class PullRequestSerializer(ItemSerializer):
    model = PullRequest
    fields = ItemSerializer.Meta.fields + ['branch_name',]


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ['id', 'commit_id']


class CodeReviewSerializer(serializers.ModelSerializer):
    commits = CommitSerializer(many=True, read_only=True)

    class Meta:
        model = CodeReview
        fields = ItemSerializer.Meta.fields + ['commits',]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['user_id', 'owner_id', 'team_name', 'role']


class DropboxSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropboxSubmission
        fields = ['event_id', 'team', 'comment', 'submission_date']


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ['submission', 'file']


class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = ['bug_id', 'time_stamp', 'description', 'user_id']

