'''
    Filters for Ufvalue through django rest
'''


from django_filters import FilterSet, CharFilter


from ufvalue.models import Ufvalue


class UfValueFilter(FilterSet):
    '''
        Filter for Ufvalue
    '''
    key = CharFilter(lookup_expr='icontains')
    class Meta(object):
        '''
            Meta class
        '''
        model  = Ufvalue
        fields = {
            'date': ['exact'],
        }
