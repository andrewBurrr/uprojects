from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType

from .permissions import IsOwnerOrReadOnly
from .serializers import *
from users.models import CustomUser, Organization
from projects.models import (
    Project, Team, Member, Follow, Event, PartOf,
    Repository, Item, Issue, CodeReview, PullRequest,
    BugResponse, BugReport, Hosts, DropboxSubmission,
    SubmissionFile
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
    """
    View to get a single user by user id.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'


class UserUpdate(generics.UpdateAPIView):
    """ 
    Allows a user to update their using patch requests.
    View to update currently logged in CustomUser attributes. 
    If a field is left blank just returns the current user values for that field.
    Updates the following fields:
    - 'profile_image' 
    - 'about' 
    - 'first_name'
    - 'last_name'
    - 'password'
    - 'tags'
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class UserSelfDelete(generics.DestroyAPIView):
    """
    Allows a user to delete their own account.
    Uses the model delete method to delete the user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
            user = CustomUser.objects.get(id=request.user.id)
            user.delete()
            return Response(status=204)
    

class UserProjectList(generics.ListCreateAPIView):
    """
    View to get a list of public projects by owner id.
    """
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
    lookup_fields = ['user_id']

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Follow.objects.filter(user_id=user_id)


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


class ProjectTeamList(generics.ListCreateAPIView):
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


class OrganizationRegister(generics.CreateAPIView):
    serializer_class = OrganizationRegisterSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EventDropboxSubmissionList(generics.ListCreateAPIView):
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


class BugResponseList(generics.ListCreateAPIView):
    serializer_class = BugResponseSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        bug_id = self.kwargs.get('bug_id')
        return BugResponse.objects.filter(bug_id=bug_id)


class BugResponseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BugResponse.objects.all()
    serializer_class = BugResponseSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        query_set = self.get_queryset()
        composite_key = {
            'bug_id': self.kwargs['bug_id'],
            'admin_id': self.kwargs['admin_id'],
        }
        obj = get_object_or_404(query_set, **composite_key)
        self.check_object_permissions(self.request, obj)
        return obj


class ProjectListSearch(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        tags = self.request.query_params.getlist('tags', [])
        sort_order = self.request.query_params.get('sort', '')

        # Start with all projects
        # TODO filter by projects visible to the current user
        queryset = Project.objects.all()

        # Apply search filters
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))

        # Apply tag filters
        if tags:
            queryset = queryset.filter(tags__tag__in=tags)

        # Apply sorting
        if sort_order:
            queryset = queryset.order_by(sort_order)

        return queryset


class TeamListSearch(generics.ListAPIView):
    serializer_class = TeamSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        tags = self.request.query_params.getlist('tags', [])
        sort_order = self.request.query_params.get('sort', '')

        # Start with all teams
        queryset = Team.objects.all()

        # Apply search filters
        if query:
            queryset = queryset.filter(Q(team_name__icontains=query))

        # Apply tag filters
        if tags:
            queryset = queryset.filter(tags__tag__in=tags)

        # Apply sorting
        if sort_order:
            queryset = queryset.order_by(sort_order)

        return queryset


class EventListSearch(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        tags = self.request.query_params.getlist('tags', [])
        sort_order = self.request.query_params.get('sort', '')

        # Start with all events
        queryset = Event.objects.all()

        # Apply search filters
        if query:
            queryset = queryset.filter(Q(name__icontains=query))

        # Apply tag filters
        if tags:
            queryset = queryset.filter(tags__tag__in=tags)

        # Apply sorting
        if sort_order:
            queryset = queryset.order_by(sort_order)

        return queryset


class OrganizationListSearch(generics.ListAPIView):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        tags = self.request.query_params.getlist('tags', [])
        sort_order = self.request.query_params.get('sort', '')

        # start with all organizations
        queryset = Organization.objects.all()

        # Apply search filters
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))

        # Apply tag filters
        if tags:
            queryset = queryset.filter(tags__tag__in=tags)

        # Apply sorting
        if sort_order:
            queryset = queryset.order_by(sort_order)

        return queryset


class UserListSearch(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        tags = self.request.query_params.getlist('tags', '')
        sort_order = self.request.query_params.get('sort', '')

        # Start with all users
        queryset = CustomUser.objects.all()

        # Apply search filters
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(profession__icontains=query) |
                Q(about__icontains=query)
            )

        # Apply tag filters
        if tags:
            queryset = queryset.filter(tags__tag__in=tags)

        # Apply sorting
        if sort_order:
            queryset = queryset.order_by(sort_order)

        return queryset


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