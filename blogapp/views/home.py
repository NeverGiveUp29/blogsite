from django.shortcuts import render

def index(request):
    # return HttpResponse("欢迎来到首页！")
    return  render(request,'index.html')