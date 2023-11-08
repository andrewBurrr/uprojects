from rest_framework import generics
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, ProjectSerializer, CollaboratorSerializer, OrganizationSerializer
from users.models import CustomUser, Organization
from projects.models import Project, Collaborator, Member


class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = generics.get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Obtain the raw SQL statement
        raw_sql = str(self.queryset.query)

        # Log the SQL statement
        print(raw_sql)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.filter(visibility="public")
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'owner_id'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Obtain the raw SQL statement
        raw_sql = str(queryset.query)

        # Log the SQL statement
        print(raw_sql)

        return super(UserProjectList, self).list(request, *args, **kwargs)


class UserTeamsList(generics.ListCreateAPIView):
    serializer_class = CollaboratorSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        teams = Member.objects.filter(user_id=user_id).values('team_name', 'owner_id')
        return Collaborator.objects.filter(team_name__in=teams.values('team_name'), owner_id__in=teams.values('owner_id'))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Obtain the raw SQL statement
        raw_sql = str(queryset.query)

        # Log the SQL statement
        print(raw_sql)

        return super(UserTeamsList, self).list(request, *args, **kwargs)


class UserOrganizationList(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['owner_id']
        return Organization.objects.filter(owner_id=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Obtain the raw SQL statement
        raw_sql = str(queryset.query)

        # Log the SQL statement
        print(raw_sql)

        return super(UserOrganizationList, self).list(request, *args, **kwargs)

# from projects.models import (Project, Repository, Item, PullRequest, Issue, Commit,
#                              CodeReview, Tag, Collaborator, CollaboratorPermission, Member, PartOf, Follow, Own)
# from .serializers import (ProjectSerializer, ProjectDetailSerializer, RepositorySerializer,
#                           ItemSerializer, ItemDetailSerializer, PullRequestSerializer, PullRequestDetailSerializer,
#                           IssueSerializer, IssueDetailSerializer, CommitSerializer, CommitDetailSerializer,
#                           CodeReviewSerializer, CodeReviewDetailSerializer, TagSerializer,
#                           OwnerOfCollaboratorSerializer, CollaboratorSerializer, CollaboratorPermissionSerializer,
#                           UserIsMemberOfSerializer, MemberUserSerializer, MemberDetailSerializer,
#                           PartOfProjectSerializer, PartOfTeamSerializer,
#                           FollowSerializer, FollowerSerializer,
#                           OwnDetailSerializer)
# from rest_framework import generics
#
#
# class ProjectList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating projects.
#
#     Attributes:
#         queryset (QuerySet): The queryset of Project instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Project instances.
#
#     Example Usage:
#         To list all projects, make a GET request to the endpoint associated with
#         this view.
#
#         To create a new project, make a POST request to the same endpoint with
#         the project data in the request body.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#
# class PublicProjectList(generics.ListAPIView):
#     """
#     API view for listing public projects.
#
#     Attributes:
#         TODO properly fetch by visibility
#         queryset (QuerySet): The queryset of Project instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Project instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#
# class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     API view for retrieving and updating projects.
#
#     Attributes:
#         TODO properly fetch by id
#         queryset (QuerySet): The queryset of Project instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Project instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Project.objects.all()
#     serializer_class = ProjectDetailSerializer
#
# class RepositoryList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating repositories.
#
#     Attributes:
#         TODO properly fetch by project_id
#         queryset (QuerySet): The queryset of Repository instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Repository instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Repository.objects.all()
#     serializer_class = RepositorySerializer
#
# class RepositoryDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     """
#     #TODO: one repository by project id, repo name
#         #the idea for this is to delete one repo
#     queryset = Repository.objects.all()
#     serializer_class = RepositorySerializer
#
# #NOTE need?
# class ItemProjectList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating items for a project.
#
#     Attributes:
#         TODO properly fetch by project_id
#         queryset (QuerySet): The queryset of Item instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Item instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#
# class ItemRepositoryList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating items for a repository.
#
#     Attributes:
#         TODO properly fetch by project_id and repository_name
#         queryset (QuerySet): The queryset of Item instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Item instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#
# class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     """
#     #TODO: specific item by project id, repo name, item id
#     queryset = Item.objects.all()
#     serializer_class = ItemDetailSerializer
#
# #NOTE need?
# class PullRequestProjectList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating pull requests for a project.
#
#     Attributes:
#         TODO properly fetch by project_id
#         queryset (QuerySet): The queryset of PullRequest instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing PullRequest instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = PullRequest.objects.all()
#     serializer_class = PullRequestSerializer
#
# class PullRequestRepositoryList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating pull requests for a repository.
#
#     Attributes:
#         TODO properly fetch by project_id and repository_name
#         queryset (QuerySet): The queryset of PullRequest instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing PullRequest instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = PullRequest.objects.all()
#     serializer_class = PullRequestSerializer
#
# class PullRequestDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     """
#     #TODO: single pull request given project id, repo name, item id
#     queryset = PullRequest.objects.all()
#     serializer_class = PullRequestDetailSerializer
#
# #NOTE need?
# class IssueProjectList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating issues for a project.
#
#     Attributes:
#         TODO properly fetch by project_id
#         queryset (QuerySet): The queryset of Issue instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Issue instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Issue.objects.all()
#     serializer_class = IssueSerializer
#
# class IssueRepositoryList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating issues for a repository.
#
#     Attributes:
#         TODO properly fetch by project_id and repository_name
#         queryset (QuerySet): The queryset of Issue instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Issue instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Issue.objects.all()
#     serializer_class = IssueSerializer
#
# class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     """
#     #TODO: single issue given project id, repo name, item id
#     queryset = Issue.objects.all()
#     serializer_class = IssueDetailSerializer
#
# #NOTE DIDNT INCLUDE ALL COMMITS FOR PROJECT
# class CommitRepositoryList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating commits for a repository.
#
#     Attributes:
#         TODO properly fetch by project_id and repository_name
#         queryset (QuerySet): The queryset of Commit instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Commit instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Commit.objects.all()
#     serializer_class = CommitSerializer
#
# class CommitDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     """
#     #TODO: single commit given project id, repo name, item id
#     queryset = Commit.objects.all()
#     serializer_class = CommitDetailSerializer
#
# #NOTE need?
# class CodeReviewProjectList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating code reviews for a project.
#
#     Attributes:
#         TODO properly fetch by project_id
#         queryset (QuerySet): The queryset of CodeReview instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing CodeReview instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = CodeReview.objects.all()
#     serializer_class = CodeReviewSerializer
#
# class CodeReviewRepositoryList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating code reviews for a repository.
#
#     Attributes:
#         TODO properly fetch by project_id and repository_name
#         queryset (QuerySet): The queryset of CodeReview instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing CodeReview instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = CodeReview.objects.all()
#     serializer_class = CodeReviewSerializer
#
# class CodeReviewDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     """
#     #TODO: single code reviews given project id, repo name, item id
#     queryset = CodeReview.objects.all()
#     serializer_class = CodeReviewDetailSerializer
#
# #NOTE not sure if this is the way to do it, but so that when tags are added to anything, if it didn't exist before, its added. if it existed before, it is matched (case insensitive)
# class TagList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating tags.
#
#     Attributes:
#         queryset (QuerySet): The queryset of Tag instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Tag instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#
# class OwnerOfCollaboratorList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating teams that an owner is an owner of.
#
#     Attributes:
#         TODO properly fetch by owner_id
#         queryset (QuerySet): The queryset of Collaborator instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Collaborator instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Collaborator.objects.all()
#     serializer_class = OwnerOfCollaboratorSerializer
#
# #NOTE since we still have team tags for searching, i (david) propose adding a visibility field to collaborators
# class CollaboratorList(generics.ListCreateAPIView):
#     """
#     """
#     #TODO: filter by tags and or owner searched for (and publicity?)
#     queryset = Collaborator.objects.all()
#     serializer_class = CollaboratorSerializer
#
# class CollaboratorPemissionList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating permissions for a team.
#
#     Attributes:
#         TODO properly fetch by collaborator_id
#         queryset (QuerySet): The queryset of CollaboratorPermission instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing CollaboratorPermission instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = CollaboratorPermission.objects.all()
#     serializer_class = CollaboratorPermissionSerializer
#
# #NOTE purely to delete permissions
# class CollaboratorPemissionDetail(generics.DestroyAPIView):
#     """
#     """
#     #TODO: filter by collaborator and permission
#     queryset = CollaboratorPermission.objects.all()
#     serializer_class = CollaboratorPermissionSerializer
#
# class UserIsMemberOfList(generics.ListCreateAPIView):
#     """
#     """
#     #TODO: filter by user id
#         #gets all teams a user is a member of
#     queryset = CollaboratorPermission.objects.all()
#     serializer_class = UserIsMemberOfSerializer
#
# class MemberList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating members of a team.
#
#     Attributes:
#         TODO properly fetch by owner_id and team_name
#         TODO maybe get more info about users?
#         queryset (QuerySet): The queryset of Member instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Member instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = CollaboratorPermission.objects.all()
#     serializer_class = MemberUserSerializer
#
# #NOTE purely to delete members from team
# class MemberInfo(generics.RetrieveDestroyAPIView):
#     """
#     """
#     #TODO: filter by owner id, team name, and user id
#         #maybe give some of user info too?
#     queryset = Member.objects.all()
#     serializer_class = MemberDetailSerializer
#
# #NOTE need class to delete a team from a users list
#
# class PartOfProjectList(generics.ListCreateAPIView):
#     """
#     API view for listing and adding teams to a project.
#
#     Attributes:
#         TODO properly fetch by project_id
#         queryset (QuerySet): The queryset of PartOf instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing PartOf instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = PartOf.objects.all()
#     serializer_class = PartOfProjectSerializer
#
# class PartOfTeamList(generics.ListCreateAPIView):
#     """
#     API view for listing and adding projects to a team.
#
#     Attributes:
#         TODO properly fetch by team_name
#             FIXME TEAM NAMES ARENT UNIQUE, THEY NEED AN OWNER AND THE OWNER
#                     IN THIS RELATIONSHIP IS THE OWNER OF THE PROJECT
#         TODO maybe get more info from collaborators?
#         queryset (QuerySet): The queryset of PartOf instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing PartOf instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = PartOf.objects.all()
#     serializer_class = PartOfTeamSerializer
#
# class PartOfProjectDetail(generics.RetrieveDestroyAPIView):
#     """
#     """
#     #TODO: filter by team_name
#         #maybe get more info from collaborators?
#     queryset = PartOf.objects.all()
#     serializer_class = PartOfTeamSerializer
#
# class FollowList(generics.ListCreateAPIView):
#     """
#     """
#     #TODO: filter by user id
#         #maybe get more info from project (name...)
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer
#
# class FolowDetail(generics.RetrieveDestroyAPIView):
#     """
#     """
#     #TODO: filter by user id and project id
#         #get more info from projects (most of it?)?
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer
#
# #NOTE when a project is changed from public to pricate how delete all followers?
# class FolowersList(generics.ListCreateAPIView):
#     """
#     """
#     #TODO: filter by project id
#         #get more info from users? (name....)
#     queryset = Follow.objects.all()
#     serializer_class = FollowerSerializer
#
# class OwnDetail(generics.ListCreateAPIView):
#     """
#     """
#     #TODO: filter by project id
#         #get more info from owner? (most of it?)
#     queryset = Own.objects.all()
#     serializer_class = OwnDetailSerializer
#
# """ Concrete View Classes
# #CreateAPIView
# Used for create-only endpoints.
# #ListAPIView
# Used for read-only endpoints to represent a collection of model instances.
# #RetrieveAPIView
# Used for read-only endpoints to represent a single model instance.
# #DestroyAPIView
# Used for delete-only endpoints for a single model instance.
# #UpdateAPIView
# Used for update-only endpoints for a single model instance.
# #ListCreateAPIView
# Used for read-write endpoints to represent a collection of model instances.
# #RetrieveUpdateAPIView
# Used for read or update endpoints to represent a single model instance.
# #RetrieveDestroyAPIView
# Used for read or delete endpoints to represent a single model instance.
# #RetrieveUpdateDestroyAPIView
# Used for read-write-delete endpoints to represent a single model instance.
# """
