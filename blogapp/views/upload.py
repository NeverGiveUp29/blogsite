import os

from django.shortcuts import render,HttpResponse
from django import forms
from django.conf import settings

from blogapp.utils.bootstrap import BootStrapForm,BootStrapModelForm
from blogapp import models

def upload_list(request):
    """文件上传"""
    if request.method=='get':
        return render(request, 'upload_list.html')

    # print(request.POST)
    # --><QueryDict: {'csrfmiddlewaretoken': ['Rui2dYtVl8FlaUiASKePOuWNddzpYJle9iLYQoIgUhGt1Q1ZeDbOJGYOC4FJKOZa'], 'username': ['fff2']}>
    # print(request.FILES)
    # --><MultiValueDict: {'uploadFile': [<InMemoryUploadedFile: 电子发票6.65 (2).pdf (application/pdf)>]}>
    file_object = request.FILES.get('uploadFile')
    # -->电子发票1.9.pdf
    if file_object:
        # print(file_object.name)
        # 把上传文件保存到项目根目录，并命名为上传文档的名称
        f = open(file_object.name,mode='wb')
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse('上传成功！')
    return render(request, 'upload_list.html')

class UploadForm(BootStrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label="姓名",max_length=32)
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像',max_length=128)

def upload_form(request):
    """form表单进行文件上传"""
    title = "头像上传"
    if request.method=='GET':
        form = UploadForm()
        return render(request, 'form_upload.html', {'form': form, 'title': title})
    form = UploadForm(data=request.POST,files=request.FILES)
    if form.is_valid():
        # 1.读取图片内容，写入到文件夹并获取文件路径
        img_object = form.cleaned_data.get('img')
        # print(img_object)# # QQ图片20230322074417.png

        # 文件改为存放到media目录下，settings.MEDIA_ROOT保存在数据库是绝对路径
        # media_path = os.path.join(settings.MEDIA_ROOT,img_object.name)

        # 文件改为存放到media目录下，'media'保存在数据库是相对路径
        media_path = os.path.join('media',img_object.name)
        f = open(media_path,mode='wb')
        for chunk in img_object.chunks():
            f.write(chunk)
        f.close()
        # 2.将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data.get('name'),
            age=form.cleaned_data.get('age'),
            img=media_path,
        )
        return HttpResponse('...')
    return render(request, 'form_upload.html',{'form':form,'title':title})

class UploadModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = '__all__'

def upload_model_form(request):
    """"modelform上传文件"""
    title = "modelform上传文件"
    if request.method == 'GET':
        form = UploadModelForm()
        return render(request, 'form_upload.html', {'form': form, 'title': title})
    form = UploadModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("上传成功")
    return render(request, 'form_upload.html', {'form': form, 'title': title})