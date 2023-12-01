import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from .storage import OverwriteStorage


class CustomAccountManager(BaseUserManager):
    """
    Custom Account Manager inheriting from Django's BaseUserManager class.

    This class creates users and superusers within the specifications of our project.

    Methods:
        create_superuser: Creates and returns a superuser with the provided details.
        create_user: Creates and returns a regular user with the provided details.
    """

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        """
        Creates and returns a superuser with the provided details.

        Args:
            email (str): Email address of the superuser.
            first_name (str): First name of the superuser.
            last_name (str): Last name of the superuser.
            password (str): Password for the superuser.
            **other_fields: Additional fields for the superuser.

        Returns:
            User: The created superuser instance.
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
        Creates and returns a regular user with the provided details.

        Args:
            email (str): Email address of the user.
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            password (str): Password for the user.
            **other_fields: Additional fields for the user.

        Returns:
            User: The created user instance.
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
    Custom Account Model using Django's AbstractBaseUser and Django's PermissionsMixin.

    This model represents a custom user account in the system.

    Attributes:
        id (UUID): Unique identifier for the user account.
        profile_image (ImageField): Image representing the user's profile picture.
        about (TextField): Description or information about the user.
        profession (TextField): Profession or role of the user.
        email (EmailField): Email address of the user (must be unique).
        first_name (CharField): First name of the user.
        last_name (CharField): Last name of the user.
        start_date (DateTimeField): Date and time when the user account was created.
        is_staff (BooleanField): Boolean indicating whether the user has staff privileges.
        is_active (BooleanField): Boolean indicating whether the user account is active.

    Inherited Attributes:
        - Additional attributes inherited from AbstractBaseUser and PermissionsMixin.

    Manager:
        objects (CustomAccountManager): Custom manager for the CustomAccount model.

    Required Fields:
        USERNAME_FIELD (str): The field used as the unique identifier for authentication (email in this case).
        REQUIRED_FIELDS (list): List of additional fields required during user creation.

    Methods:
        __str__: Returns a string representation of the user, using first name and last name.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    profile_image = models.ImageField(upload_to="images/profile_images/", storage=OverwriteStorage(), blank=True)
    about = models.TextField(max_length=1000)
    profession = models.TextField(max_length=150, default="")
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
        """
        Returns a string representation of the user, using first name and last name.

        Returns:
            str: String representation of the user.
        """
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
        tags (list(str)): tags associated with a user

        Inherited Attributes:
        Additional attributes inherited from CustomAccount:
        - profile_image (ImageField): Image representing the admin's profile picture.
        - about (TextField): Description or information about the admin.
        - profession (TextField): Profession or role of the admin.
        - email (EmailField): Email address of the admin.
        - first_name (CharField): First name of the admin.
        - last_name (CharField): Last name of the admin.
        - start_date (DateTimeField): Date and time when the admin account was created.
        - is_staff (BooleanField): Boolean indicating whether the admin has staff privileges.
        - is_active (BooleanField): Boolean indicating whether the admin account is active.

    Methods:
        save
    """
    owner_id = models.ForeignKey(Owner, null=True, on_delete=models.CASCADE) # set to null for now, will be set to a unique value upon creation.
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        """
        Overridden save method for the CustomUser model.
        """
        if not self.pk:
            Owner.objects.create()
            self.owner_id = Owner.objects.create()
        super().save(*args, **kwargs)


class CustomAdmin(CustomAccount):
    """
    Model representing a custom administrator in the system.

    Each custom admin has a base set of account information inherited from the CustomAccount model,
    along with an additional attribute to specify the type of administrator.

    Attributes:
        id (UUID): Unique identifier for the custom admin.
        admin_type (CharField): Type of the administrator, e.g., "Superuser" or "Moderator."

    Inherited Attributes:
        Additional attributes inherited from CustomAccount:
        - profile_image (ImageField): Image representing the admin's profile picture.
        - about (TextField): Description or information about the admin.
        - profession (TextField): Profession or role of the admin.
        - email (EmailField): Email address of the admin.
        - first_name (CharField): First name of the admin.
        - last_name (CharField): Last name of the admin.
        - start_date (DateTimeField): Date and time when the admin account was created.
        - is_staff (BooleanField): Boolean indicating whether the admin has staff privileges.
        - is_active (BooleanField): Boolean indicating whether the admin account is active.

    Methods:
        save: Overridden save method to handle the creation of owner information.
              It creates an Owner instance and associates it with the user as an identifier for user owned entities.
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
    Model representing an organization in the system.

    Each organization has a unique identifier, a logo, a name, a description,
    an owner user, an owner identifier, and associated tags.

    Attributes:
        id (UUID): Unique identifier for the organization.
        logo (ImageField): Image representing the organization's logo.
        name (CharField): Name of the organization.
        description (TextField): Description of the organization.
        user_owner (ForeignKey to Owner): Foreign key to the owner user of the organization.
        owner_id (ForeignKey to Owner): Foreign key to the owner identifier of the organization.
        tags (ManyToManyField to Tag): Tags associated with the organization.

    Methods:
        save: Overridden save method to handle the creation of owner information.
              It creates an Owner instance and associates it with the organization as the owner identifier.
              If a user is provided during save (via the 'user' parameter), it sets the user as the owner user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    logo = models.ImageField(upload_to="images/logo_images/", storage=OverwriteStorage(), blank=True)
    name = models.CharField(max_length=60)
    description = models.TextField()
    user_owner = models.ForeignKey(Owner, related_name="user_owner", on_delete=models.CASCADE, null=True) # set to null for now, will be set to a unique value upon creation.
    owner_id = models.ForeignKey(Owner, related_name="owner_id", on_delete=models.SET_NULL, null=True) # set to null for now, will be set to a unique value upon creation.
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        """
        Overridden save method for the Organization model.

        This method is called when saving an Organization instance.
        It handles the creation of owner information:
        - Creates an Owner instance and associates it with the organization as the owner identifier.
        - If a user is provided during save (via the 'user' parameter),
          it sets the user as the owner user.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments, expected to include 'user' (optional).

        Returns:
            None
        """
        if not self.pk:
            owner_id = Owner.objects.create()
            self.owner_id = owner_id
            if 'user' in kwargs:
                self.user_owner = kwargs['user']
        super().save(*args, **kwargs)