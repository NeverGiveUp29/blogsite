from blogapp import models
from django import forms
from  django.core.validators import RegexValidator # 导入正则校验模块
from django.core.exceptions import ValidationError # 导入异常模块，方便抛出异常
from blogapp.utils.bootstrap import BootStrapModelForm

class UserModelForm(BootStrapModelForm):
    # 定义meta类，并实例化UserInfo类，同时定义一个列表存放数据表字段
    class Meta:
        # 如果想给字段添加更多的校验，比如字数限制，密码格式校验，可在这定义变量进行重写
        # name = forms.CharField(min_length=3,label="用户名")# 用户名至少三位
        # password =forms.CharField(label="密码",validators="re")# re是填正则表达式

        model = models.UserInfo
        fields = ["name","password","age","account","create_time","depart","gender"]

# 定义靓号的ModelForm类，定义元数据类和样式
class PrettyModelForm(BootStrapModelForm):
    # 字段格式校验方法一：给手机号字段添加校验规则
    mobile = forms.CharField(
        label="手机号",
        # validators是一个可迭代对象（列表），可填写多个校验参数
        validators=[RegexValidator(r'1[3-9]\d{9}$', '手机号格式错误')]
    )
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]

    # 字段格式校验方法二：钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exits = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exits:
            raise ValidationError("手机号已存在！")
        if len(txt_mobile) != 11:
            # 长度不是11，验证不通过，
            raise ValidationError("格式错误,手机号必须是11位数！")
        # 验证通过，返回用户输入的值
        return txt_mobile

class PrettyEditModelForm(BootStrapModelForm):
    # 字段格式校验方法一：给手机号字段添加校验规则
    mobile = forms.CharField(
        label="手机号",
        # validators是一个可迭代对象（列表），可填写多个校验参数
        validators=[RegexValidator(r'1[3-9]\d{9}$', '手机号格式错误')]
    )
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
    # 将form.ModelForm改为继承BootStrapModelForm后，就不用再定义 __init__了
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     for name,field in self.fields.items():
    #         field.widget.attrs = {"class":"form-control","placeholder":field.label}

    def clean_mobile(self):
        # 打印当前编辑的那一行的ID,用pk,即primary key，model(表)的主键
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        # 编辑，校验除了当前编辑靓号以外，录入的手机号已存在数据库中。exclude()排除满足条件的数据，返回一个新的 QuerySet
        exits = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exits:
            raise ValidationError("手机号已存在！")
        if len(txt_mobile) != 11:
            # 长度不是11，验证不通过，
            raise ValidationError("格式错误,手机号必须是11位数！")
        # 验证通过，返回用户输入的值
        return txt_mobile