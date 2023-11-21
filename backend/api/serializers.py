from rest_framework import serializers
from projects.models import ( Project, Tag, Collaborator)
from users.models import CustomUser, Interest, Organization


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

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('interest')


class UserSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_image', 'start_date', 'interests']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag')


class ProjectSerializer(serializers.ModelSerializer):
    """
        Serializer for the Project model.
        TODO update serializer and model schema to match data requirements
        TODO How are project tags handled by this serializer? Should we consider creating a Project tag serializer?

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
        fields = ('id', 'name', 'visibility', 'description', 'owner_id', 'tags')


class CollaboratorSerializer(serializers.ModelSerializer):
    """
    Serializer for the users/models.Collaborator model.

    Necessary Collaborator fields:
    - owner_id : users/model.Owner
    - team_name
    - tags: users/model.Tag
    """
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Collaborator
        fields = ('owner_id', 'team_name', 'tags')


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
        fields = ('org_id', 'logo', 'name', 'description', 'owner_id', 'tags')


# class ProjectDetailSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Project
#         fields = ('id', 'name', 'visibility', 'description', 'owner_id', 'tags')
#
#
# class RepositorySerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Repository
#         fields = ('repo_name',)
#
#
# class ItemSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Item
#         fields = ('item_id', 'item_name', 'status', 'owner_id')
#
#
# class ItemDetailSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Item
#         fields = ('project_id', 'repo_name', 'item_id', 'item_name', 'status', 'description', 'is_approved', 'due_date',
#                   'owner_id', 'team_name')
#
#
# class PullRequestSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = PullRequest
#         fields = ('id', 'branch_name')
#
#
# class PullRequestDetailSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     # TODO: have it list the item details for it too
#     class Meta:
#         model = PullRequest
#         fields = ('id', 'branch_name')
#
#
# class IssueSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Issue
#         fields = ('id', 'issue_type')
#
#
# class IssueDetailSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     # TODO: have it list the item details for it too
#     class Meta:
#         model = Issue
#         fields = ('id', 'issue_type')
#
#
# # NOTE TO READERS: I (david) think that commits could also use a name even if not used as PK (for human readability)
# class CommitSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Commit
#         fields = ('id', 'commit_id')
#
#
# class CommitDetailSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     # TODO: have it list the item details for it too
#     class Meta:
#         model = Commit
#         fields = ('id', 'commit_id')
#
#
# # NOTE TO READERS: I (david) think that code reviews could use a name even if not used as PK (for human readability)
# class CodeReviewSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = CodeReview
#         fields = ('id', 'commits')
#
#
# class CodeReviewDetailSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     # TODO: have it list the item details for it too
#     class Meta:
#         model = CodeReview
#         fields = ('id', 'commits')
#
#
# class TagSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Tag
#         fields = ('tag_name',)
#
#
# class OwnerOfCollaboratorSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     # TODO: tags?
#     class Meta:
#         model = Collaborator
#         fields = ('team_name',)
#
#
# class CollaboratorSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Collaborator
#         fields = ('team_name', 'owner_id', 'tags')
#
#
# class CollaboratorPermissionSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = CollaboratorPermission
#         fields = ('permission',)
#
#
# class UserIsMemberOfSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Member
#         fields = ('team_name', 'owner_id', 'role')
#
#
# class MemberUserSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Member
#         fields = ('user_id', 'role')
#
#
# class MemberDetailSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Member
#         fields = ('role',)
#
#
# class PartOfProjectSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = PartOf
#         fields = ('team_name',)
#
#
# class PartOfTeamSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = PartOf
#         fields = ('project_id', 'owner_id')
#
#
# class FollowSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Follow
#         fields = ('project_id',)
#
#
# class FollowerSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Follow
#         fields = ('user_id',)
#
#
# class OwnDetailSerializer(serializers.ModelSerializer):
#     """
#     """
#
#     class Meta:
#         model = Own
#         fields = ('owner_id',)
