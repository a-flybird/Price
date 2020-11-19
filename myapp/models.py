from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token
from simple_history import register
from simple_history.models import HistoricalRecords
class basedata(models.Model):
    id = models.AutoField(primary_key=True)
    productcode = models.CharField(max_length=32, blank=True, null=True, verbose_name='编码')
    name = models.CharField(max_length=512, blank=True, null=True, verbose_name='名称')
    model = models.CharField(max_length=512, null=True, blank=True, verbose_name='型号/类号')
    description = models.CharField(max_length=512, verbose_name='描述')
    Price_Source = (
        ('Pricing', '定价'),
        ('Quotation', '报价'),
    )
    product_type = models.CharField(max_length=32, verbose_name='物料类型')
    price_source = models.CharField(max_length=32, choices=Price_Source, verbose_name='价格来源')
    RRP_USD = models.CharField(max_length=32, blank=True, null=True)
    RRP_EUR = models.CharField(max_length=32, blank=True, null=True)
    RRP_GBP = models.CharField(max_length=32, blank=True, null=True)
    RRP_RMB = models.CharField(max_length=32, blank=True, null=True)
    remark = models.CharField(max_length=1024, blank=True, null=True, verbose_name='备注信息')
    createddate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lastmodifieddate = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        print('aaaaaaaaaa', self.changed_by)
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = '基础数据'
        verbose_name_plural = '基础数据'
#
# def get_poll_user(instance, **kwargs):
#     print(instance.changed_by)
#     return instance.changed_by
#
# register(basedata, get_user=get_poll_user)


class importfile(models.Model):
    file=models.FileField(upload_to='file')
    createddate = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '导入数据'
        verbose_name_plural = '导入数据'

class downloadfile(models.Model):
    createddate = models.DateTimeField(auto_now_add=True)
    down_file=models.CharField(max_length=50,default=createddate)
    class Meta:
        verbose_name = '导出数据'
        verbose_name_plural = '导出数据'

class updatefile(models.Model):
    update_file=models.FileField(upload_to='update_file')
    lastmodifieddate = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '更新数据'
        verbose_name_plural = '更新数据'

class upsertfile(models.Model):
    filename=models.FileField(upload_to='filename')
    upsertdate=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '导入/更新数据'
        verbose_name_plural = '导入/更新数据'

class CaseFile(models.Model):
    file_name=models.FileField(upload_to='case/%Y/%m/%d',verbose_name=u"文件名称")

class UserToken(models.Model):
    token = models.CharField(max_length=100, unique=True, null=False, verbose_name='用户令牌/用户的唯一标识')
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='关联的用户')
    out_time = models.DateTimeField(null=False, verbose_name='过期时间')

class Role(models.Model):
    role_code = models.CharField(max_length=64, unique=True, null=False, verbose_name='角色编码')
    role_name = models.CharField(max_length=64, unique=True, null=False, verbose_name='角色名称')
    description = models.CharField(max_length=200, null=False, verbose_name='角色描述')
    create_time = models.DateTimeField(auto_now_add=True,null=False, verbose_name='创建时间')

class Menu(models.Model):
    menu_code = models.CharField(max_length=64, unique=True, null=False, verbose_name='菜单编码')
    menu_name = models.CharField(max_length=64, unique=True, null=False, verbose_name='菜单名称')
    description = models.CharField(max_length=200, null=False, verbose_name='菜单描述')
    icon = models.CharField(max_length=32,null=False, verbose_name='icon')
    roles = models.ManyToManyField(Role,through='RoleMenu')

class RoleMenu(models.Model):
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True,)
    class Meta:
        db_table = 'Role_Menu'

class UserRole(models.Model):
    role_id = models.ForeignKey(Role,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'UserRole'

class BJ_basedata(models.Model):
    id = models.AutoField(primary_key=True)
    productcode = models.CharField(max_length=32, blank=True, null=True, verbose_name='编码')
    description = models.CharField(max_length=512, verbose_name='描述(中文)')
    description_en = models.CharField(max_length=512, verbose_name='描述(英文)')
    unit = models.CharField(max_length=512, verbose_name='单位')
    USD = models.CharField(max_length=32, blank=True, null=True)
    EUR = models.CharField(max_length=32, blank=True, null=True)
    GBP = models.CharField(max_length=32, blank=True, null=True)
    CNY = models.CharField(max_length=32, blank=True, null=True)
    CAD = models.CharField(max_length=32, blank=True, null=True)
    AUD = models.CharField(max_length=32, blank=True, null=True)
    createddate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lastmodifieddate = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    class Meta:
        verbose_name = '备件数据'
        verbose_name_plural = '备件数据'

class FW_basedata(models.Model):
    id = models.AutoField(primary_key=True)
    productcode = models.CharField(max_length=32, blank=True, null=True, verbose_name='编码')
    description = models.CharField(max_length=512, verbose_name='描述(中文)')
    description_en = models.CharField(max_length=512, verbose_name='描述(英文)')
    unit = models.CharField(max_length=512, verbose_name='单位')
    USD = models.CharField(max_length=32, blank=True, null=True)
    EUR = models.CharField(max_length=32, blank=True, null=True)
    GBP = models.CharField(max_length=32, blank=True, null=True)
    CNY = models.CharField(max_length=32, blank=True, null=True)
    CAD = models.CharField(max_length=32, blank=True, null=True)
    AUD = models.CharField(max_length=32, blank=True, null=True)
    createddate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lastmodifieddate = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '服务数据'
        verbose_name_plural = '服务数据'