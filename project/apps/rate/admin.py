from django.contrib import admin

from .models import (
    Rating,
)


class RatingAdmin(admin.ModelAdmin):
    save_on_top = True
    raw_id_fields = ['performance']
    list_display = ['user', 'performance', 'song_one', 'song_two']
    list_filter = ['user']

admin.site.register(Rating, RatingAdmin)
