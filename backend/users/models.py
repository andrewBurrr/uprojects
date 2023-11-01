import uuid
from os.path import join
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from .storage import OverwriteStorage

# TODO: Make sure that models create Owner_id for each user when user is created.
#TODO: comment

def image_to_path(instance, filename):
    extension = filename.split('.')[-1]
    unique_filename = f'profile.{extension}'  # TODO: Change so we're not saving all images to one folder
    result = join('profile_images', f'{instance.id}_{unique_filename}')
    print(result)
    return result


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, last_name, password, **other_fields):

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
    TODO: comment
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    profile_image = models.ImageField(upload_to=image_to_path, storage=OverwriteStorage(), blank=True)
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
    TODO: comment
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)


class Interest(models.Model):
    """
    TODO: comment
    """
    interest = models.CharField(max_length=60, primary_key=True)    


class CustomUser(CustomAccount):
    """
    TODO: comment
    """
    owner_id = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)  # TODO: Should we do an on_delete?
    interest = models.ManyToManyField(Interest)
    

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


class Tag(models.Model):
    """
    TODO: comment
    """
    tag = models.CharField(max_length=60, primary_key=True)  


class Organization(models.Model):
    """
    TODO: comment
    """
    org_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    logo = models.ImageField(upload_to=image_to_path, storage=OverwriteStorage(), blank=True)
    name = models.CharField(max_length=60)
    description = models.TextField()
    owner_id = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)


