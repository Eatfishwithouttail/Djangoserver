from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def order_list(request,order_num,city_code):
    print(order_num,city_code)
    return render(request,'list_order.html',locals())




def cancel_order(request,order_num):
    #order_num订单编号是uuid类型的
    print(order_num)
    return render(request,'list_order.html',locals())


def search(request,email):
    phone = email
    return render(request,'list_order.html',locals())


def query(request):
    #查询参数中的code（1.按城市city和订单num查询），2.按手机号查询
    url = reverse('order:search',args=('870815471@qq.com',))
    # url = reverse('order:search',kwargs=dict(city_code=1000,order_num=1000))
    return HttpResponse('hi,query%s'%url)
