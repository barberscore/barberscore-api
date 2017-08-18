# Django
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password='', person, **kwargs):
        user = self.model(
            email=email,
            password='',
            person=person,
            is_active=True,
            **kwargs
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, person, **kwargs):
        user = self.model(
            email=email,
            person=person,
            is_staff=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
