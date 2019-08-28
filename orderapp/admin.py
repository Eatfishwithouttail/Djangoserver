import xadmin
from django.contrib import admin
from orderapp.models import OrderModel,OrderDetail,OrderAddress

# Register your models here.



class OrderAdmin(object):
    list_display = ("num",'user_id',"address_id",'title')


class OrderDetailAdmmin(object):
    list_display = ('id','num','goods_id','cnt','get_price1','get_price','pay_type','pay_status')
    def get_price(self, obj):
        return obj.price
    get_price.short_description = "小计"
    def get_price1(self, obj):
        return obj.price1
    get_price1.short_description = "单价"


class OrderAddressAdmin(object):
    list_display = ('id','user_id','receiver','receiver_phone','receiver_phone')



xadmin.site.register(OrderModel,OrderAdmin)
xadmin.site.register(OrderAddress,OrderAddressAdmin)
xadmin.site.register(OrderDetail,OrderDetailAdmmin)