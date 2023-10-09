from django.shortcuts import render,redirect
from blogapp import models
from blogapp.utils.pagination import Pagination
from blogapp.utils.form import UserModelForm

def user_list(request):
    """用户列表，获取数据库的数据"""
    user_info_set = models.UserInfo.objects.all()
    page_tool = Pagination(request,query_set=user_info_set,page_size=2,plus=3)
    context = {
        "user_info_set": page_tool.page_queryset,
        "page_string": page_tool.html()
    }

    return render(request,'user_list.html',context)
def user_add(request):
    """添加用户"""
    if request.method=="GET":
        # 获取性别的元组值、部门值，部门是直接从数据库中获取，然后返回给前端页面
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request,'user_add.html',context)

    # 获取用户提交的数据，根据name属性的值作为变量进行获取
    username = request.POST.get('name')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    depart = request.POST.get('depart')
    gender = request.POST.get('gender')

    # 添加到数据库中
    models.UserInfo.objects.create(name=username,password=password,age=age,
                                   account=account,create_time=create_time,
                                   depart_id=depart,gender=gender)
    # 添加成功后返回到用户列表
    return redirect("/user/list/")

def user_model_form_add(request):
    """添加用户（ModelForm版本）"""
    if request.method=='GET':
        form = UserModelForm()
        return render(request,'user_model_form_add.html',{"form":form})
    # post请求，获取post提交的数据
    form = UserModelForm(data=request.POST)
    # 如果提交数据合法，就保存数据，并会新增到数据库
    if form.is_valid():
        # print(form.cleaned_data)# 打印提交的表单数据
        # save()也执行了sql的保存操作，等于UserInfo.objects.create(...)
        form.save()
        return redirect('/user/list/')
    # 校验失败，，停留在提交页面，并返回错误信息。也需要在html里回显错误信息
    return render(request,'user_model_form_add.html',{"form":form})

def user_edit(request,nid):
    """编辑用户"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method=="GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{"form":form})
    # post数据处理,instance是获取当前表单的数据参数
    form  = UserModelForm(data=request.POST,instance=row_object)
    # 数据格式校验
    if form.is_valid():
        # 默认保存的是用户数亿人的所有数据，如果想要在用户输入意外增加一点值，比如新增一个用户特权字段
        # form.instance.priviege = "VIP"
        #格式： form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request,'user_edit.html',{'form':form})

def user_delete(request):
    """删除用户"""
    nid = request.GET.get("nid")
    # 数据库删除该用户
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')