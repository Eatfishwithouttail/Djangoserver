from django.contrib import admin
from mainapp.models import UserEntity, CateTypeEntity, FruitEntity, StoreEntity, FruitImageEntty,RealProfile,Cart,FruitCartEntity
# Register your models here.
import xadmin


#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'age', 'phone')
#     list_per_page = 3
#     list_filter = ('id', 'age')
#     search_fields = ('id', 'phone')
#
# class CateTypeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'order_num')
#
# class FruitAdmin(admin.ModelAdmin):
#     list_display = ('name', 'source','price', 'category')
# class StoreAdmin(admin.ModelAdmin):
#     list_display = ('name', 'boss_name', 'phone', 'address')
# class FruitImageAdmin(admin.ModelAdmin):
#     list_display = ('fruit_id', 'url','name')
#
# admin.site.register(UserEntity, UserAdmin)
# admin.site.register(CateTypeEntity, CateTypeAdmin)
# admin.site.register(FruitEntity, FruitAdmin)
# admin.site.register(FruitImageEntty, FruitImageAdmin)
# admin.site.register(StoreEntity, StoreAdmin)
#

class UserAdmin(object):
    list_display = ('id', 'name', 'age', 'phone')
    list_per_page = 3
    list_filter = ('id', 'age')
    search_fields = ('id', 'phone')


class CateTypeAdmin(object):
    list_display = ('id', 'name', 'order_num')


class FruitAdmin(object):
    list_display = ('id', 'name', 'source', 'price', 'category')


class StoreAdmin(object):
    # readonly_fields = ('id',)
    list_display = ('id_', 'name', 'boss_name', 'city','phone', 'address','store_type', 'logo', 'opened','open_time')
    # 指定表单修改的字段
    fields = ('name', 'boss_name', 'city','phone', 'address','store_type', 'logo', 'summary', 'opened')

class FruitImageAdmin(object):
    list_display = ('id', 'fruit_id', 'url', 'name')

class RealProfilelAdmin(object):
    list_display = ('user','real_name','number','real_type','image1','image2')

class CartAdmin(object):
    list_display = ('user','no')

class FruitCartEntityAdmin(object):
    list_display = ('cart','fruit','get_price1','cnt','get_price')

    def get_price1(self,obj):
        return obj.price1

    get_price1.short_description = "单价"

    def get_price(self, obj):
        return obj.price

    get_price.short_description = "小计"




xadmin.site.register(UserEntity, UserAdmin)
xadmin.site.register(CateTypeEntity, CateTypeAdmin)
xadmin.site.register(FruitEntity, FruitAdmin)
xadmin.site.register(FruitImageEntty, FruitImageAdmin)
xadmin.site.register(StoreEntity, StoreAdmin)
xadmin.site.register(RealProfile, RealProfilelAdmin)
xadmin.site.register(Cart, CartAdmin)
xadmin.site.register(FruitCartEntity, FruitCartEntityAdmin)
