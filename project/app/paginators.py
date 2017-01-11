from collections import OrderedDict
from rest_framework import serializers
from rest_framework.views import Response
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)
from rest_framework.utils.urls import remove_query_param, replace_query_param

class PersonPaginator(PageNumberPagination):
    """
    A json-api compatible pagination format
    NOTE: Meta is not built nbormally.
    """
    page_size = 10
    page_size_query_param = 'per'
    max_page_size = 1000

    def build_link(self, index):
        if not index:
            return None
        url = self.request and self.request.build_absolute_uri() or ''
        return replace_query_param(url, 'page', index)

    def get_paginated_response(self, data):
        next = None
        previous = None

        if self.page.has_next():
            next = self.page.next_page_number()
        if self.page.has_previous():
            previous = self.page.previous_page_number()

        return Response({
            'results': data,
            'meta': OrderedDict([
                ('page', self.page.number),
                ('total_pages', self.page.paginator.num_pages),
            ]),
            'links': OrderedDict([
                ('first', self.build_link(1)),
                ('last', self.build_link(self.page.paginator.num_pages)),
                ('next', self.build_link(next)),
                ('prev', self.build_link(previous))
            ]),
        })

