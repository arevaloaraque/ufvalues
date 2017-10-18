'''
    URLs for module of UF values
'''


from django.conf.urls import url


from rest_framework import routers


from ufvalue import views


router = routers.SimpleRouter()
router.register(r'api', views.UfvalueApi, 'uf')


urlpatterns = [
    url(r'^list/$', views.index, name='list'),
    url(r'^uf_list/$', views.uf_list, name='uf_list'),
    url(r'^price/$', views.price, name='uf_price'),
]

urlpatterns += router.urls
