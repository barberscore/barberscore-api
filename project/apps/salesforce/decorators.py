from django.conf import settings

from django.contrib.auth import get_user_model

def notification_user(func):
	def wrapper(*args, **kwargs):
		User = get_user_model()
		by = User.objects.filter(id=settings.TASK_USER_ID).first()
		if 'by' not in kwargs:
			kwargs['by'] = by
		return func(*args, **kwargs)

	return wrapper

