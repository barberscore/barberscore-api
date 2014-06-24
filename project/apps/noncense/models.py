from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None):
        """
        Creates and saves a User with the given mobile number.
        Password is optional.
        """

        if not mobile:
            raise ValueError("Users must have a mobile phone.")

        user = self.model(
            mobile=mobile,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        """
        Creates and saves a superuser with the given mobile number
        and password.
        """
        user = self.create_user(
            mobile=mobile,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    mobile = models.CharField(
        verbose_name='mobile number',
        help_text="""
            The mobile number of the User.""",
        max_length=20,
        unique=True,
    )

    full_name = models.CharField(
        verbose_name="Full Name",
        help_text="""
            The Full Name of the User.""",
        blank=True,
        null=True,
        max_length=100,
    )

    is_staff = models.BooleanField(
        default=False,
        help_text="""
            Designates whether the user can log into this admin site """,
    )

    is_active = models.BooleanField(
        default=True,
        help_text="""
            Designates whether this user should be treated as active.
            Unselect this instead of deleting accounts."""
    )

    is_superuser = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # Full name, if available
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email
        return self.mobile

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    def __unicode__(self):
        return self.mobile


class TwilioMessage(models.Model):
    MessageSid = models.CharField(
        max_length=34,
        null=True,
        blank=True,
    )

    From = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    To = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    Body = models.CharField(
        max_length=1600,
        null=True,
        blank=True,
    )

    # def __unicode__(self):
    #     return self.MessageSid
