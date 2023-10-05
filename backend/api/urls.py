from django.urls import path
from .views import ProjectList, ProjectDetail

# Define the url namespace for these URL patterns
app_name = 'api'

urlpatterns = [
    # URL pattern to retrieve a specific project
    path('<int:pk>/', ProjectDetail.as_view(), name='detailcreate'),
    # URL pattern for listing and creating projects
    path('', ProjectList.as_view(), name='listcreate')
]
