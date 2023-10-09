"""
自定义的分页组件,使用该组件需要做到以下几件事情。
一、在视图函数中：
    def pretty_list(request):
    data_dict = {}
    # 1.根据自己的情况去筛选自己的数据，queryset
    query_set = models.PrettyNum.objects.filter(**data_dict).order_by("-level",'id')

    # 2. 实例化分页对象
    from blogapp.utils.pagination import Pagination
    page_tool = Pagination(request,query_set=query_set)
    page_string =page_tool.html()
    # #当前页的数据：page_tool.page_queryset
    request_context = {
        "query_set": page_tool.page_queryset, #分页当前页数据
        "search_data": search_data, # 获取的查询页码
        "page_string": page_string
    }
    return render(request,"pretty_list.html",request_context)
二、在HTML页面中：
     2.1循环展示列表字段
        {% for obj in query_set %}
          {{obj.xx}}
        {% endfor %}

     2.2 添加页码模块
    <!--分页区域-->
    <div class="clearfix">
        <ul class="pagination" style="float: left">
            <!--页码部分-->
            {{ page_string }}
        </ul>
    </div>

"""
from django.utils.safestring import mark_safe
from copy import deepcopy
from django.http import QueryDict
class Pagination(object):
    def __init__(self, request, query_set, request_param = 'page', page_size = 10, plus=5):
        """

        :param request:请求的对象
        :param query_set:符合查询条件的数据（根据这个数据进行分页处理）
        :param request_param:在URL中传递的获取分页的参数，例如：/pretty/list/?page=296
        :param page_size:每页显示多少条数据
        :param plus:显示当前页的前（后）几页（页码）
        """
        # 深复制请求参数字典，并赋值修改参数。因为GET的请求迭代是不能修改的，需要复制。修改查询条件和翻页参数不保留的bug
        query_dict = deepcopy(request.GET)
        # 修改_mutable属性为True,就能修改用setlist(属性值，迭代值)方法修改queryDict，如query_dict.setlist('page',[11])
        query_dict._mutable = True
        self.query_dict =query_dict
        self.request_param = request_param

        page_num = request.GET.get(request_param, "1")
        if page_num.isdecimal():
            page_num = int(page_num)
        else:
            page_num = 1

        self.start = (page_num - 1) * page_size
        self.end = page_num * page_size
        self.page_queryset = query_set[self.start:self.end]
        # 先获取所有数据的数量
        self.total_count = query_set.count()


        self.page_num = page_num
        self.page_size = page_size
        self.plus = plus

        # 总数除以每页数，等于总页数和余数
        self.total_page_count, div = divmod(self.total_count, self.page_size)
        if div:
            # 余数不为0时，总页数+1
            self.total_page_count += 1

    def html(self):
        page_str_list = []
        # 首页
        self.query_dict.setlist(self.request_param,[1])
        print(self.query_dict.urlencode())
        first_page_str = '<li ><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(first_page_str)

        # 上一页
        if self.page_num > 1:
            self.query_dict.setlist(self.request_param, [self.page_num - 1])
            prev = '<li class="active"><a href="?{0}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.request_param, [1])
            prev = '<li class="disabled"><a href="?{0}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 显示当前页的前5页，后5页
        if self.page_num - self.plus > 1:
            start_page = self.page_num - self.plus
        else:
            start_page = 1
        if self.page_num + self.plus <= self.total_page_count:
            end_page = self.page_num + self.plus
        else:
            end_page = self.total_page_count

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.request_param, [i])
            if i == self.page_num:
                # 当前页面显示为已选择状态
                ele = '<li class="active"><a href="?{0}">{1}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{0}">{1}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page_num < self.total_page_count:
            self.query_dict.setlist(self.request_param, [self.page_num + 1])
            prev = '<li class="active"><a href="?{0}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.request_param, [self.total_page_count])
            prev = '<li class="disabled"><a href="?{0}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist(self.request_param, [self.total_page_count])
        last_page_str = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(last_page_str)

        # 页码跳转部分，设置为string，方便封装
        search_string = """
            <li>
                <!--输入页码进行跳转-->
                <form method="get" style="float:left;margin-left: -1px">
                    <div class="input-group" style="width: 120px">
                        <input style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0"
                                type="text" class="form-control" name="page" placeholder="页码">
                        <span class="input-group-btn">
                            <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                        </span>
                    </div>
                </form>
            </li>
            """
        page_str_list.append(search_string)
        # 使用makr_safe方法使得string转化为html元素格式
        page_string = mark_safe("".join(page_str_list))
        return page_string