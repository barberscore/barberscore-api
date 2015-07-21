import dedupe

# from apps.api.models import (
#     Group,
# )

from .models import (
    Collection,
    Duplicate,
)

# variables = [
#     {
#         'field': 'name',
#         'type': 'String',
#         'has missing': False,
#     },
#     {
#         'field': 'kind',
#         'type': 'String',
#         'has missing': False,
#     }
# ]


# def get_data():
#     qs = Group.objects.all()
#     data = {}
#     for q in qs:
#         data[q.id.hex] = {
#             'name': q.name,
#             'kind': q.get_kind_display(),
#         }
#     return data


def build_sample(data):
    deduper = dedupe.Dedupe(variables)
    deduper.sample(data)
    return deduper


def populate_duplicates(deduper, data):
    matches = deduper.match(data)
    for match in matches:
        collection = Collection.objects.create(
            kind='Group',
        )
        i = 0
        l = len(match[0])
        while i < l:
            Duplicate.objects.create(
                collection=collection,
                source_id=match[0][i],
            )
            i += 1
