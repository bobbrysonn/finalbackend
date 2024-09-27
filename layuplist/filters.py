""" Custom sorting logic """

import re
from rest_framework.filters import OrderingFilter


class CustomOrderingFilter(OrderingFilter):
    """Custom ordering filter for sorting course names"""

    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = super().remove_invalid_fields(queryset, fields, view, request)
        custom_fields = []
        for field in valid_fields:
            if field.lstrip("-") == "course_name":
                custom_fields.append(field)
        return custom_fields

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            for field in ordering:
                if field.lstrip("-") == "course_name":
                    reverse = field.startswith("-")
                    queryset = sorted(
                        queryset,
                        key=lambda x: int(re.search(r"\d+", x.course_name).group()),
                        reverse=reverse,
                    )
        return queryset
