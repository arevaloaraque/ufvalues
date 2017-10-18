'''
    Global pagination
'''


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    '''
        Pagination class to prevent long time when loading records
    '''
    page_size             = 20
    page_size_query_param = 'itemsPerPage'
    max_page_size         = 1000

    def get_paginated_response(self, data):
        '''
            Pagination setting
        '''
        return Response({
            'paginate': {
                'currentPage'  : self.page.number,
                'totalItems'   : self.page.paginator.count,
                'itemsPerPage' : self.page.paginator.per_page,
                'num_pages'    : self.page.paginator.num_pages,
            },
            'items': data
        })

    def get_page_size(self, request):
        '''
            Return total page
        '''
        if self.page_size_query_param:
            page_size = min(int(request.query_params.get(self.page_size_query_param, self.page_size)), self.max_page_size)
            if page_size > 0:
                return page_size
            elif page_size == 0:
                return None
            else:
                pass

        return self.page_size
