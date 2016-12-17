# Django
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **kwargs):
        user = self.model(
            username=username,
            password=None,
            is_active=True,
            **kwargs
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.model(
            username=username,
            is_staff=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
