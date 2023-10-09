from django.shortcuts import render,redirect,HttpResponse
from django import forms
from io import BytesIO

from blogapp import models
from blogapp.utils.bootstrap import BootStrapForm
from blogapp.utils.encrypt import md5
from blogapp.utils.code import check_code


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(),
        required=True
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)

def login(request):
    """登录"""
    if request.method=="GET":
        form = LoginForm()
        return render(request,'login.html',{"form":form})
    form = LoginForm(data=request.POST)
    if form.is_valid():

        # code1.1:验证码校验：获取cleaned_data的验证码，由于后面用到cleaned_data数据库查询，所以通过pop()方法截取验证码.
        user_input_code = form.cleaned_data.pop('code')
        # code1.2:获取session中存储的验证码，如果没有，则赋值为空字符串，因为后台设置了60秒超时，超时后就获取不到了。
        code = request.session.get('iamge_code','')
        # code1.3:用户输入验证码不对，返回验证码错误
        if code.upper()!=user_input_code.upper():
            form.add_error("code", "验证码输入错误！")
            return render(request, 'login.html', {"form": form})
        # 数据库查询用户输入的密码和用户名是否存在
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # 密码错误提示，显示在密码输入框下面
            form.add_error("password","用户名或密码错误！")
            # print(form.errors)
            return render(request, 'login.html', {"form": form})
        # 用户名和密码正确，则网站生成随机字符串；写到用户浏览器的cookie中，再写入到session中
        request.session["info"] = {"id":admin_object.id,"name":admin_object.username}
        # code1.4:验证通过，重新设置session的有效期为7天
        request.session.set_expiry(60*60*24*7)
        return redirect('/admin/list/')
    return render(request,'login.html',{"form":form})

def image_code(request):
    """生成验证码，需要在中间件里加上不需要登录验证，if request.path_info in ['/login/','/image/code/']
    """
    # 调用pillow方法生成验证码方法，生成图片
    img,code_string = check_code()
    # 把验证码写入到自己的session中，方便后续获取验证码再进行校验
    request.session['iamge_code'] = code_string
    # 设置超时时间为60秒
    request.session.set_expiry(60)

    # 把图片img写入内存文件，方便使用而不是多次读取文件
    stream = BytesIO()
    img.save(stream,'png')

    return HttpResponse(stream.getvalue())

def logout(request):
    """退出登录"""
    # 清除session中的登录信息即可，该信息在登录接口里有，存的键值对：{"id":admin_object.id,"name":admin_object.username}
    request.session.clear()
    return redirect('/login')