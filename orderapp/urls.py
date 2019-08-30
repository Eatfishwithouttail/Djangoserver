from django.urls import path, re_path
from django.conf.urls import url
from orderapp.views import order_list, cancel_order, search, query

app_name ='orderapp'





urlpatterns = [
    path('list/<order_num>/<city_code>',order_list,name='list'),
    path('cancel/<uuid:order_num>',cancel_order,name='cancel'),
    # url(r'^list2/(\w+)/(\d+)$',order_list)
    # re_path(r'^search/(?P<phone>1[3-57-9][\d]{9})$',search)
    re_path(r'^search/(?P<email>(\w+[@]\w+.[\w]+))',search,name='search'),
    path('query',query)
]