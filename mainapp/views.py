import os
from datetime import datetime

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from helloDjango import settings
from mainapp.models import UserEntity, FruitEntity, FruitImageEntty, StoreEntity
from django.db.models import Count, Sum, Min, Avg, Max, F, Q


# Create your views here.
def user_list(request):
    users = [
        {
            'id': 101,
            'name': 'tomas'
        },
        {
            'id': 102,
            'name': 'ben'
        },
        {
            'id': 103,
            'name': 'toni'
        }
    ]

    return render(request, 'user/list.html', locals())


def user_list2(request):
    users = UserEntity.objects.all()
    return render(request, 'user/list.html', locals())


def add_user(request):
    name = request.GET.get('name', default=None)
    age = request.GET.get('age', default=0)
    phone = request.GET.get('phone', default=None)
    # 验证数据是否完整
    if all((name, age, phone)):
        UserEntity(name=name, age=age, phone=phone).save()
    else:
        return HttpResponse('<h3 style="color:red;">用户信息不完整！</h3>', status=400)
    return redirect('/user/list2/')


def user_update(request):
    # 查询参数有id， name, phone
    # 通过模型查询id用户是否存在，Model类.objects.get()可能会出现异常 -- 尝试捕获
    id = request.GET.get('id', default=0)
    name = request.GET.get('name', default=None)
    age = request.GET.get('age', default=0)
    phone = request.GET.get('phone', default=None)
    if id and any((name, age, phone)):
        try:
            u = UserEntity.objects.get(pk=int(id))
        except Exception as e:
            return HttpResponse('<h3 style="color:red;">用户不存在！</h3>')
        if name:
            u.name = name
        if phone:
            u.phone = phone
        if age:
            u.age = age
        u.save()
        return redirect('/user/list2/')
    else:
        return HttpResponse('<h3 style="color:red;">参数不完整！</h3>', status=400)


def user_delete(request):
    # 查询参数有id
    # 验证id是否存在
    id = request.GET.get('id', default=0)
    if not id:
        return HttpResponse('<h3 style="color:red;">参数不完整！</h3>', status=400)
    try:
        u = UserEntity.objects.get(pk=int(id))
    except:
        return HttpResponse('<h3 style="color:red;">用户不存在！</h3>')
    u.delete()
    return redirect('/user/list2/')


def get_fruit_all(request):
    data = []
    fruits = FruitEntity.objects.all()
    for f in fruits:
        for img in FruitImageEntty.objects.all():
            print(f.name, img.fruit_id, f.id == img.fruit_id.id)
            if f.id == img.fruit_id.id:
                data.append({
                    'fruit':f,
                    'img':img
                })
                break
    print(data)
    return render(request, 'fruit/index.html', locals())


def find_fruit(request):
    price1 = request.GET.get('price1',0)
    price2 = request.GET.get('price2',1000)
    print(price1,price2)
    username = request.COOKIES.get('login_name')
    if not username:
        return redirect('/user/login')
    #从查询参数中获取价格区间price1，price2
    # result1 = FruitEntity.objects.filter(price__gte=price1,price__lte=price2).\
    #                                             exclude(price=250).all()

    # result = FruitImageEntty.objects.values('url','fruit_id__name','fruit_id__price','fruit_id__source').filter(fruit_id__price__gte=price1,fruit_id__price__lte=price2).all()
    result = FruitEntity.objects.values('name','price','source','fruitimageentty__url').filter(price__gte=price1,price__lte=price2).all()

    print(result)
    # .filter(name__contains='果')
    # images = FruitImageEntty.objects.get(id=1)
    # image =  images.fruit_id


    #根据我们价格区间来查找满足条件的所有水果信息
    #将查询到的数据渲染到模板上
    return render(request,'fruit/afterlog.html',locals())

def find_store(request):
    user = UserEntity.objects.all()
    msg = "最优秀的学员"

    info = '<h3>lallala</h3>'
    size = os.path.getsize('mainapp/models.py')
    file_dir = os.path.join(settings.BASE_DIR,'mainapp/')
    files = {path:os.stat(file_dir+path) for path in os.listdir(file_dir) if os.path.isfile( file_dir + path)}
    #加载模板
    template = loader.get_template('store/list.html')
    html = template.render(context={
        'msg':msg,
        'users':user,
        'info':info,
        'time':datetime.now(),
        "file":files,
        "float":19.13549
    })

    return  HttpResponse(html,status=200)  #增加响应头？？？



