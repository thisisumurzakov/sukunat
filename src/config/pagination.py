from rest_framework.pagination import CursorPagination, PageNumberPagination


class StandardResultsPagination(PageNumberPagination):
    page_size = 10  # default number of items per page
    page_size_query_param = "page_size"  # allows clients to override the default size
    max_page_size = 100  # maximum limit for page_size


class StandardCursorPagination(CursorPagination):
    page_size = 10  # default number of items per page
    page_size_query_param = "page_size"  # allows clients to override the default size
    max_page_size = 100  # maximum limit for page_size

    ordering = "-created_at"  # field to order by
