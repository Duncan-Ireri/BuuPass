from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from django.urls import reverse
from django.utils.translation import gettext as _
from tickets.models import Tickets
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app 
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)  # change password to hash
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

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

    

# CREATE USER CLASS AND INHERIT AbstractUSer 
class User(AbstractUser):
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
    username = models.CharField(_("username"), max_length=50)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    supervisor = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="supervisor")
    # roles = models.ManyToManyField("Role", verbose_name="user_role", blank=True) TO BE USED WITH THE ABOVE PREFILLED ROLES MODEL
    image = models.ImageField(upload_to="static/%Y/%m/%D", default="images/default.svg",
                              max_length=100, null=True, blank=True) # THIs SHOULD PROBABLY BE OFFLOADED TO A THIRD PARTY SITE LIKE CLOUDINARY OR DROPBOX
    phone_number = models.CharField(_("Phone Number"), max_length=15) # USE THIS TO SEND TICKET VERIFICATIONS USING SHORTCODE OR 2fACTOR AUTH FOR PAYMENTS
    roles = models.CharField(choices=ROLE, max_length=50, blank=True, default='member')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def getFullName(self):
        return self.first_name + " " + self.last_name

    def __str__(self) -> str:
        return self.getFullName()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['first_name']