from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from django import forms

from blogapp import models
from blogapp.utils.pagination import Pagination
from blogapp.utils.form import PrettyModelForm,PrettyEditModelForm
from blogapp.utils.bootstrap import BootStrapModelForm


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {"detail": forms.TextInput()}

def task_list(request):
    """任务管理"""


    form = TaskModelForm()

    context = {
        "form":form
    }
    return render(request,'task_list.html',context)

@csrf_exempt
def task_ajax(request):
    """ajax练习"""
    print(request.GET)
    print(request.POST)
    data_dict = {
        "status":True,
        "data":[11,22,33,44]
    }
    return HttpResponse(json.dumps(data_dict))
    # ajax返回的数据一般是json，不是页面，所以需要转为json格式。也可以直接用django提供给JsonResponse()方法
    # return JsonResponse(data_dict)

@csrf_exempt
def task_add(request):
    """新增任务"""
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {
            "status": True,
        }
        return HttpResponse(json.dumps(data_dict))
    data_dict = {
        "status":False,
        "error": form.errors
    }
    return HttpResponse(json.dumps(data_dict,ensure_ascii=False))
