from django.db import models

# Create your models here.
from django.db.models import Q

from mainapp.models import FruitEntity, UserEntity


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        abstract = True  # 抽象的表类


class OrderManager(models.Manager):
    # 获取查询结果集独享Query_set
    def get_queryset(self):
        return super().get_queryset().filter(~Q(pay_status=5))



class OrderAddress(models.Model):
    receiver = models.CharField(max_length=20, null=True, verbose_name="收货人")
    receiver_phone = models.CharField(max_length=11, null=True, verbose_name="收货人电话")
    receiver_address = models.TextField(verbose_name="收货地址")
    user_id = models.ForeignKey(UserEntity, verbose_name="用户名称", on_delete=models.CASCADE)

    def __str__(self):
        return self.receiver_address

    class Meta:
        db_table = 't_address'
        verbose_name = verbose_name_plural = '用户地址表'



class OrderModel(models.Model):
    num = models.CharField(max_length=20, primary_key=True, verbose_name='订单号')
    user_id = models.ForeignKey(UserEntity, verbose_name="用户名称", on_delete=models.CASCADE)
    address_id = models.ForeignKey(OrderAddress,on_delete=models.CASCADE,verbose_name='收货地址')
    title = models.CharField(max_length=100, verbose_name="订单名称")


    def __str__(self):
        return self.title

    class Meta:
        db_table = 't_order'
        verbose_name = verbose_name_plural = '订单表'


class OrderDetail(BaseModel):
    num = models.ForeignKey(OrderModel, verbose_name='订单名称', on_delete=models.CASCADE)
    goods_id = models.ForeignKey(FruitEntity, verbose_name="水果", on_delete=models.CASCADE)
    cnt = models.IntegerField(verbose_name="数量", default=0)
    pay_type = models.IntegerField(choices=((0, "余额"),
                                            (1, "银行卡"),
                                            (2, "微信支付"),
                                            (3, "支付宝")),
                                   verbose_name="支付方式", default=0)
    pay_status = models.IntegerField(choices=((0, "待支付"),
                                              (1, "已支付"),
                                              (2, "待收货"),
                                              (3, "已收货"),
                                              (4, "完成"),
                                              (5, "取消")),
                                     verbose_name="订单状态", default=0)
    objects = OrderManager()

    def __str__(self):
        return self.num.title
    class Meta:
        db_table = 't_detail'
        verbose_name = verbose_name_plural = '订单详情表'

    @property
    def price(self):
        return round(self.cnt*self.goods_id.price)


    @property
    def price1(self):
        return self.goods_id.price


    # @property
    # def image(self):
    #     images = self.goods_id.fruitimageentty_set.values('url')
    #     for i in images:
    #         print(i)
    #
    #     return i['url']

