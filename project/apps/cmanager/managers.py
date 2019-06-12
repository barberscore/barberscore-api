
# Standard Library
import logging
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.core.files.base import ContentFile

# Django
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from django.db.models import F
from django.db.models import Manager


log = logging.getLogger(__name__)

validate_url = URLValidator()

validate_twitter = RegexValidator(
    regex=r'@([A-Za-z0-9_]+)',
    message="""
        Must be a single Twitter handle
        in the form `@twitter_handle`.
    """,
)


class AwardManager(Manager):
    def sort_tree(self):
        self.all().update(tree_sort=None)
        awards = self.order_by(
            '-status',  # Actives first
            'group__tree_sort',  # Basic BHS Hierarchy
            '-kind', # Quartet, Chorus
            'gender', #Male, mixed
            F('age').asc(nulls_first=True), # Null, Senior, Youth
            'level', #Championship, qualifier
            'is_novice',
            'name', # alpha
        )
        i = 0
        for award in awards:
            i += 1
            award.tree_sort = i
            award.save()
        return

    def get_awards(self):
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'ID',
            'Name',
            'Kind',
            'Gender',
            'Season',
            'Level',
            'Single',
            'Threshold',
        ]
        ws.append(fieldnames)
        awards = self.filter(
            status__gt=0,
        ).order_by('tree_sort')
        for award in awards:
            pk = str(award.id)
            name = award.name
            kind = award.get_kind_display()
            gender = award.get_gender_display()
            season = award.get_season_display()
            level = award.get_level_display()
            single = award.is_single
            threshold = award.threshold
            row = [
                pk,
                name,
                kind,
                gender,
                season,
                level,
                single,
                threshold,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content
