from django.urls import path
from .views import ProjectList, ProjectDetail

# Define the url namespace for these URL patterns
app_name = 'apis'

urlpatterns = [
    # URL pattern to retrieve a specific project (provides the primary key in the url slug)
    path('<int:pk>/', ProjectDetail.as_view(), name='detailcreate'),
    # URL pattern for listing and creating projects
    path('', ProjectList.as_view(), name='listcreate')
]
