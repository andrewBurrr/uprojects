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
    """
    View to get a single user by user id.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'


class UserProjectList(generics.ListCreateAPIView):
    """
    View to get a list of public projects by owner id. 
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]

    #TODO: WIP

    def get_queryset(self):
        # queryset = Project.objects.all()

        url_owner_id = self.kwargs['owner_id']

        #getting all public projects
        public_projects = Project.objects.filter(visibility='PUBLIC')
        queryset = public_projects

        # this will break if nobody is loged in

        # current_user = CustomUser.objects.get(id=self.request.user)

        # FIXME: current issue is idk how to get the current users owner id for authentication checks

        if self.request.user.is_authenticated:# and self.request.user.owner_id == url_owner_id:
            #getting all projects this user owns
            # need to go through the owns table.
                # filter the owns table by owner_id
                # then filter the projects table by all the project_id in the result

            # FIXME: might be better to just use union here too lol
            user_owner = Own.objects.filter(owner_id=url_owner_id).values('project_id')
            user_owns = Project.objects.filter(project_id__in=user_owner)

            #getting all projects this user has access to (teams)

            # need to go through the member table (project team) filtering by user_id=requests.user.id
                # then go through the teams (project owner_id) filtering by id=team.id
                    # then go through owns (project project_id) filtering by owner_id= teams owner id
                        # then go through project filtering by project_id = owns project_id
            user_member = Member.objects.filter(user_id=self.request.user.id).values('team')
            team_owner = Team.objects.filter(id__in=user_member).values('owner_id')
            project_owner = Own.objects.filter(owner_id__in=team_owner).values('project_id')
            user_has_access_to = Project.objects.filter(project_id__in=project_owner)

            # user_owns = Project.objects.all()
            # user_has_access_to = Project.objects.all()

            queryset = (public_projects.union(user_owns)).union(user_has_access_to)
    
        return queryset

    # def get_queryset(self):
    #     # test = self.kwargs.get('owner_id')
    #     # owner_id = Owner.objects.get(id=test)
    #     user_id = self.request.user.id
    #     current_user = CustomUser.objects.get(id=user_id)

    #     if self.request.user.is_authenticated and current_user.owner_id == owner_id:
    #         queryset = Project.objects.filter(owner_id=owner_id)
    #     else:
    #         user_teams = Member.objects.filter(user_id=current_user.id).values('team')
    #         queryset = Project.objects.filter(
    #             Q(owner_id=owner_id, visibility='public') |
    #             Q(owner_id=owner_id, partof__team__in=user_teams))
    #     return queryset


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


class GlobalSearchAPIView(generics.ListAPIView):
    serializer_class = None
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

        all_results = {
            'projects': ProjectSerializer(project_results, many=True).data,
            'teams': TeamSerializer(team_results, many=True).data,
            'events': EventSerializer(event_results, many=True).data,
            'orgs': OrganizationSerializer(org_results, many=True).data,
            'users': UserSerializer(user_results, many=True).data
        }
        # localhost:8000/search/?q='some stuff'&tags='','',''&sort='reverse'
        order_by = self.request.query_params.get('sort', '')
        if order_by and order_by in self.ordering_fields:
            for category, results in all_results.items():
                all_results[category] = sorted(results, key=lambda x: x[order_by])

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
# project

# TODO: fix
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
        return self.serializer_class_mapping.get(type_param, IssueSerializer)

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

# TODO: Make a view for each item type. I don't think that item detail view will work 
#       for abstract classes. This will need testing.
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
    serializer_class = BugResponseSerializer
    permission_classes = [IsOwnerOrReadOnly]


class BugDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BugReport.objects.all()
    serializer_class = BugResponseSerializer
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