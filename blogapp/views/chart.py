from django.shortcuts import render
from django.http.response import JsonResponse
def chart_list(request):
    """数据统计"""
    return  render(request,'chart_list.html')

def chart_bar(request):
    """构造柱状统计图的数据"""
    title_text = '员工月度订单销量'
    legend_data = ['张三','李四']
    xAxis_data = ['一月', '二月', '三月', '四月', '五月', '六月']
    series = [
              {
                "name": '张三',
                "type": 'bar',
                "data": [5, 20, 36, 40, 10, 40]
              },
            {
                'name': '李四',
                'type': 'bar',
                'data': [23, 40, 35, 15, 10, 20]
              }
            ]
    result = {
        'status':True,
        'data':{
            'title_text': title_text,
            'legend_data': legend_data,
            'xAxis_data': xAxis_data,
            'series': series,
        }

    }
    return JsonResponse(result)

def chart_pie(request):
    """饼状图构造数据"""
    result = {
        'status': True,
        'data': [
            {'value': 1048, 'name': 'IT部门'},
            {'value': 735, 'name': '营销部门'},
            {'value': 580, 'name': '运维部门'},
            {'value': 484, 'name': '售后服务部门'},
            {'value': 300, 'name': '领导组'},
        ]

    }
    return JsonResponse(result)

def chart_line(request):
    """折线图构造数据"""
    result = {
        'status': True,
        'data':{
            'legend_data': ['上海', '广东', '广西'],
            'xAxis_data': ['1月', '2月', '3月', '4月', '5月', '6月', '7月'],
            'series_data': [
                {
                    'name': '上海',
                    'type': 'line',
                    'stack': 'Total',
                    'data': [120, 132, 101, 134, 90, 230, 210]
                },
                {
                    'name': '广东',
                    'type': 'line',
                    'stack': 'Total',
                    'data': [220, 182, 191, 234, 290, 330, 310]
                },
                {
                    'name': '广西',
                    'type': 'line',
                    'stack': 'Total',
                    'data': [820, 932, 901, 934, 1290, 1330, 1320]
                }
            ]
        }
    }
    return JsonResponse(result)