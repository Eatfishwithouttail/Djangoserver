import uuid

from django.db import models


# Create your models here.
class UserEntity(models.Model):
    name = models.CharField(max_length=20, verbose_name='账号')
    age = models.IntegerField(default=0, verbose_name='年龄')
    phone = models.CharField(max_length=11, verbose_name='手机号', blank=True, null=True)

    class Meta:
        # 设置表名
        db_table = 't_user'
        verbose_name = '客户管理'
        # 设置复数表示方式
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 水果分类
class CateTypeEntity(models.Model):
    name = models.CharField(max_length=20, verbose_name='分类名')
    order_num = models.IntegerField(verbose_name='排序')

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'mainapp'    #指定应用名称
        db_table = 't_category'
        ordering = ['-order_num']  # 指定排序字段 - 表示降序  默认升序
        verbose_name = '水果分类表'
        verbose_name_plural = verbose_name


#水果类
class FruitEntity(models.Model):
    name = models.CharField(max_length=20, verbose_name='水果名')
    price = models.FloatField(verbose_name='价格')
    source = models.CharField(max_length=30, verbose_name='原产地')
    category = models.ForeignKey(CateTypeEntity, on_delete=models.CASCADE)

    class Meta:
        db_table = 't_fruit'
        verbose_name = '水果表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#水果图片
class FruitImageEntty(models.Model):
    fruit_id = models.ForeignKey(FruitEntity, on_delete=models.CASCADE)
    url = models.ImageField(max_length=50, verbose_name='地址')
    name = models.CharField(max_length=100, verbose_name='名称')

    class Meta:
        db_table = 't_fruit_image'
        verbose_name = '水果图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#水果商店类
class StoreEntity(models.Model):
    # 默认情况下，模型自创建主键id字段--隐式
    # 但是也可以显式的方式声明主键（primary_key）
    id = models.UUIDField(primary_key=True, verbose_name='店号')
    name = models.CharField(max_length=30, verbose_name='店名称')
    store_type = models.IntegerField(choices=((0, '自营'), (1, '第三方')), db_column='type_', verbose_name='店类型')

    boss_name = models.CharField(max_length=10, verbose_name='老板名称')
    phone = models.CharField(max_length=10, verbose_name='电话')
    address = models.CharField(max_length=50, verbose_name='具体地址')
    # 支持城市搜索, 所以创建索引
    city = models.CharField(max_length=20, db_index=True, verbose_name='城市')

    logo = models.ImageField(verbose_name='logo', upload_to='store', width_field='logo_width',
                             height_field='logo_height', null=True, blank=True)
    logo_width = models.IntegerField(verbose_name='logo宽', null=True)
    logo_height = models.IntegerField(verbose_name='logo高', null=True)

    summary = models.TextField(verbose_name='介绍', blank=True, null=True)

    opened = models.BooleanField(verbose_name='是否开业', default=False)

    create_time = models.DateField(verbose_name='成立时间', auto_now_add=True, null=True)
    last_time = models.DateField(verbose_name='最后变更时间', auto_now=True, null=True)

    # lat = models.FloatField(verbose_name='纬度')
    # lon = models.FloatField(verbose_name='经度')

    class Meta:
        db_table = 't_store'
        verbose_name = '商店表'
        verbose_name_plural = verbose_name
        unique_together = (('name', 'city'),)

    def __str__(self):
        return self.name

    # 调用模型保存方法时调用
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.id = uuid.uuid4().hex
        super().save()

    @property
    def id_(self):
        return self.id.hex
