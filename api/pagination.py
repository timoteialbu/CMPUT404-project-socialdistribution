from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
	page_size = 5
	page_size_query_param = 'size'
	max_page_size = 1000

class PostPaginator(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'results': data
        })
    
