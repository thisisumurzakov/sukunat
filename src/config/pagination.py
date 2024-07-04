from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    page_size = 10  # default number of items per page
    page_size_query_param = "page_size"  # allows clients to override the default size
    max_page_size = 100  # maximum limit for page_size


class StandardCursorPagination(CursorPagination):
    page_size = 10  # default number of items per page
    page_size_query_param = "page_size"  # allows clients to override the default size
    max_page_size = 100  # maximum limit for page_size

    ordering = "-created_at"  # field to order by

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.encode_cursor(self.get_next_link()),
                "previous": self.encode_cursor(self.get_previous_link()),
                "results": data,
            }
        )

    def encode_cursor(self, url):
        if url is None:
            return None
        # Extract the cursor value from the URL
        return url.split("cursor=")[-1]
