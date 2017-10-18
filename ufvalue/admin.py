'''
    Register of models to admin page
'''


from django.contrib import admin


from ufvalue.models import Ufvalue


class AdminUfvalue(admin.ModelAdmin):
    '''
        Change design list of Ufvalue model
    '''
    list_display = ['pk', 'key', 'value', 'date',]
    ordering     = ['key', 'value', 'date',]


admin.site.register(Ufvalue, AdminUfvalue)
