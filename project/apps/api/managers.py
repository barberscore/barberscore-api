# Django
from django.contrib.auth.models import BaseUserManager
from django.db.models import (
    Manager,
    Sum,
    QuerySet,
)

# from django.apps import apps
# Score = apps.get_model('api', 'Score')



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


class ScoreQuerySet(QuerySet):
    def officials(self):
        return self.exclude(
            points=None,
        ).exclude(
            kind=self.model.KIND.practice,
        )
        # .order_by(
        #     'category',
        # ).values(
        #     'category',
        # ).annotate(
        #     total=models.Sum('points'),
        #     average=models.Avg('points'),
        # )


class ScoreManager(Manager):
    def get_queryset(self):
        return ScoreQuerySet(self.model, using=self._db)

    def official_totals(self):
        return self.get_queryset().officials().aggregate(
            s=Sum('points'))['s']
