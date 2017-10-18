'''
    Methods to use in any point at the App
'''
import json
from datetime import datetime


import requests
from pyquery import PyQuery as pq


from ufvalue.models import Ufvalue


requests.packages.urllib3.disable_warnings()
DATA_REQUEST  = {
    'Opcion'               : '1',
    'idMenu'               : 'UF_IVP_DIARIO',
    'codCuadro'            : 'UF_IVP_DIARIO',
    'DrDwnAnioDesde'       : '1977',
    'DrDwnAnioHasta'       : datetime.now().year,
    'DrDwnAnioDiario'      : datetime.now().year,
    'DropDownListFrequency': 'DAILY',
    'DrDwnCalculo'         : 'NONE',
}
LIST_FILTER = []


def extract_historic_uf(date = datetime.now().year):
    '''
        Method to extract history of the UF values from the central bank of Chile
    '''
    session      = requests.session()
    homepage     = session.get('http://si3.bcentral.cl/Siete/secure/cuadros/home.aspx')
    dom_homepage = pq(homepage.content.replace('\n', '').replace('\t', '').replace('xmlns', ''))
    request_data = {
        '__EVENTTARGET'  : 'lnkBut01',
        '__EVENTARGUMENT': ''
    }
    LIST_FILTER = Ufvalue.objects.filter(key__contains=date).values_list('key', flat=True)
    for _input in dom_homepage.find('input'):
        if not _input.attrib['name'] == '__EVENTTARGET' and not _input.attrib['name'] == '__EVENTARGUMENT':
            try:
                request_data[_input.attrib['name']] = _input.attrib['value']
            except KeyError:
                request_data[_input.attrib['name']] = ''

    session.post('http://si3.bcentral.cl/Siete/secure/cuadros/home.aspx', data=request_data)
    session.get('http://si3.bcentral.cl/Siete/secure/cuadros/arboles.aspx')

    data_history = {}
    DATA_REQUEST['DrDwnAnioDiario'] = date
    data = session.get('http://si3.bcentral.cl/Siete/secure/cuadros/actions.aspx', params=DATA_REQUEST)
    try:
        data = json.loads(data.content)
        data_history[date] = []
        data_history[date].append(data['Grid'][0])
        proccess_data(data_history)
    except Exception:
        pass
    
    # clean data
    if len(data_history) > 0:
        return True


def proccess_data(data):
    '''
        Method to process data extracted from bcentral and deleting existing records
    '''
    excluded = ['Meta', 'Reg', 'nombre', 'seriesId', 'spanish_title', 'Date']
    months   = {
        'Ene' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Abr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Ago' : '08',
        'Sep' : '09',
        'Oct' : '10',
        'Nov' : '11',
        'Dic' : '12',
    }
    for index in data:
        for dict_ in data[index]:
            for key, value in dict_.iteritems():
                if key not in excluded:
                    date = key.split('.')
                    pkey = str(date[0]) + str(months[date[1]]) + str(date[2])
                    date = datetime(int(date[2]), int(months[date[1]]), int(date[0])).date()
                    if not pkey in LIST_FILTER:
                        Ufvalue.objects.get_or_create(key=pkey, defaults={
                            'key'  : pkey,
                            'date' : date,
                            'value': value
                        })
                else:
                    continue

    return True
