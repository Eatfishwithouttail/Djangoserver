import xadmin
from django.contrib import admin
from orderapp.models import OrderModel

# Register your models here.



class OrderAdmin(object):
    list_display = ("num","title","price","pay_status","receiver","receiver_phone","receiver_address")
    fields = ("num","title","price","pay_status","receiver","receiver_phone","receiver_address")
    list_filter = ('pay_status',)






xadmin.site.register(OrderModel,OrderAdmin)