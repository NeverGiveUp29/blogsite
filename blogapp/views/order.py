from random import randint
from datetime import datetime
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from blogapp import models
from blogapp.utils.form import BootStrapModelForm
from blogapp.utils.pagination import Pagination

class OrderModerForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # 展示所有的字段
        # fields = '__all__'
        # 展示除了oid以外的所有字段，系统自动生成的id也不展示
        exclude = ['oid','admin']

def order_list(request):
    form = OrderModerForm
    query_set = models.Order.objects.all().order_by('-id')
    page_tool = Pagination(request,query_set=query_set,page_size=5)
    content_context = {
        "queryset": page_tool.page_queryset,
        "page_string": page_tool.html(),
        "form": form,
    }

    return render(request,'order_list.html',content_context)

@csrf_exempt
def order_add(request):
    """新增订单，用ajax实现"""
    form = OrderModerForm(data=request.POST)
    if form.is_valid():
        # 订单编号：额外新增一些不是用户输入的值
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S")+str(randint(1000,9999))
        # 管理员：从session中获取到admin_id，并赋值给表单
        form.instance.admin_id = request.session['info']['id']
        form.save()
        return JsonResponse({"status":True})
    return JsonResponse({"status":False,'error':form.errors})

def order_delete(request):
    """删除订单"""
    # 获取get请求传过来的uid
    uid = request.GET.get('uid')
    exist = models.Order.objects.filter(id=uid).exists()
    if not exist:
        return JsonResponse({"status":False,'error':'删除失败，数据不存在！'})
    # 查询的id存在，则删除。
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status":True})

def order_detail(request):
    """根据uid获取订单详细信息"""
    """    
    方式一：
    uid = request.GET.get('uid')
    # 根据id在数据库查询订单信息
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status":False,'error':'数据不存在！'})
    result = {
        "status": True,
        "data":{
            "title":row_object.title,
            "price":row_object.price,
            "order_status":row_object.order_status,
        }
    }
    return JsonResponse(result)
    """
    # 方式二：直接查询的数据库返回值为字典格式
    uid = request.GET.get('uid')
    # 根据id在数据库查询订单信息
    # row_object = models.Order.objects.filter(id=uid).first()
    # 取某个列的值：row_object.title

    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "order_status", ).first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': '编辑失败，数据不存在，请刷新重试！'})
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get('uid')
    row_data = models.Order.objects.filter(id=uid).first()
    if not row_data:
        return JsonResponse({"status": False, 'tips': '数据不存在！'})
    form = OrderModerForm(data=request.POST,instance=row_data)
    if form.is_valid():
        form.save()
        return JsonResponse({"status":True})
    return JsonResponse({"status":False,'error':form.errors})