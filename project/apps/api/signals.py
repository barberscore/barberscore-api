# from django.db.models.signals import (
#     post_save,
# )

# from django.dispatch import receiver

# from .models import (
# )


# @receiver(post_save, sender=Contestant)
# def contestant_post_save(sender, instance=None, created=False, raw=False, **kwargs):
#     """Denormalization to create protected class."""
#     if not raw:
#         if created:
#             ContestantScore.objects.create(
#                 contestant=instance,
#             )
