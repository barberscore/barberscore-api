import logging
log = logging.getLogger('apps.convention')

from django.contrib.auth import get_user_model

User = get_user_model()


class MobileBackend(object):
    def authenticate(self, mobile):
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User(
                mobile=mobile,
            )
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
