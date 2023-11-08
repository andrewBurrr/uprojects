from django.urls import path
from .views import UserDetail, UserProjectList, UserTeamsList, UserOrganizationList

# Define the url namespace for these URL patterns
app_name = 'apis'

# TODO Tag lookup performs query on project list/team list/etc
# TODO collaborator view (unique by owner_id, team_name)
# TODO collaborator permissions (might do a join on another query), show all members of a team and team permissions/settings (unique by collaborator_id, permission)
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
    # get User dashboard
    path('user/<uuid:pk>', UserDetail.as_view(), name='userdetail'),
    path('user-projects/<uuid:owner_id>', UserProjectList.as_view(), name='userprojectdetail'),
    path('user-teams/<uuid:user_id>', UserTeamsList.as_view(), name='userteamslist'),
    path('user-organizations/<uuid:owner_id>', UserOrganizationList.as_view(), name='userorganizationlist'),
    # path('user-follows/<uuid:user_id>', UserFollows.as_view(), name='userfollows'),
    # get searchbar
    # URL pattern to retrieve a specific project (provides the primary key in the url slug)
    # path('<int:pk>/', ProjectDetail.as_view(), name='detailcreate'),
    # # URL pattern for listing and creating projects
    # path('', ProjectList.as_view(), name='listcreate')
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