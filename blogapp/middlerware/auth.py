from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleWare(MiddlewareMixin):
    """登录授权中间件"""
    def process_request(self,request):
        """
        中间件请求，如果返回值为None，则继续走往下一个中间件或视图函数；
        如果返回值不是None,则往上一个步骤走，可以是HttpRespose,render,redirect
        :param request:
        :return:
        """
        if request.path_info in ['/login/','/image/code/']:
            return
        # 获取session
        auth_info = request.session.get("info")
        # print(auth_info)
        if auth_info:
            # 获取的session为空，则返回None,继续走
            return
        return redirect('/login/')