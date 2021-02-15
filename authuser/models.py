from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from django.urls import reverse
from django.utils.translation import gettext as _
from tickets.models import Tickets
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
# Create your models here.

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class AuthUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, phone_number, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_complete_user(self, 
                            username, 
                            email, 
                            phone_number, 
                            roles,
                            dept=None,
                            skill=None,
                            password=None):
        if not phone_number:
            raise ValueError('Users must have a phone')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=AuthUserManager.normalize_email(email),
            phone_number=phone_number,
            password=password,
            roles=roles,
            dept=dept,
            skill=skill
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'

# PERMISSIONS CLASS
class AuthPermissions (models.Model):
    """
    Create Permissions for various Roles
    """
    perm_name = models.CharField(_("Permission Name"),max_length=30, unique=True, blank=False)
    perm_description = models.TextField(_("Permission Description"))
    permission_uuid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="PermissionsAuth")

    class Meta:
        verbose_name = _("authperm")
        verbose_name_plural = _("authperms")

    def __str__(self):
        return self.perm_name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

# CREATE A ROLE CLASS FOR ROLES
class Role(models.Model):
    """
    Assign Roles to users based on the Permissions Matrix in AuthPermissions
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="role")
    # permissions = models.ManyToManyField("AuthPermissions", blank=True, verbose_name="role_permissions")
    tickets = models.ManyToManyField(Tickets, blank=True, verbose_name="ticketing_role")
    desc = models.TextField(_("Role Description"))
    

    class Meta:
        verbose_name = _("role")
        verbose_name_plural = _("roles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

    
USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'
# CREATE USER CLASS AND INHERIT AbstractBaseUSer 
class User(AbstractBaseUser):
    SUPERADMIN = 'supadmin'
    ADMIN = 'admin'
    MEMBER = 'member'
    ANONYMOUS = 'anon'
    API_USER = 'api_user' # TO BE MATCHED AGAINST API KEYS

    ROLE = (
        (SUPERADMIN, _('Super User')),
        (ADMIN, _('Admin User')),
        (MEMBER, _('Member')),
        (ANONYMOUS, _('Anonymous')),
        (API_USER, _('API User')),
    )

    email = models.EmailField(_('Email Address'), unique=True, blank=False)
    username = models.CharField(max_length=255, unique=True, validators=[RegexValidator(
        regex=USERNAME_REGEX,
        message='name must be Alphanumeric or contain any of the following: ". @ + -" ',
        code='invalid_name'
    )])
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    supervisor = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="supervisor")
    # roles = models.ManyToManyField("Role", verbose_name="user_role", blank=True) TO BE USED WITH THE ABOVE PREFILLED ROLES MODEL
    image = models.ImageField(upload_to="static/%Y/%m/%D", default="images/default.svg",
                              max_length=100, null=True, blank=True) # THIs SHOULD PROBABLY BE OFFLOADED TO A THIRD PARTY SITE LIKE CLOUDINARY OR DROPBOX
    phone_number = models.CharField(_("Phone Number"), max_length=15) # USE THIS TO SEND TICKET VERIFICATIONS USING SHORTCODE OR 2fACTOR AUTH FOR PAYMENTS
    roles = models.CharField(choices=ROLE, max_length=50, blank=True, default='member')
    dept = models.CharField(max_length=50, blank=True, null=True)
    skill = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    def getFullName(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        user_name = self.username
        if user_name == "":
            return self.email
        else:
            return user_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['first_name']