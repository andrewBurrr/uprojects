from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType

from .permissions import IsOwnerOrReadOnly
from .serializers import *
from users.models import CustomUser, Organization
from projects.models import (
    Project, Team, Member, Follow, Event, PartOf,
    Repository, Item, Issue, CodeReview, PullRequest, BugReport,
    Hosts, DropboxSubmission, SubmissionFile
)


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
    lookup_field = 'id'


class UserProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        owner_id = self.kwargs.get('owner_id')
        user_id = self.request.user.id
        current_user = CustomUser.objects.get(id=user_id)

        if self.request.user.is_authenticated and current_user.owner_id.id == owner_id:
            queryset = Project.objects.filter(owner_id=owner_id)
        else:
            user_teams = Member.objects.filter(user_id=current_user.id).values('team')
            queryset = Project.objects.filter(
                Q(owner_id=owner_id, visibility='PUBLIC') |
                Q(owner_id=owner_id, partof__team__in=user_teams)
            )
        return queryset


# Q(owner_id=owner_id, partof__team__in=user_teams)


class UserTeamList(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        owner_id = CustomUser.objects.get(id=user_id).owner_id
        user_teams = Member.objects.filter(user_id=user_id).values('team')
        owned_teams = Team.objects.filter(owner_id=owner_id).values('id')
        queryset = Team.objects.filter(Q(id__in=user_teams) | Q(id__in=owned_teams))
        return queryset


class UserOrganizationList(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['owner_id']
        return Organization.objects.filter(owner_id=user_id)


class UserFollowList(MultipleFieldLookupMixin, generics.ListCreateAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_fields = ['user_id']

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follow.objects.filter(user_id=user_id)


class GlobalSearchAPIView(generics.ListAPIView):
    serializer_class = SearchResultSerializer
    ordering_fields = ['projects', 'teams', 'events', 'orgs', 'users']

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        tags = self.request.query_params.getlist('tags', [])
        project_results = Project.objects.filter(name__icontains=query)  # TODO restrict public projects
        team_results = Team.objects.filter(team_name__icontains=query)
        event_results = Event.objects.filter(name__icontains=query)
        org_results = Organization.objects.filter(name__icontains=query)
        user_results = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))

        if tags:
            project_results = project_results.filter(tags__tag__in=tags)
            team_results = team_results.filter(tags__tag__in=tags)
            event_results = event_results.filter(tags__tag__in=tags)
            org_results = org_results.filter(tags__tag__in=tags)
            user_results = user_results.filter(tags__tag__in=tags)

        # all_results = {
        #     'projects': ProjectSerializer(project_results, many=True).data,
        #     'teams': TeamSerializer(team_results, many=True).data,
        #     'events': EventSerializer(event_results, many=True).data,
        #     'orgs': OrganizationSerializer(org_results, many=True).data,
        #     'users': UserSerializer(user_results, many=True).data
        # }

        all_results = SearchResultSerializer(
            ProjectSerializer(project_results, many=True).data,
            TeamSerializer(team_results, many=True).data,
            EventSerializer(event_results, many=True).data,
            OrganizationSerializer(org_results, many=True).data,
            UserSerializer(user_results, many=True).data
        )

        # order_by = self.request.query_params.get('sort', '')
        # if order_by and order_by in self.ordering_fields:
        #     for category, results in all_results.items():
        #         all_results[category] = sorted(results, key=lambda x: x[order_by])

        return all_results


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        query_set = self.get_queryset()
        composite_key = {
            'owner_id': self.kwargs['owner_id'],
            'team_name': self.kwargs['team_name'],
        }
        obj = get_object_or_404(query_set, **composite_key)
        self.check_object_permissions(self.request, obj)
        return obj


class TeamMembersList(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        composite_key = {
            'owner_id': self.kwargs['owner_id'],
            'team_name': self.kwargs['team_name'],
        }
        team = get_object_or_404(Team.objects.all(), **composite_key)
        queryset = Member.objects.filter(team=team)
        return queryset
# project


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]  # TODO use permissions fields


class ProjectTeamsList(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]  # TODO use permissions fields

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = PartOf.objects.filter(project_id=project_id).values('team')
        return queryset


class ProjectRepositoryList(generics.ListCreateAPIView):
    serializer_class = RepositorySerializer
    permission_classes = [IsOwnerOrReadOnly]  # TODO use permissions fields

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Repository.objects.filter(project_id=project_id)


# repository

class RepositoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = [IsOwnerOrReadOnly]  # TODO use permissions fields


class RepositoryItemList(generics.ListCreateAPIView):
    serializer_class_mapping = {
        'issue': IssueSerializer,
        'pullrequest': PullRequestSerializer,
        'codereview': CodeReviewSerializer
    }

    def get_serializer_class(self):
        type_param = self.request.query_params.get('type', '').lower()
        return self.serializer_class_mapping.get(type_param, ItemSerializer)

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(Item)
        issues = Issue.objects.filter(content_type=content_type)
        pull_requests = PullRequest.objects.filter(content_type=content_type)
        code_reviews = CodeReview.objects.filter(content_type=content_type)

        queryset = list(issues) + list(pull_requests) + list(code_reviews)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        type_param = self.request.query_params.get('type', '').lower()
        model_map = {
            'issue': Issue,
            'pullrequest': PullRequest,
            'codereview': CodeReview
        }

        model = model_map.get(type_param)
        if model:
            item = serializer.save()
            model.objects.create(item=item)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class_mapping = {
        'issue': IssueSerializer,
        'pullrequest': PullRequestSerializer,
        'codereview': CodeReviewSerializer,
    }

    def get_queryset(self):
        # Get ContentType for the Item superclass
        item_content_type = ContentType.objects.get_for_model(Item)

        # Retrieve objects from the Issue, PullRequest, and CodeReview models based on the common ContentType
        issues = Issue.objects.filter(content_type=item_content_type)
        pull_requests = PullRequest.objects.filter(content_type=item_content_type)
        code_reviews = CodeReview.objects.filter(content_type=item_content_type)

        # Combine the queryset for all objects
        queryset = list(issues) + list(pull_requests) + list(code_reviews)
        return queryset

    def get_serializer_class(self):
        # Determine the serializer class based on the 'type' query parameter
        type_param = self.request.query_params.get('type', '').lower()
        return self.serializer_class_mapping.get(type_param, IssueSerializer)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        type_param = self.request.query_params.get('type', '').lower()
        model_map = {
            'issue': Issue,
            'pullrequest': PullRequest,
            'codereview': CodeReview
        }

        model = model_map.get(type_param)
        if model:
            item = serializer.save()
            model.objects.create(item=item)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# organization


class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsOwnerOrReadOnly]


class OrganizationProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        # show all projects that the org owns that are public
        # if the current user owns the org, show all projects
        # if the current user is on a team for a project show it
        org_id = self.kwargs.get('org_id')
        org = Organization.objects.get(id=org_id)
        current_user = CustomUser.objects.get(id=self.request.user.id)

        if current_user.is_authenticated and current_user.owner_id == org.user_owner:
            queryset = Project.objects.filter(org.owner_id)
        else:
            user_teams = Member.objects.filter(user_id=current_user.id).values('team')
            queryset = Project.objects.filter(
                Q(owner_id=org.owner_id, visibility='public') |
                Q(owner_id=org.owner_id, partof__team__in=user_teams)
            )
        return queryset


class OrganizationTeamList(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        owner_id = self.kwargs['owner_id']
        queryset = Team.objects.filter(owner_id=owner_id)
        return queryset


class OrganizationEventsList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        queryset = Event.objects.filter(
            id__in=Hosts.objects.filter(org_id=organization_id).values('event_id'),
        )
        return queryset


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EventDropBoxSubmissionList(generics.ListCreateAPIView):
    serializer_class = DropboxSubmissionSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        queryset = DropboxSubmission.objects.filter(event_id=event_id)
        return queryset


class DropBoxSubmissionDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = DropboxSubmission.objects.all()
    serializer_class = DropboxSubmissionSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_fields = ['event_id', 'team']


class DropBoxSubmissionFileList(generics.ListCreateAPIView):
    serializer_class = SubmissionFileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        submission = self.kwargs['submission']
        queryset = SubmissionFile.objects.filter(
            submission=submission
        )
        return queryset


class BugList(generics.ListCreateAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    permission_classes = [IsOwnerOrReadOnly]


class BugDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugReportSerializer
    permission_classes = [IsOwnerOrReadOnly]

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
# class OwnerOfTeamList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating teams that an owner is an owner of.
#
#     Attributes:
#         TODO properly fetch by owner_id
#         queryset (QuerySet): The queryset of Team instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing Team instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = Team.objects.all()
#     serializer_class = OwnerOfTeamSerializer
#
# #NOTE since we still have team tags for searching, i (david) propose adding a visibility field to Teams
# class TeamList(generics.ListCreateAPIView):
#     """
#     """
#     #TODO: filter by tags and or owner searched for (and publicity?)
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#
# class TeamPemissionList(generics.ListCreateAPIView):
#     """
#     API view for listing and creating permissions for a team.
#
#     Attributes:
#         TODO properly fetch by Team_id
#         queryset (QuerySet): The queryset of TeamPermission instances to be used for listing.
#         serializer_class (Serializer): The serializer class used for
#             serializing/deserializing TeamPermission instances.
#
#     Note:
#         This view assumes that you have configured the URL pattern to map to it
#         and that you have set the 'api_name' namespace for the URL pattern.
#     """
#     queryset = TeamPermission.objects.all()
#     serializer_class = TeamPermissionSerializer
#
# #NOTE purely to delete permissions
# class TeamPemissionDetail(generics.DestroyAPIView):
#     """
#     """
#     #TODO: filter by Team and permission
#     queryset = TeamPermission.objects.all()
#     serializer_class = TeamPermissionSerializer
#
# class UserIsMemberOfList(generics.ListCreateAPIView):
#     """
#     """
#     #TODO: filter by user id
#         #gets all teams a user is a member of
#     queryset = TeamPermission.objects.all()
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
#     queryset = TeamPermission.objects.all()
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
#         TODO maybe get more info from Teams?
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
#         #maybe get more info from Teams?
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
