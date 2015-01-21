# import pytz

# from django.utils import timezone


# class TimezoneMiddleware(object):
#     def process_request(self, request):
#         try:
#             tzname = request.user.profile.timezone
#         except:
#             tzname = None
#         if tzname:
#             timezone.activate(pytz.timezone(tzname))
#         else:
#             timezone.deactivate()
