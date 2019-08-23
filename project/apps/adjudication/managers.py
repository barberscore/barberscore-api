
# Standard Library
import json
import logging
import uuid
import maya

# Third-Party
import django_rq
from algoliasearch_django.decorators import disable_auto_indexing
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Django
from django.apps import apps
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import CharField
from django.db.models import F
from django.db.models import Manager
from django.db.models import Value
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.utils.timezone import localdate
from django.utils.timezone import now

# First-Party
from phonenumber_field.validators import validate_international_phonenumber
from .validators import validate_bhs_id
from .validators import validate_tin
from .validators import validate_url


log = logging.getLogger(__name__)

validate_url = URLValidator()

validate_twitter = RegexValidator(
    regex=r'@([A-Za-z0-9_]+)',
    message="""
        Must be a single Twitter handle
        in the form `@twitter_handle`.
    """,
)

class AppearanceManager(Manager):
    def update_or_create_from_clean(self, item):
        Round = apps.get_model('adjudication.round')
        round = Round.objects.get(
            # session__convention__district=item.district,
            # session__convention__season=item.season,
            # session__convention__year=item.year,
            # session__convention__name=item.convention,
            session__kind=item.session,
            kind=item.round,
        )
        defaults = {
            'legacy_group': item.legacy_group,
        }
        return self.update_or_create(
            round=round,
            num=item.appearance_num,
            defaults=defaults,
        )


class PanelistManager(Manager):
    def update_or_create_from_clean(self, item):
        Round = apps.get_model('adjudication.round')
        round = Round.objects.get(
            # session__convention__district=item.district,
            # session__convention__season=item.season,
            # session__convention__year=item.year,
            # session__convention__name=item.convention,
            session__kind=item.session,
            kind=item.round,
        )
        defaults = {
            'status': self.model.STATUS.released,
            'kind': self.model.KIND.official,
            'legacy_person': item.legacy_person,
            'category': item.category,
        }
        return self.update_or_create(
            round=round,
            num=item.num,
            defaults=defaults,
        )


class SongManager(Manager):
    def update_or_create_from_clean(self, item):
        Appearance = apps.get_model('adjudication.appearance')
        appearance = Appearance.objects.get(
            # round__session__convention__district=item.district,
            # round__session__convention__season=item.season,
            # round__session__convention__year=item.year,
            # round__session__convention__name=item.convention,
            round__session__kind=item.session.kind,
            round__kind=item.round.kind,
            num=item.appearance_num,
        )
        # defaults = {
        #     'legacy_chart': item.legacy_chart,
        # }
        return self.update_or_create(
            appearance=appearance,
            num=item.song_num,
            defaults=defaults,
        )


class ScoreManager(Manager):
    def update_or_create_from_clean(self, item):
        song = item.cleansong.song
        panelist = item.cleanpanelist.panelist
        defaults = {
            'points': item.points,
        }
        return self.update_or_create(
            song=song,
            panelist=panelist,
            defaults=defaults,
        )
