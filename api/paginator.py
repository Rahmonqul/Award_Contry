from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# class AwardPagination(PageNumberPagination):
#     page_size = 2  # Количество наград на одной странице
#     page_size_query_param = 'page_size'
#     max_page_size = 100  # Максимальное количество наград на странице
#
#     def get_paginated_response(self, data):
#         return Response({
#             'count': self.page.paginator.count,  # Общее количество наград
#             'next': self.get_next_link(),  # Ссылка на следующую страницу
#             'previous': self.get_previous_link(),  # Ссылка на предыдущую страницу
#             'results': data  # Результаты текущей страницы
#         })

class DecisionPagination(PageNumberPagination):
    page_size = 3  # Количество решений на одной странице
    page_size_query_param = 'page_size'
    max_page_size = 100  # Максимальное количество решений на одной странице

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Общее количество решений
            'next': self.get_next_link(),  # Ссылка на следующую страницу
            'previous': self.get_previous_link(),  # Ссылка на предыдущую страницу
            'results': data  # Результаты текущей страницы
        })


class AwardPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Общее количество решений
            'next': self.get_next_link(),  # Ссылка на следующую страницу
            'previous': self.get_previous_link(),  # Ссылка на предыдущую страницу
            'results': data  # Результаты текущей страницы
        })