from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlparse, parse_qs


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
                "next": self.get_cursor_value(self.get_next_link()),
                "previous": self.get_cursor_value(self.get_previous_link()),
                "results": data,
            }
        )

    def get_cursor_value(self, url):
        if url is None:
            return None
        # Parse the URL and extract the cursor value
        parsed_url = urlparse(url)
        cursor_value = parse_qs(parsed_url.query).get("cursor")
        return cursor_value[0] if cursor_value else None
