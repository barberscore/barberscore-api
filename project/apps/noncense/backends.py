from .models import MobileUser


class NonceBackend(object):
    """Nonce over SMS authentication backend.

    This backend uses a simplified four-digit nonce sent over
    SMS to authenticate users.
    """

    def authenticate(self, mobile=None):
        """Authenticate over nonce service

        Authenticates if the user passes against a nonce service.
        """
        nonce_user = MobileUser(mobile)
        if nonce_user.is_authenticated():
            try:
                user = MobileUser.objects.get(mobile=mobile)
            # Note that this always creates an account.
            # Handle permissions accordingly, or raise
            # an error which this exception is thrown.
            except MobileUser.DoesNotExist:
                user = MobileUser(mobile=mobile)
                user.save()
            return user

    def get_user(self, user_id):
        try:
            return MobileUser.objects.get(pk=user_id)
        except MobileUser.DoesNotExist:
            return None
