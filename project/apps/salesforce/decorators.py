from django.conf import settings

def notification_user(func):
	def wrapper(*args, **kwargs):
		if 'by' not in kwargs:
			kwargs['by'] = settings.TASK_USER_ID
		return func(*args, **kwargs)

	return wrapper
