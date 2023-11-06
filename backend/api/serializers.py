from rest_framework import serializers
from projects.models import (Project, Repository, Item, PullRequest, Issue, Commit,
                             CodeReview, Tag, Collaborator, CollaboratorPermission, Member, PartOf)


class ProjectSerializer(serializers.ModelSerializer):
    """
        Serializer for the Project model.
        TODO update serializer and model schema to match data requirements

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
    class Meta:
        model = Project
        fields = ('id', 'name')

class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Project
        fields = ('id', 'name', 'visibility', 'description', 'owner_id', 'tags')

class RepositorySerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Repository
        fields = ('repo_name',)

class ItemSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Item
        fields = ('item_id', 'item_name', 'status', 'owner_id')

class ItemDetailSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Item
        fields = ('project_id', 'repo_name', 'item_id', 'item_name', 'status', 'description', 'is_approved', 'due_date', 'owner_id', 'team_name')

class PullRequestSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = PullRequest
        fields = ('id', 'branch_name')

class PullRequestDetailSerializer(serializers.ModelSerializer):
    """
    """
    #TODO: have it list the item details for it too
    class Meta:
        model = PullRequest
        fields = ('id', 'branch_name')

class IssueSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Issue
        fields = ('id', 'issue_type')

class IssueDetailSerializer(serializers.ModelSerializer):
    """
    """
    #TODO: have it list the item details for it too
    class Meta:
        model = Issue
        fields = ('id', 'issue_type')

#NOTE TO READERS: I (david) think that commits could also use a name even if not used as PK (for human readability)
class CommitSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Commit
        fields = ('id', 'commit_id')

class CommitDetailSerializer(serializers.ModelSerializer):
    """
    """
    #TODO: have it list the item details for it too
    class Meta:
        model = Commit
        fields = ('id', 'commit_id')

#NOTE TO READERS: I (david) think that code reviews could use a name even if not used as PK (for human readability)
class CodeReviewSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = CodeReview
        fields = ('id', 'commits')

class CodeReviewDetailSerializer(serializers.ModelSerializer):
    """
    """
    #TODO: have it list the item details for it too
    class Meta:
        model = CodeReview
        fields = ('id', 'commits')

class TagSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Tag
        fields = ('tag_name',)

class OwnerOfCollaboratorSerializer(serializers.ModelSerializer):
    """
    """
    #TODO: tags?
    class Meta:
        model = Collaborator
        fields = ('team_name',)

class CollaboratorSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Collaborator
        fields = ('team_name', 'owner_id', 'tags')

class CollaboratorPermissionSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = CollaboratorPermission
        fields = ('permission',)

class UserIsMemberOfSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Member
        fields = ('team_name', 'owner_id', 'role')

class MemberUserSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Member
        fields = ('user_id', 'role')

class MemberDetailSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = Member
        fields = ('role', )

class PartOfProjectSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = PartOf
        fields = ('team_name', )

class PartOfTeamSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = PartOf
        fields = ('project_id', 'owner_id')

