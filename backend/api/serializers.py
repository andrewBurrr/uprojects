from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """
        Serializer for the Project model.
        TODO update serializer and model schema to match data requirements

        This serializer is used to convert Project model instances to JSON
        representations and vice versa. It specifies the fields to include
        in the serialized output.

        Attributes:
            id (int): The unique identifier for the project.
            name (str): The name of the project.

        Note:
            This serializer is used in conjunction with views to provide a
            RESTful API for managing Project instances.
        """
    class Meta:
        model = Project
        fields = ('id', 'name')
