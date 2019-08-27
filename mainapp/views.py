from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from mainapp.models import UserEntity, FruitEntity, FruitImageEntty, StoreEntity
from django.db.models import Count,Sum,Min,Avg,Max


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
    #从查询参数中获取价格区间price1，price2
    result = FruitEntity.objects.filter(price__gte=price1,price__lte=price2).\
                                                exclude(price=250).all()
                                                 # .filter(name__contains='果')

    #根据我们价格区间来查找满足条件的所有水果信息
    #将查询到的数据渲染到模板上
    return render(request,'fruit/index.html',locals())


def find_store(request):
    queryset = StoreEntity.objects.filter(create_time__month="08",create_time__year=2019)

    stores = queryset.all()
    return render(request,'store/list.html',locals())



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
    result =FruitEntity.objects.aggregate(cnt=Count('name'),acg=Avg('price'),max=Max('price'),min=Min('price'),sum=Sum('price'))
    return JsonResponse(result)
