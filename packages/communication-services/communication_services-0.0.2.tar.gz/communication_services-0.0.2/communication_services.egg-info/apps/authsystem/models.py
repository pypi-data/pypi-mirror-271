from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
import uuid as uuid_package
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from organization import models as org_models
from django.core import exceptions


def validate_file(value):
    if value.size > 10 * 1024 * 1024:
        raise exceptions.ValidationError(_("file should not bigger than 10 mb"))


def get_file_loc(instance, filename):
    time_hierarchy = f"{instance.created.strftime('%Y')}/{instance.created.strftime('%m')}/{instance.created.strftime('%d')}"

    return f"avatar/{time_hierarchy}/{filename}"


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, known languages and password.
        """
        if not username and not extra_fields.get("phone_number"):
            raise ValueError("Users must have an username address or phone number")

        user = self.model(username=username, is_active=True, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(username, password=password, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid_package.uuid4)
    username = models.CharField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255, blank=True, default="")
    cellphone = models.CharField(max_length=20, null=True, unique=True)
    email = models.EmailField(unique=True, null=True)
    # org = models.ManyToManyField(
    #     org_models.Organization, through=org_models.UserOrganization
    # )
    avatar = models.FileField(
        upload_to=get_file_loc, validators=[validate_file], null=True, blank=True
    )
    created = models.DateTimeField(
        verbose_name=_("the date this user is created in database"),
        default=timezone.now,
    )
    modified = models.DateTimeField(
        verbose_name=("the date this user info being updated in database"),
        null=True,
        blank=True,
    )
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.username:
            return self.username
        else:
            return str(self.id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return super().has_perm(perm, obj=obj)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return super().has_module_perms(app_label)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super().save(*args, **kwargs)

    def reset_password(self):
        self.set_password(self.username)
        self.save()

    class Meta:
        ordering = ["-created"]
