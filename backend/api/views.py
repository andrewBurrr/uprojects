from projects.models import (Project, Repository, Item, PullRequest, Issue, Commit,
                             CodeReview, Tag, Collaborator, CollaboratorPermission, Member, PartOf, Follow, Own)
from .serializers import (ProjectSerializer, ProjectDetailSerializer, RepositorySerializer,
                          ItemSerializer, ItemDetailSerializer, PullRequestSerializer, PullRequestDetailSerializer,
                          IssueSerializer, IssueDetailSerializer, CommitSerializer, CommitDetailSerializer,
                          CodeReviewSerializer, CodeReviewDetailSerializer, TagSerializer,
                          OwnerOfCollaboratorSerializer, CollaboratorSerializer, CollaboratorPermissionSerializer,
                          UserIsMemberOfSerializer, MemberUserSerializer, MemberDetailSerializer,
                          PartOfProjectSerializer, PartOfTeamSerializer,
                          FollowSerializer, FollowerSerializer,
                          OwnDetailSerializer)
from rest_framework import generics


class ProjectList(generics.ListCreateAPIView):
    """
    API view for listing and creating projects.

    Attributes:
        queryset (QuerySet): The queryset of Project instances to be used for listing.
        serializer_class (Serializer): The serializer class used for
            serializing/deserializing Project instances.

    Example Usage:
        To list all projects, make a GET request to the endpoint associated with
        this view.

        To create a new project, make a POST request to the same endpoint with
        the project data in the request body.

    Note:
        This view assumes that you have configured the URL pattern to map to it
        and that you have set the 'api_name' namespace for the URL pattern.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class PublicProjectList(generics.ListAPIView):
    """
    """
    #TODO: filter by visibility = "PUBLIC"
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving and updating projects.

    Attributes:
        TODO properly fetch by id
        queryset (QuerySet): The queryset of Project instances to be used for listing.
        serializer_class (Serializer): The serializer class used for
            serializing/deserializing Project instances.

    Note:
        This view assumes that you have configured the URL pattern to map to it
        and that you have set the 'api_name' namespace for the URL pattern.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer

class RepositoryList(generics.ListCreateAPIView):
    """
    """
    #TODO: all repositories in a project
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

class RepositoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    #TODO: one repository by project id, repo name
        #the idea for this is to delete one repo
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

#NOTE need?
class ItemProjectList(generics.ListCreateAPIView):
    """
    """
    #TODO: all items for a project
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemRepositoryList(generics.ListCreateAPIView):
    """
    """
    #TODO: all items for a project
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    #TODO: specific item by project id, repo name, item id
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer

#NOTE need?
class PullRequestProjectList(generics.ListCreateAPIView):
    """
    """
    #TODO: list of pull requests for a project
    queryset = PullRequest.objects.all()
    serializer_class = PullRequestSerializer

class PullRequestRepositoryList(generics.ListCreateAPIView):
    """
    """
    #TODO: list of pull requests for a repository
    queryset = PullRequest.objects.all()
    serializer_class = PullRequestSerializer

class PullRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    #TODO: single pull request given project id, repo name, item id
    queryset = PullRequest.objects.all()
    serializer_class = PullRequestDetailSerializer

#NOTE need?
class IssueProjectList(generics.ListCreateAPIView):
    """
    """
    #TODO: list of issues for a project
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class IssueRepositoryList(generics.ListCreateAPIView):
    """
    """
    #TODO: list of issues for a repository
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    #TODO: single issue given project id, repo name, item id
    queryset = Issue.objects.all()
    serializer_class = IssueDetailSerializer

#NOTE DIDNT INCLUDE ALL COMMITS FOR PROJECT
class CommitRepositoryList(generics.ListCreateAPIView):
    """
    """
    #TODO: list of commits for a repository
    queryset = Commit.objects.all()
    serializer_class = CommitSerializer

class CommitDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    #TODO: single commit given project id, repo name, item id
    queryset = Commit.objects.all()
    serializer_class = CommitDetailSerializer

#NOTE need?
class CodeReviewProjectList(generics.ListCreateAPIView):
    """
    """
    #TODO: list of code reviews for a project
    queryset = CodeReview.objects.all()
    serializer_class = CodeReviewSerializer

class CodeReviewRepositoryList(generics.ListCreateAPIView):
    """
    """
    #TODO: list of code reviews for a repository
    queryset = CodeReview.objects.all()
    serializer_class = CodeReviewSerializer

class CodeReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    #TODO: single code reviews given project id, repo name, item id
    queryset = CodeReview.objects.all()
    serializer_class = CodeReviewDetailSerializer

#NOTE not sure if this is the way to do it, but so that when tags are added to anything, if it didn't exist before, its added. if it existed before, it is matched (case insensitive)
class TagList(generics.ListCreateAPIView):
    """
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class OwnerOfCollaboratorList(generics.RetrieveUpdateDestroyAPIView):
    """
    """
    #TODO: filter by owner
    queryset = Collaborator.objects.all()
    serializer_class = OwnerOfCollaboratorSerializer

