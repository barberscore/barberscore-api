from django.contrib.auth.models import (
    BaseUserManager,
)

from django.db import (
    models,
)

# from django.db.models.query import (
#     QuerySet,
# )


# class PanelistQuerySet(QuerySet):
#     def composite(self):
#         return self.filter(category__in=[7, 8, 9])

#     def practice(self):
#         return self.filter(category__in=[4, 5, 6])

#     def scoring(self):
#         return self.filter(category__in=[1, 2, 3])

#     def administrator(self):
#         return self.filter(category=0)

#     def contest(self):
#         return self.filter(category__in=[0, 1, 2, 3])

class SessionManager(models.Manager):
    def initial(self):
        return self.order_by('-kind').first()


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
