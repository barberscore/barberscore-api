from django.contrib.auth.models import (
    BaseUserManager,
)

from django.db import (
    models,
)

from django.db.models.query import (
    QuerySet,
)

# from .models import (
#     Panelist,
#     Contestant,
# )


class PanelistQuerySet(QuerySet):
    def official(self):
        return self.filter(
            category__in=[
                self.model.CATEGORY.admin,
                self.model.CATEGORY.music,
                self.model.CATEGORY.presentation,
                self.model.CATEGORY.singing,
            ]
        )

    def practice(self):
        return self.filter(
            category__in=[
                self.model.CATEGORY.music_candidate,
                self.model.CATEGORY.presentation_candidate,
                self.model.CATEGORY.singing_candidate,
            ]
        )

    def scoring(self):
        return self.filter(
            category__in=[
                self.model.CATEGORY.music,
                self.model.CATEGORY.presentation,
                self.model.CATEGORY.singing,
                self.model.CATEGORY.music_candidate,
                self.model.CATEGORY.presentation_candidate,
                self.model.CATEGORY.singing_candidate,
            ]
        )

    def composite(self):
        return self.filter(
            category__in=[
                self.model.CATEGORY.music_composite,
                self.model.CATEGORY.presentation_composite,
                self.model.CATEGORY.singing_composite,
            ]
        )


class ContestantQuerySet(QuerySet):
    def accepted(self):
        return self.filter(
            status=self.model.STATUS.accepted,
        )

    def official(self):
        return self.filter(
            status=self.model.STATUS.official,
        )


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
