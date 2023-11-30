from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType

from .permissions import IsOwnerOrReadOnly
from .serializers import *
# (UserSerializer, ProjectSerializer, TeamSerializer, OrganizationSerializer,
#     UserFollowSerializer, EventSerializer, BaseSearchSerializer, RepositorySerializer, IssueSerializer)
from users.models import CustomUser, Organization
from projects.models import (Project, Team, Member, Follow, Event, PartOf,
                              Repository, Item, Issue, CodeReview, PullRequest, BugReport,
                              Hosts, DropboxSubmission, SubmissionFile)


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
    """
    View to get a single user by user id.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserProjectList(generics.ListCreateAPIView):
    """
    View to get a list of public projects by owner id. 
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'owner_id'

    def get_queryset(self):
        current_user = self.request.user
        queryset = Project.objects.filter(Q(visibility='public') | Q(owner_id=current_user.owner_id))
        return queryset


class UserTeamsList(generics.ListCreateAPIView):
    """
    TODO: this serializer is poorly named. should be member related
    """
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Team.objects.filter(
            team_name__in=Member.objects.filter(user_id=user_id).values('team_name'),
            owner_id__in=Member.objects.filter(user_id=user_id).values('owner_id')
        )
        return queryset


class UserOrganizationList(generics.ListCreateAPIView):
    """
    View to get a list of organizations by owner id.
    FIXME: im not actually sure how this works
    """
    serializer_class = OrganizationSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['owner_id']
        return Organization.objects.filter(owner_id=user_id)


class UserFollowList(MultipleFieldLookupMixin, generics.ListCreateAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_fields = ['user_id', 'project_id']

    def get_queryset(self):
        return Follow.objects.all()


# # search
# class SearchView(generics.ListAPIView):
#     serializer_class = None

#     def get_serializer_class(self):
#         model_name = self.request.query_params.get('model')
#         if model_name == 'project':
#             self.queryset = Project.objects.all()
#             return ProjectSerializer
#         elif model_name == 'team':
#             self.queryset = Team.objects.all()
#             return TeamSerializer
#         elif model_name == 'organization':
#             self.queryset = Team.objects.all()
#             return OrganizationSerializer
#         elif model_name == 'event':
#             self.queryset = Event.objects.all()
#             return EventSerializer
#         elif model_name == 'user':
#             self.queryset = Event.objects.all()
#             return UserSerializer
#         return BaseSearchSerializer

#     def get_queryset(self):
#         search_query = self.request.query_params.get('query', '')
#         tags = self.request.query_params.getlist('tags', [])

#         queryset = self.queryset.filter(
#             Q(name__icontains=search_query) |
#             Q(description__icontains=search_query)
#         )

#         if tags:
#             queryset.filter(tags__overlap=tags)
#         return queryset

# project


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]  # TODO use permissions fields


class ProjectTeamsList(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]  # TODO use permissions fields
    lookup_field = 'project_id'

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        queryset = Team.objects.filter(
            team_name__in=PartOf.objects.filter(user_id=project_id).values('team_name'),
            owner_id__in=PartOf.objects.filter(user_id=project_id).values('owner_id')
        )
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
    permission_classes = [IsOwnerOrReadOnly]  # TODO use permissions fields


class OrganizationEventsList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        queryset = Event.objects.filter(
            id__in=Hosts.objects.filter(org_id=organization_id).values('event_id'),
        )
        return queryset


class OrganizationTeamsList(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        owner_id = self.kwargs['owner_id']
        queryset = Team.objects.filter(owner_id=owner_id)
        return queryset


class TeamMembersList(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        owner_id = self.kwargs['owner_id']
        team_name = self.kwargs['team_name']
        queryset = Member.objects.filter(
            owner_id=owner_id,
            team_name=team_name
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
