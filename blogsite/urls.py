"""blogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings

from blogapp.views import home,pretty,depart,user,admin,account,task,order,chart,upload,city
urlpatterns = [
    # path('admin/', admin.site.urls),'
    # 配置media目录存放用户上传的数据
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT},name='media'),

    path('index/', home.index),
    path('depart/list/',depart.depart_list),
    path('depart/list_local/',depart.depart_list_other),
    path('depart/add/',depart.depart_add),
    path('depart/delete/',depart.depart_delete),
    # http://127.0.0.1:8000/depart/{nid}/edit/  # <int:nid>说明nid只能是int类型
    path('depart/<int:nid>/edit/',depart.depart_edit),
    path('depart/upload/',depart.depart_upload),

    path('user/list/',user.user_list),
    path('user/add/',user.user_add),
    path('user/model/form/add/',user.user_model_form_add),
    path('user/<int:nid>/edit/',user.user_edit),
    path('user/delete/',user.user_delete),

    path('pretty/list/',pretty.pretty_list),
    path('pretty/add/',pretty.pretty_add),
    path('pretty/<int:nid>/edit/',pretty.pretty_edit),
    path('pretty/<int:nid>/delete/',pretty.pretty_delete),

    # 管理员
    path('admin/list/',admin.admin_list),
    path('admin/add/',admin.admin_add),
    path('admin/<int:nid>/edit/',admin.admin_edit),
    path('admin/<int:nid>/delete/',admin.admin_delete),
    path('admin/<int:nid>/reset/',admin.admin_reset),

    # 登录
    path('login/',account.login),
    path('logout/',account.logout),
    path('image/code/',account.image_code),

    # 任务管理
    path('task/list/',task.task_list),
    path('task/ajax/',task.task_ajax),
    path('task/add/',task.task_add),

    # 订单管理
    path('order/list/',order.order_list),
    path('order/add/',order.order_add),
    path('order/delete/',order.order_delete),
    path('order/detail/',order.order_detail),
    path('order/edit/',order.order_edit),

    # 数据统计
    path('chart/list/',chart.chart_list),
    # 柱状图
    path('chart/bar/',chart.chart_bar),
    # 饼状图
    path('chart/pie/',chart.chart_pie),
    # 折线图
    path('chart/line/',chart.chart_line),

    # 文件上传
    path('upload/list/',upload.upload_list),
    # form表单进行文件上传
    path('upload/form/',upload.upload_form),
    # modelform表单上传文件
    path('upload/model/form/',upload.upload_model_form),

    # 城市列表
    path('city/list/',city.city_list),
    path('city/add/',city.city_add),
]
