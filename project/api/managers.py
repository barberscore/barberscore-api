# Django
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, person, password='', **kwargs):
        user = self.model(
            email=email,
            name=person.name,
            person=person,
            password='',
            is_active=True,
            **kwargs
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, email, person, password, **kwargs):
        user = self.model(
            email=email,
            name=person.name,
            person=person,
            is_staff=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
