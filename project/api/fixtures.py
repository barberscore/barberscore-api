import json
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

# First-Party
from api.models import (
    Award,
    Chart,
    Entity,
    Office,
)

def dump_entities():
    with open('entities.json', 'w') as f:
        qs = Entity.objects.filter(
            kind__lt=30,
            status=Entity.STATUS.active,
        ).order_by(
            'kind',
            'name',
        )
        serialize(
            'json',
            qs,
            fields = (
                'name',
                'status',
                'kind',
                'age',
                'is_novice',
                'short_name',
                'long_name',
                'code',
                'start_date',
                'end_date',
                'location',
                'website',
                'facebook',
                'twitter',
                'email',
                'phone',
                'description',
                'notes',
                'bhs_id',
                'parent',
            ),
            stream=f,
            cls=DjangoJSONEncoder,
        )


def dump_charts():
    with open('charts.json', 'w') as f:
        qs = Chart.objects.all()
        serialize(
            'json',
            qs,
            fields = (
                'status',
                'bhs_id',
                'title',
                'published',
                'composers',
                'lyricists',
                'arrangers',
                'holders',
                'entity',
            ),
            stream=f,
            cls=DjangoJSONEncoder,
        )


def dump_offices():
    with open('offices.json', 'w') as f:
        qs = Office.objects.filter(
            status=Office.STATUS.active,
        )
        serialize(
            'json',
            qs,
            fields = (
                'name',
                'status',
                'kind',
                'is_cj',
                'is_jc',
                'is_ml',
                'is_drcj',
                'is_ca',
                'is_rep',
                'short_name',
                'long_name',
            ),
            stream=f,
            cls=DjangoJSONEncoder,
        )


def dump_awards():
    with open('awards.json', 'w') as f:
        qs = Award.objects.filter(
            status=Award.STATUS.active,
        )
        serialize(
            'json',
            qs,
            fields = (
                'name',
                'status',
                'kind',
                'age',
                'season',
                'is_qualifier',
                'is_primary',
                'is_improved',
                'is_novice',
                'is_manual',
                'is_multi',
                'is_district_representative',
                'rounds',
                'threshold',
                'minimum',
                'advance',
                'entity',
                'parent',
            ),
            stream=f,
            cls=DjangoJSONEncoder,
        )