#NOTE since we still have team tags, i (david) propose adding a visibility field to collaborators
class CollaboratorList(generics.ListCreateAPIView):
    """
    """
    #TODO: filter by tags and or owner searched for (and publicity?)
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer

class CollaboratorPemissionList(generics.ListCreateAPIView):
    """
    """
    #TODO: filter by collaborator
    queryset = CollaboratorPermission.objects.all()
    serializer_class = CollaboratorPermissionSerializer

#NOTE purely to delete permissions
class CollaboratorPemissionDetail(generics.DestroyAPIView):
    """
    """
    #TODO: filter by collaborator and permission
    queryset = CollaboratorPermission.objects.all()
    serializer_class = CollaboratorPermissionSerializer

class UserIsMemberOfList(generics.RetrieveDestroyAPIView):
    """
    """
    #TODO: filter by user id
        #gets all teams a user is a member of
    queryset = CollaboratorPermission.objects.all()
    serializer_class = UserIsMemberOfSerializer

class MemberList(generics.ListCreateAPIView):
    """
    """
    #TODO: filter by owner id and team name
        #all members in one team
    queryset = CollaboratorPermission.objects.all()
    serializer_class = MemberUserSerializer

#NOTE purely to delete members from team
class MemberInfo(generics.RetrieveDestroyAPIView):
    """
    """
    #TODO: filter by owner id, team name, and user id
        #maybe give some of user info too?
    queryset = Member.objects.all()
    serializer_class = MemberDetailSerializer

class PartOfProjectList(generics.ListCreateAPIView):
    """
    """
    #TODO: filter by project
    queryset = PartOf.objects.all()
    serializer_class = PartOfProjectSerializer

class PartOfTeamList(generics.ListCreateAPIView):
    """
    """
    #TODO: filter by team_name
        #maybe get more info from collaborators?
    queryset = PartOf.objects.all()
    serializer_class = PartOfTeamSerializer

class PartOfProjectDetail(generics.RetrieveDestroyAPIView):
    """
    """
    #TODO: filter by team_name
        #maybe get more info from collaborators?
    queryset = PartOf.objects.all()
    serializer_class = PartOfTeamSerializer

class FollowList(generics.ListCreateAPIView):
    """
    """
    #TODO: filter by user id
        #maybe get more info from project (name...)
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

class FolowDetail(generics.RetrieveDestroyAPIView):
    """
    """
    #TODO: filter by user id and project id
        #get more info from projects (most of it?)?
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

#NOTE when a project is changed from public to pricate how delete all followers?
class FolowersList(generics.ListCreateAPIView):
    """
    """
    #TODO: filter by project id
        #get more info from users? (name....)
    queryset = Follow.objects.all()
    serializer_class = FollowerSerializer

class OwnDetail(generics.ListCreateAPIView):
    """
    """
    #TODO: filter by project id
        #get more info from owner? (most of it?)
    queryset = Own.objects.all()
    serializer_class = OwnDetailSerializer

""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
#ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
#RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
