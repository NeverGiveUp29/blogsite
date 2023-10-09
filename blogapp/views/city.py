from django.shortcuts import render,redirect

from blogapp import models
# 直接用已有的上传modelform
from blogapp.views.upload import UploadModelForm


def city_list(request):
    """城市列表"""
    query_set = models.City.objects.all()
    return render(request,'city_list.html',{'queryset':query_set})

def city_add(request):
    """"新建城市"""
    title = "新建城市"
    if request.method == 'GET':
        form = UploadModelForm()
        return render(request, 'form_upload.html', {'form': form, 'title': title})
    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')
    return render(request, 'form_upload.html', {'form': form, 'title': title})