from django.db import models


# Create your models here.
class Project(models.Model):
    """
    Project model used by django's built in ORM

    This model defines the fields and parameters that will be defined for
    the projects table

    Attributes:
        id (int): implicitly defined by django models that dont specify a pk (primary key)
        name (str): The text field name for the project (will likely be changed or removed later)
    """
    name = models.TextField()

    def __str__(self):
        return self.name
