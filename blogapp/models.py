from django.db import models

# Create your models here.
class Department(models.Model):
    """部门表"""
    # id = models.BigAutoField()
    title = models.CharField(verbose_name='标题',max_length=32)
    def __str__(self):
        # 实例化这个类后可返回部门名称
        return self.title

class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    def __str__(self):
        return self.username

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    # ,max_digits是长度，decimal_place是小数点2位
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2,default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")# Y-m-d H:M:S
    create_time = models.DateField(verbose_name="入职时间") # 没有时分秒，Y-m-d
    # depart_id = models.BigIntegerField(verbose_name="部门ID") # 这样写，部门id没约束，可随便新增

    # 级联删除，关联。避免写入部门表不存在的部门id.
    # 用户表存ID还是存部门名称？1.按数据库范式存id,可节省存储开销。
    # 存名称，是大公司常用的，因为查名称次数较多，连表耗时。为了加速查找，允许数据冗余。
    # to:与那张表关联
    # to_field:与表中的那一列关联，比如与id列关联
    # 1.on_delete,级联删除，如果部门表的某一部门被删除了，也把用户表的这个部门id删掉
    depart = models.ForeignKey(verbose_name="部门",to="Department",to_field="id",on_delete=models.CASCADE)
    #2.如果不想被级联删除，可以 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True,blank=True,on_delete=models.SET_NULL)
    # 存在性别，为了节省开支，存数字。在django中约束gengder的值，如用元组预先存储值，写入数据库时只能存1或2.
    gender_choices =(
        (1,"男"),
        (2,"女")
    )
    # choice参数，即值只能从传入choice的列表或元组或字典里取值
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)

class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号",max_length=11)
    # 想要允许未空，null=True,blank=True
    price = models.IntegerField(verbose_name="价格",default=0)
    # 靓号等级
    level_choice = (
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级")
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choice,default=1)
    # 状态,默认是未占用
    status_choice = (
        (1,"已占用"),
        (2,"未占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choice,default=2)

class Task(models.Model):
    title = models.CharField(verbose_name="标题",max_length=64)
    detail = models.TextField(verbose_name="详细信息",max_length=512)
    level_choice = (
        (1,"紧急"),
        (2,"重要"),
        (3,"临时"),
        (4, "正常"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choice, default=1)
    user = models.ForeignKey(verbose_name="负责人", to=Admin, on_delete=models.CASCADE)


class Order(models.Model):
    """订单管理"""
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="商品名称", max_length=32)
    price = models.CharField(verbose_name="价格", max_length=32)
    status_choice = (
        (1,"待支付"),
        (2,"已支付"),
    )
    order_status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to=Admin, on_delete=models.CASCADE)

class Boss(models.Model):
    """老板列表，用于Form上传头像"""
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    img = models.CharField(verbose_name='头像', max_length=128)


class City(models.Model):
    """城市列表，用于ModelForm上传文件，结合media文件"""
    name = models.CharField(verbose_name="城市", max_length=32)
    count = models.IntegerField(verbose_name='人口')
    # FileField()本质上数据库也是CharField，自动保存数据.upload_to:/media/city/
    img = models.FileField(verbose_name='Logo', max_length=128,upload_to='city/')