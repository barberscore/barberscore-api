# from optparse import make_option

# from django.core.management.base import (
#     BaseCommand,
#     CommandError,
# )

# from apps.api.models import (
#     Person,
#     Singer,
#     Director,
#     Arranger,
# )


# class Command(BaseCommand):
#     help = "Merge selected singers by name"
#     option_list = BaseCommand.option_list + (
#         make_option(
#             "-o",
#             "--old",
#             dest="old",
#             help="specify old name",
#         ),
#     )
#     option_list = option_list + (
#         make_option(
#             "-n",
#             "--new",
#             dest="new",
#             help="specify new name",
#         ),
#     )

#     def handle(self, *args, **options):
#         # make sure file option is present
#         if options['old'] is None:
#             raise CommandError("Option `--old=...` must be specified.")

#         if options['new'] is None:
#             raise CommandError("Option `--new=...` must be specified.")

#         # make sure both singers exist
#         try:
#             new_person = Person.objects.get(
#                 name__iexact=options['new'],
#             )
#         except Person.DoesNotExist:
#             raise CommandError("New person does not exist.")
#         try:
#             old_person = Person.objects.get(
#                 name__iexact=options['old'],
#             )
#         except Singer.DoesNotExist:
#             raise CommandError("Old person does not exist.")

#         # Move related records
#         for director in old_person.choruses.all():
#             Director.objects.create(
#                 person=new_person,
#                 performer=director.performer,
#                 part=director.part,
#             )
#         for singer in old_person.quartets.all():
#             Singer.objects.create(
#                 person=new_person,
#                 performer=singer.performer,
#                 part=singer.part,
#             )

#         for arranger in old_person.catalogs.all():
#             Arranger.objects.create(
#                 person=new_person,
#                 chart=arranger.chart,
#                 part=arranger.part,
#             )

#         # remove redundant singer
#         try:
#             old_person.delete()
#         except Exception as e:
#             raise CommandError("Error deleted old singer: {0}".format(e))

#         return "Merged {0} into {1}".format(old_person, new_person)
