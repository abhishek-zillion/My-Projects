from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


class ReviweFullDetailPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'info'
    page_size_query_param = 'size'
    max_page_size = 3
    last_page_strings = ('last',)

class ReviewFullDetailLimitOffsetPag(LimitOffsetPagination):
    default_limit=2
    max_limit=4
    offset_query_param='start'
    limit_query_param='limit_to'