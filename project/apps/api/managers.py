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
#     Judge,
#     Contestant,
# )


class JudgeQuerySet(QuerySet):
    def official(self):
        return self.filter(
            kind__in=[
                self.model.KIND.admin,
                self.model.KIND.music,
                self.model.KIND.presentation,
                self.model.KIND.singing,
            ]
        )

    def practice(self):
        return self.filter(
            kind__in=[
                self.model.KIND.music_candidate,
                self.model.KIND.presentation_candidate,
                self.model.KIND.singing_candidate,
            ]
        )

    def scoring(self):
        return self.filter(
            kind__in=[
                self.model.KIND.music,
                self.model.KIND.presentation,
                self.model.KIND.singing,
                self.model.KIND.music_candidate,
                self.model.KIND.presentation_candidate,
                self.model.KIND.singing_candidate,
            ]
        )

    def composite(self):
        return self.filter(
            kind__in=[
                self.model.KIND.music_composite,
                self.model.KIND.presentation_composite,
                self.model.KIND.singing_composite,
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