def all_store(request):
    #返回所有的水果店的json数据
    result = {}
    if StoreEntity.objects.exists():
        datas = StoreEntity.objects.values()
        print(type(datas))
        total = StoreEntity.objects.count()

        store__list = []
        for store in datas:
            store__list.append(store)

            # store_dict = {}
            # store_dict['id'] = store.id
            # store_dict['name'] = store.name
            # store_dict['city'] = store.city
            # store_dict['address'] = store.address
            result['data'] = store__list
    else:
        result['msg'] = '数据是空的'

    result['total'] = total
    return JsonResponse(result)

def count_fruit(request):
    #返回json数据，统计每种分类的水果数量，最高价格，和最低价格和总价格
    # result =FruitEntity.objects.aggregate(cnt=Count('name'),acg=Avg('price'),max=Max('price'),min=Min('price'),sum=Sum('price'))

    #中秋节： 全场水果打8.8折
    # FruitEntity.objects.update(price=F('price')*0.88)
    fruits = FruitEntity.objects.values()

    #查询价格低于50 或者 高于200的 或者 产地为西安 且名字中包含‘果’

    fruits2 =  FruitEntity.objects.filter(Q(price__lte=3) | Q(price__gte=10) | Q(Q(source='西安') & Q(name__contains='果'))).values()

    results = FruitEntity.objects.values('name','price','source','fruitimageentty__url').all()

    results1 = FruitEntity.objects.raw("select * from t_fruit_image")
    for i in results1:
        print(i.url,i.name)

    return JsonResponse({
        'count':[result for result in results],
        'fruits':[fruit for fruit in fruits],
        'multi_query':[fruit for fruit in fruits2],
        })



def login(request):
    result = FruitEntity.objects.values('name','price','source','fruitimageentty__url').all()
    if request.COOKIES.get('login_name'):
        return redirect('/user/find')
    return render(request,'fruit/index.html',locals())


def loginHandler(request):
    # price1 = request.GET.get('price1', 0)
    # price2 = request.GET.get('price2', 1000)
    # result = FruitEntity.objects.values('name', 'price', 'source', 'fruitimageentty__url').filter(price__gte=price1,
    #                                                                                               price__lte=price2).all()
    if request.method == 'POST':
        name = request.POST.get('name',None)
        phone = request.POST.get('phone',None)
        response = ''
        user_ = UserEntity.objects.filter(name=name).first()
        if user_:
            print(name, phone, user_.name)
            if user_.phone == phone:
                response = HttpResponse("ok")
                response = HttpResponseRedirect('find')
                response.set_cookie('login_name',user_.name)
                response.set_cookie('login_status',True)
                return response
            else:
                result = FruitEntity.objects.values('name', 'price', 'source', 'fruitimageentty__url').all()
                msg = '<script>alert("密码错误")</script>'
                return render(request,'fruit/index.html',locals())
        else:
            result = FruitEntity.objects.values('name', 'price', 'source', 'fruitimageentty__url').all()
            msg = '<script>alert("用户不存在")</script>'
            return render(request,'fruit/index.html',locals())





def find_nut(request,name):
    # name = request.GET.get('name')
    username = request.COOKIES.get('login_name')
    print(name)
    result = FruitEntity.objects.values('name', 'price', 'source', 'fruitimageentty__url').filter(category__name=name).all()
    print(result)
    return render(request, 'fruit/afterlog.html', locals())


def loginout(request):
    response = HttpResponse("ok")
    response = HttpResponseRedirect('/')
    response.delete_cookie('login_name')
    response.delete_cookie('is_login')
    key = request.COOKIES.get('login_name')
    print(key)
    return response


def FruitCart(request):
    username = request.COOKIES.get('login_name')
    fruit = UserEntity.objects.values('name','cart__fruitcartentity__fruit__name','cart__fruitcartentity__cnt','cart__fruitcartentity__fruit__price').filter(name=username)
    print(
        fruit
    )
    return render(request,'fruit/cart.html',locals())
