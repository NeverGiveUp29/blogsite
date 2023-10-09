from django.shortcuts import render,redirect
from blogapp import models
from django import forms
from django.core.exceptions import ValidationError

from blogapp.utils.bootstrap import BootStrapModelForm
from blogapp.utils.encrypt import md5 # md5加密
from blogapp.utils.pagination import Pagination

def admin_list(request):
    """管理员账户列表"""
    # 搜索
    data_dict = {}
    search_data = request.GET.get('q', '')
    # 去除输入框的空格、换行
    search_data = search_data.strip().replace(' ', '').replace('\n', '').replace('\r', '')
    if search_data:
        data_dict["username__contains"] = search_data
    query_set = models.Admin.objects.filter(**data_dict).order_by('id')

    # 分页
    page_tool = Pagination(request,query_set=query_set,page_size=3,plus=2)
    content_text = {
        "queryset": page_tool.page_queryset,
        "page_string": page_tool.html(),
        "search_data": search_data
    }
    return render(request,'admin_list.html',content_text)


class AdminForm(BootStrapModelForm):
    # 1.1新增一个字段：确认密码
    confirm_password = forms.CharField(
        label="确认密码",
        max_length=64,
        # 定义为密码输入表单，render_value=True为校验不通过时保留输入内容。
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username","password","confirm_password"]
        # 1.2给已有字段password添加样式为密码输入框
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        """ 返回表单提交的加密后的密码"""
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        """如果原密码和确认密码一致，返回加密后的确认密码"""
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd!=confirm:
            raise ValidationError("确认密码和原密码不一致")
        return confirm

def admin_add(request):
    """新建管理员账户"""
    if request.method=='GET':
        form = AdminForm()
        return render(request,'change.html',{"title":"新增管理员","form":form})

    # 如果是post请求，则校验表单数据。数据正确，则提交保存到数据库，并返回到列表页面。
    form = AdminForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"title": "新增管理员", "form": form})

class AdminEditForm(BootStrapModelForm):
    """"编辑管理员ModelForm"""
    # confirm_password = forms.CharField(
    #     label="确认密码",
    #     max_length=64,
    #     widget=forms.PasswordInput(render_value=True)
    # )

    class Meta:
        model = models.Admin
        # fields = ["username","password","confirm_password"]
        fields = ["username","password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        """ 返回表单提交的加密后的密码"""
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # def clean_confirm_password(self):
    #     """如果原密码和确认密码一致，返回加密后的确认密码"""
    #     pwd = self.cleaned_data.get("password")
    #     confirm = md5(self.cleaned_data.get("confirm_password"))
    #     if pwd!=confirm:
    #         raise ValidationError("确认密码和原密码不一致")
    #     return confirm

class AdminResetForm(BootStrapModelForm):
    """重置密码ModelForm,用户名字段不需要显示"""
    confirm_password = forms.CharField(
        label="确认密码",
        max_length=64,
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password","confirm_password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        """ 新增逻辑,密码和原密码相同时,则不允许重置"""
        pwd = md5(self.cleaned_data.get("password"))
        exits = models.Admin.objects.filter(id=self.instance.pk,password=pwd).exists()
        if exits:
            raise ValidationError("新密码不能和旧密码相同!")
        return pwd

    def clean_confirm_password(self):
        """如果原密码和确认密码一致，返回加密后的确认密码."""
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd!=confirm:
            raise ValidationError("确认密码和原密码不一致")
        return confirm

def admin_edit(request,nid):
    """编辑管理员账户"""
    row_data = models.Admin.objects.filter(id=nid).first()
    # 1.管理员账户不存在时，跳转到错误提示页面
    if not row_data:
        return render(request, 'error.html', {"error_msg": "该管理账户不存在！"})
    # 2.get请求时（进入编辑页面），回填字段信息。
    if request.method == "GET":
        form = AdminEditForm(instance=row_data)
        return render(request, 'change.html', {"title": "编辑管理员", "form": form})
    # 3.提交编辑好的信息后，跳转到列表页面。如果表单输入数据不合法，则还是停留在编辑页面。
    form = AdminEditForm(data=request.POST,instance=row_data)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request,'change.html',{"title":"编辑管理员","form":form})

def admin_delete(request,nid):
    """删除管理员账户"""
    row_data = models.Admin.objects.filter(id=nid).first()
    # 1.管理员账户不存在时，跳转到错误提示页面
    if not row_data:
        return render(request, 'error.html', {"error_msg": "该管理员账户不存在！"})
    # 2.get请求时（进入编辑页面），回填字段信息。
    row_data.delete()
    return redirect('/admin/list/')

def admin_reset(request,nid):
    row_data = models.Admin.objects.filter(id=nid).first()
    if not row_data:
        return render(request, 'error.html', {"error_msg": "该管理账户不存在！"})
    title = f"重置密码-{row_data.username}"
    if request.method == "GET":
        form = AdminResetForm()
        return render(request, 'change.html', {"title": title, "form": form})
    form = AdminResetForm(data=request.POST, instance=row_data)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {"title": title, "form": form})