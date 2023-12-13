from django.urls import path
from .views import (
    UserDetail, UserProjectList, UserTeamList, UserOrganizationList, UserFollowList,
    OrganizationDetail, OrganizationProjectList, OrganizationTeamList, OrganizationEventsList,
    OrganizationRegister, GlobalSearchAPIView, UserUpdate,
    TeamDetail, TeamMembersList, UserSelfDelete
)
# Define the url namespace for these URL patterns
app_name = 'apis'

# TODO Team view (unique by owner_id, team_name)
# TODO Team permissions (might do a join on another query), show all members of a team and team permissions/settings (unique by Team_id, permission)
# TODO Member (show all the members of a team), probably a read only endpoint (unique by (user_id, owner_id, team_name))
# TODO Project (probably needs multiple views) (unique by id: Strong entity)
# TODO PartOf Links teams to projects (unique by project_id, owner_id, team_name)
# TODO Repository (unique by project_id, repo_name)
# TODO Item (unique by project_id, repo_name, item_id) do something to get the union of all issues, code reviews, and pull requests
# TODO Follow (unique by user_id, project_id)
# TODO Own (unique by owner_id, project_id)


"""
A user must be able to search all projects with a query
A user must be able to view all projects owned by a user/organization under that user/organizations page

"""
urlpatterns = [
    # URL patterns for user dashboard
    path('user/<uuid:id>/', UserDetail.as_view(), name='api-user-detail'),
    path('user/update/<uuid:id/', UserUpdate.as_view(), name='api-user-update'),
    path('user-projects/<uuid:owner_id>/', UserProjectList.as_view(), name='api-user-projects'),
    path('user-teams/<uuid:user_id>/', UserTeamList.as_view(), name='api-user-teams'),
    path('user-orgs/<uuid:owner_id>/', UserOrganizationList.as_view(), name='api-user-orgs'),
    path('user-follows/<uuid:user_id>/', UserFollowList.as_view(), name='api-user-follows'),
    path('user/delete/', UserSelfDelete.as_view(), name='api-user-delete'),
    # URL patterns for organization dashboard
    path('organization/<uuid:id>/', OrganizationDetail.as_view(), name='api-org-detail'),
    path('organization-projects/<uuid:org_id>/', OrganizationProjectList.as_view(), name='api-org-projects'),
    path('organization-teams/<uuid:owner_id>/', OrganizationTeamList.as_view(), name='api-org-teams'),
    path('organization-events/<uuid:owner_id>/', OrganizationEventsList.as_view(), name='api-org-events'),
    path('organization-register/<uuid:user_id>/', OrganizationRegister.as_view(), name='api-org-register'),
    # URL patterns for search
    path('search/', GlobalSearchAPIView.as_view(), name='api-global-search'),
    # URL pattern for teams
    path('team/<uuid:owner_id>/<str:team_name>/', TeamDetail.as_view(), name='api-team-detail'),
    path('team/<uuid:owner_id>/<str:team_name>/members/', TeamMembersList.as_view(), name='api-team-members-list'),
    # URL patterns for project detail
    # path('project/<uuid:id>', ),
    # path('project/<uuid:id>/teams/', ),
    # path('project/<uuid:id>/repos/', ),
    # # URL patterns for repo detail
    # path('repository/<uuid:project_id>/<str:repo_name>/', ),
    # # URL patterns for event detail
    # path('event/'),

    # URL patterns for bugs
]
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
