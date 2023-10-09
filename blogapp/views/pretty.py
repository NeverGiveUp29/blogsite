############## 靓号 ############
from django.shortcuts import render,redirect
from blogapp import models
from blogapp.utils.pagination import Pagination
from blogapp.utils.form import PrettyModelForm,PrettyEditModelForm
def pretty_list(request):
    # 靓号列表
    # select from blogapp_prettynum disorder by level # 根据等级逆序排序
    # query_set = models.PrettyNum.objects.all().order_by("-level",'mobile')
    # 优化，增加手机号查询功能，先获取查出输入框的值,然后根据模糊查询返回查询结果
    data_dict = {}
    search_data = request.GET.get('q','')
    # 去除输入框的空格、换行
    search_data = search_data.strip().replace(' ', '').replace('\n', '').replace('\r', '')
    if search_data:
        data_dict["mobile__contains"]=search_data
    query_set = models.PrettyNum.objects.filter(**data_dict).order_by("-level",'id')

    page_tool = Pagination(request,query_set=query_set)
    page_string =page_tool.html()
    # #当前页的数据：page_tool.page_queryset
    request_context = {
        "query_set": page_tool.page_queryset,
        "search_data": search_data,
        "page_string": page_string
    }
    return render(request,"pretty_list.html",request_context)

def pretty_add(request):
    """添加靓号"""
    if request.method=="GET":
        form = PrettyModelForm()
        return render(request,'pretty_add.html',{"form":form})
    # 非GET请求时，获取页面提交的数据
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request,'pretty_add.html',{"form":form})

def pretty_edit(request,nid):
    # 编辑、新增可以公用一个ModelForm的原属数据，也可以给编辑重新定义一个新的ModelForm。
    row_data = models.PrettyNum.objects.filter(id=nid).first()
    if request.method=="GET":
        form = PrettyEditModelForm(instance=row_data)
        return render(request,'pretty_edit.html',{"form":form})
    form = PrettyEditModelForm(data=request.POST,instance=row_data)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {"form": form})

def pretty_delete(request,nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')