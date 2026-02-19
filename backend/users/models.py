from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))

        email = extra_fields.get('email')
        if email:
            email = self.normalize_email(email)
            extra_fields['email'] = email

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        CUSTOMER = 'CUSTOMER', _('Customer')
        COLLECTOR = 'COLLECTOR', _('Collector')
        PACKER = 'PACKER', _('Packer')
        COURIER_MANAGER = 'COURIER_MANAGER', _('Courier Manager')

    phone_number = models.CharField(_('phone number'), max_length=15, unique=True)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    full_name = models.CharField(_('full name'), max_length=255, blank=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    # Tracking Fields
    fbp = models.CharField(max_length=255, blank=True, null=True, help_text="Facebook Pixel Cookie")
    fbc = models.CharField(max_length=255, blank=True, null=True, help_text="Facebook Click Cookie")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []  # email is optional

    objects = UserManager()

    def __str__(self):
        return self.phone_number
