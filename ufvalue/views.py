'''
    Views for methods related to UF values
'''
import json
import datetime


from django.shortcuts import render, redirect
from django.urls import reverse


from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response


from microservicio_valor_uf.pagination import Pagination
from ufvalue.models import Ufvalue
from ufvalue.utils import extract_historic_uf
from ufvalue.serializers import UfvalueSerializer
from ufvalue.filters import UfValueFilter


class UfvalueApi(viewsets.ModelViewSet):
    '''
        Viewset Django rest for manage of UF value model
    '''
    # queryset         = Ufvalue.objects.all().order_by('date')
    serializer_class = UfvalueSerializer
    filter_backends  = (filters.DjangoFilterBackend, SearchFilter,)
    # pagination_class = Pagination
    filter_class     = UfValueFilter
    search_fields    = '__all__'

    def get_queryset(self):
        '''
            check if year does not exist to execute robot
        '''
        queryset = Ufvalue.objects.all()
        _filters = {}

        if 'year' in self.request.GET and len(Ufvalue.objects.filter(key='3112'+self.request.GET.get('year'))) == 0:
            _filters['key__contains'] = self.request.GET.get('year')
            extract_historic_uf(self.request.GET.get('year'))
        else:
            actualyear = str(datetime.datetime.now().year)
            if len(Ufvalue.objects.filter(key='3112'+actualyear)) == 0:
                extract_historic_uf()

        if len(_filters) > 0:
            queryset = queryset.filter(**_filters).order_by('date')
        return queryset


def uf_list(request):
    '''
        Process data to list UF history by date
    '''
    data = json.loads(request.body)
    if request.method == 'POST' and 'date' in data:
        extract_historic_uf(data['date'])
    else:
        extract_historic_uf()

    return redirect(str(reverse('uf:uf-list')) + '?itemsPerPage=0&key=' + str(data['date']))


def price(request):
    '''
        Get value by date and return it to convert CLP * UF VALUE
    '''
    response = {}
    if 'value' in request.GET and 'date' in request.GET:
        try:
            response['date']  = str(request.GET.get('date'))
            response['value'] = float(request.GET.get('value'))
            _key = request.GET.get('date')[6:8] + request.GET.get('date')[4:6] + request.GET.get('date')[0:4]
            _ufvalue = Ufvalue.objects.get(key=_key)
        except Ufvalue.DoesNotExist:
            extract_historic_uf(_key)
        except Exception:
            pass

        try:
            _ufvalue             = Ufvalue.objects.get(key = _key)
            response['selected'] = UfvalueSerializer(_ufvalue, many = False).data['value']
        except Ufvalue.DoesNotExist:
            pass
    return render(request, 'base.html', {'data':response})


def index(request):
    '''
        Index template
    '''
    return render(request, 'base.html', {})
