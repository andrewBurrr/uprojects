import uuid
from os.path import join
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from .storage import OverwriteStorage


# TODO: Make sure that models create Owner_id for each user when user is created.
# TODO: comment

# def image_to_path(instance, filename, category):
#     extension = filename.split('.')[-1]
#     unique_filename = f'{category}.{extension}'
#     result = join(f'{category}', f'{instance.id}_{unique_filename}')
#     return result


class CustomAccountManager(BaseUserManager):
    """
    Custom Account Manager inheriting from Django's BaseUserManager class
    - This class creates users and superusers within the specs of our project.
    """

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        """
        TODO: Document
        """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **other_fields)


    def create_user(self, email, first_name, last_name, password, **other_fields):
        """
        TODO: Document
        """
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomAccount(AbstractBaseUser, PermissionsMixin):
    """
    Custom Account Model using Django's AbstractBaseUser and Django's PermissionsMixin
    
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    # profile_image = models.ImageField(upload_to=lambda instance, filename: image_to_path(instance, filename, "profile_image"), storage=OverwriteStorage(), blank=True)
    profile_image = models.ImageField(upload_to="images/profile_images/", blank=True)
    about = models.TextField(max_length=1000)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Owner(models.Model):
    """
    Owner model used by django's built in ORM

    This model defines the fields and parameters that will be defined for the 
    Owner table.

    Attributes:
        id (int): (Primary Key)The owner identification number of both user's and 
                 Organizations.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)


class Tag(models.Model):

    """
    Tag model used by django's built in ORM

    This model defines the fields and parameters that will be defined for the 
    Tag table.

    Attributes:
        tag (str): (Primary Key) Char Field containing the specified tag
    """

    tag = models.CharField(max_length=60, primary_key=True, unique=True)


class CustomUser(CustomAccount):
    """
    CustomUser model inheriting from the CustomAccount model.

    This model defines the fields and parameters that will be defined for the 
    CustomUser table.

    Attributes:
        owner_id (int): (Foreign Key) A custom user's assigned Owner id number.
        tag (list(str)): tags associated with a user
    """
    # TODO: We changed the on delete behaviour to SET_NULL. If an owner get's 
    # deleted shouldn't we cascade? because every user,organization, project, etc
    # needs a ownerID.

    owner_id = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)


class CustomAdmin(CustomAccount):
    """
    TODO: comment
    """
    admin_type = models.CharField(max_length=60)


class CustomAdminPermission(models.Model):
    """
    TODO: comment
    """
    PERMISSIONS = [
        ("R", "read"),
        ("W", "write"),
        ("X", "execute")
    ]
    admin_id = models.ForeignKey(CustomAdmin, on_delete=models.CASCADE)
    permission = models.CharField(max_length=1, choices=PERMISSIONS, default="R")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["admin_id", "permission"],
                name="unique_admin_permission_constraint"
            )
        ]


class Organization(models.Model):
    """
    TODO: comment
    """
    org_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    #logo = models.ImageField(upload_to=lambda instance, filename: image_to_path(instance, filename, "logo_image"), storage=OverwriteStorage(), blank=True)  # TODO figure out params
    logo = models.ImageField(upload_to="images/logo_images/", blank=True)  # TODO yolo 
    name = models.CharField(max_length=60)
    description = models.TextField()
    user_owner = models.ForeignKey(Owner, related_name="user_owner", on_delete=models.CASCADE)
    owner_id = models.ForeignKey(Owner, related_name="owner_id", on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

