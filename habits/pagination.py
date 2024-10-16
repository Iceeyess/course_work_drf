from rest_framework import pagination


class FiveHabitsOnPage(pagination.PageNumberPagination):
    """Класс-пагинации. По заданию должно быть по 5 элементов на странице"""
    page_size = 5  # кол-во элементов на странице
    page_size_query_param = 'page_size'  # Параметр запроса для указания количества элементов
    max_page_size = 5
