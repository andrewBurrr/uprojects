from projects.models import Project
from .serializers import ProjectSerializer
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
    serializer_class = ProjectSerializer


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
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
