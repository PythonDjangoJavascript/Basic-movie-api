from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)


class StanderedPNumPagination(PageNumberPagination):
    page_size = 3
    # page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10
    # last_page_strings = 'last'  # default is 'end'


class StanderdLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    limit_query_param = 'limit'  # default is also limit
    offset_query_param = 'start'  # default if 'ofset'
    max_limit = 5


class StanderdCursorPagination(CursorPagination):

    page_size = 4
    cursor_query_param = 'record'  # default is record
    ordering = '-crated_at'
