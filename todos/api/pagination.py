from rest_framework.pagination import PageNumberPagination

class TodoPagination(PageNumberPagination):
    page_size = 5