import uuid
from django.db import models
from users.models import CustomUser

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
    VISIBILITY = [
        ("PUBLIC", "public"),
        ("PRIVATE", "private"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField()
    visibility = models.CharField(choices=VISIBILITY, default="PRIVATE")
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # check whether this is cascading on user deletion or project deletion. reference Owners in diagram (probably not a User type)

    def __str__(self):
        return self.name
    

class Project_tags(models.Model):
    """
    Project model used by django's built in ORM

    This model defines the fields and parameters that will be defined for
    the projects table

    Attributes:
        id (int): implicitly defined by django models that dont specify a pk (primary key)
        name (str): The text field name for the project (will likely be changed or removed later)
    """
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag_name = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project_id", "tag_name"], name = "Utag_name_comb"
            )
        ]

