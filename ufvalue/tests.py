'''
    Test to Ufvalue model
'''
from django.urls import reverse
from django.test import TestCase


from rest_framework.test import APIClient
from rest_framework import status


from ufvalue.models import Ufvalue


class UfValueTestCase(TestCase):
    '''
        Class for Ufvalue tests
    '''
    def setUp(self):
        '''
            Initial objects for test
        '''
        Ufvalue.objects.create(key = "01011999", value = 14685.87, date = "1999-01-01")
        Ufvalue.objects.create(key = "01021999", value = 14744.11, date = "1999-02-01")

    def test_get_objects(self):
        '''
            Test case get
        '''
        jan99 = Ufvalue.objects.get(key = "01011999")
        feb99 = Ufvalue.objects.get(key = "01021999")
        self.assertEqual(jan99.value, 14685.87)
        self.assertEqual(feb99.value, 14744.11)

    def test_update_objects(self):
        '''
            Test case update
        '''
        Ufvalue.objects.filter(key = "01011999").update(value=25650.25)
        Ufvalue.objects.filter(key = "01021999").update(value=26650.25)
        jan99 = Ufvalue.objects.get(key = "01011999")
        feb99 = Ufvalue.objects.get(key = "01021999")
        self.assertEqual(jan99.value, 25650.25)
        self.assertEqual(feb99.value, 26650.25)

    def test_delete_objects(self):
        '''
            Test case delete
        '''
        Ufvalue.objects.filter(key = "01011999").delete()
        Ufvalue.objects.filter(key = "01021999").delete()
        self.assertEqual(Ufvalue.objects.all().count(), 0)



class ApiUfValueTestCase(TestCase):
    '''
        Test for endpoints of RestFramework
    '''

    def setUp(self):
        '''
            Define the test client
        '''
        self.ufvalue = {
            "key"  : "08012017",
            "value": 26354.78,
            "date" : "2017-01-08"
        }
        self.client = APIClient()
        self.response = self.client.get(reverse('uf:uf-list'))

    def test_api_ufvalue(self):
        '''
            Test case for create, list and get an ufvalue
        '''
        self.response = self.client.post(reverse('uf:uf-list'), self.ufvalue, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

        self.response = self.client.get(reverse('uf:uf-list'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data.items()[0][1]), 1)

        self.response = self.client.get(("%s?key=08012017" % reverse('uf:uf-list')))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data.items()[0][1]), 1)
