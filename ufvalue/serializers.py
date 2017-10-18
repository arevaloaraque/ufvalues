'''
    Serializer for UF values
'''


from rest_framework import serializers, generics


from ufvalue.models import Ufvalue


class UfvalueSerializer(serializers.ModelSerializer):
    '''
        Serializer for UF values
    '''
    class Meta(object):
        '''
            Meta class
        '''
        def __init__(self):
            pass

        model  = Ufvalue
        fields = '__all__'
