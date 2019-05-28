# -*- coding: utf-8 -*-
import csv
import json
import os
import sys
import traceback
import dateformatting
from StringIO import StringIO
import datetime

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_protect

import medialibary
from utils.common import Pagenate

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
from io import BytesIO
from urllib import quote

import time

import xlrd
import xlwt
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect

from media.settings import BASE_DIR
from medialibary.models import MediaLibrary


def get_style(name,color=0, bold=False, italic=False):
    """指定参数单元格式"""
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.colour_index = color
    font.bold = bold
    font.italic = italic
    style.font = font
    return style


def file_down(request):
    """下载模板"""
    path = os.path.join(BASE_DIR, 'static', 'download', 'medialibary_model.csv')
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="medialibary_model.csv"'
    return response


@csrf_protect
def download_mode(request):
    """导入csv到数据库"""
    if request.method == 'GET':
        # try:
        #     page = int(request.GET.get('page', 1))
        # except Exception as e:
        #     page = 1
        # data = MediaLibrary.objects.filter(is_del=0).all()
        # paninator = Paginator(data, 10)
        # page_data = paninator.page(page)
        # print(type(page_data))
        # print(page_data)
        # print(data)
        # print(type(data))
        return render(request, 'medialibary/download_mode.html', locals())
    if request.method == 'POST':
        file_obj = request.FILES.get('file_upload_trumpl')
        ori_name = file_obj.name
        if file_obj:
            time_stamp = int(time.time())
            file_name = os.path.join(
                BASE_DIR, 'static', 'upload', ("download_mode") + str(time_stamp)
            )
            # 写入到后台
            reader = csv.reader(file_obj)
            reader.next()
            count = 0
            counts = 0
            counts2 = 0
            for parts in reader:
                try:

                    MediaLibrary.objects.create(
                        # id=parts[0].decode('GB2312').encode('utf-8'),
                        url=parts[1].decode('GB2312').encode('utf-8'),
                        secondpage=parts[2].decode('GB2312').encode('utf-8'),
                        thirdpage=parts[3].decode('GB2312').encode('utf-8'),
                        xunxun_nickname=parts[4].decode('GB2312').encode('utf-8'),
                        sousou_nickname=parts[5].decode('GB2312').encode('utf-8'),
                        website=parts[6].decode('GB2312').encode('utf-8'),
                        sitetype=parts[7].decode('GB2312').encode('utf-8'),
                        regional=parts[8].decode('GB2312').encode('utf-8'),
                         fetchlevel= int(parts[9].decode('GB2312').encode('utf-8')) if parts[9].decode('GB2312').encode('utf-8') else 2,
                        yesterdaycapture= int(parts[10].decode('GB2312').encode('utf-8')) if parts[10].decode('GB2312').encode('utf-8') else None,
                        is_author=int(parts[11].decode('GB2312').encode('utf-8')) if parts[11].decode('GB2312').encode('utf-8') else None,
                        addpaper=parts[12].decode('GB2312').encode('utf-8'),
                         addtime=parts[13].decode('GB2312').encode('utf-8'), updatetime=parts[14].decode('GB2312').encode('utf-8'),
                        latestfetchtime=parts[15].decode('GB2312').encode('utf-8'),
                        fetchstatus=int(parts[16].decode('GB2312').encode('utf-8')) if parts[16].decode('GB2312').encode('utf-8') else 1,
                         is_process=int(parts[17].decode('GB2312').encode('utf-8')) if parts[17].decode('GB2312').encode('utf-8') else 4,
                        note=parts[18].decode('GB2312').encode('utf-8').decode('GB2312').encode('utf-8'),
                        is_xuxu=int(parts[19].decode('GB2312').encode('utf-8')) if parts[19].decode('GB2312').encode('utf-8') else 3,
                        is_sousou=int(parts[20].decode('GB2312').encode('utf-8')) if parts[20].decode('GB2312').encode('utf-8') else 3,
                        many_choice=int(parts[21].decode('GB2312').encode('utf-8')) if parts[21].decode('GB2312').encode('utf-8') else None,
                        is_static = int(parts[22].decode('GB2312').encode('utf-8')) if parts[22].decode('GB2312').encode('utf-8') else 1,

                    )
                    count += 1
                    MediaLibrary.objects.update(count=count)
                except Exception as e:
                    counts += 1
            return HttpResponse('插入了%s条数据,修改了%s条数据，点击网址刷新页面返回' % (count, counts2))
        return HttpResponse('插入数据格式有误，请检查')


def show_updata_count(request):
    if request.method == 'GET':
       updata_count = MediaLibrary.objects.all()
    return render(request, 'medialibary/updata_count.html', {'updata_count': updata_count})


def export_emp_excel(request):
    """导出Excel报表"""
    # 创建Excel工作簿
    import datetime
    from django.utils.timezone import utc
    utcnow = datetime.datetime.utcnow().replace(tzinfo=utc)
    workbook = xlwt.Workbook(encoding='utf-8')
    # 向工作簿中添加工作表
    sheet = workbook.add_sheet(u'models')
    # 设置表头
    titles = ('ID', '链接','二级板面', '三级版面', '讯讯别称', '搜搜别称', '网站', '网站类型', '地域', '抓取等级',
              '昨日抓取量', '是否有作者/互动/原创转载', '添加人', '添加时间', '修改时间', '最新抓取时间', '抓取状态',
              '作者/互动/原创转载是否处理','备注',  '是否应用讯讯', '是否应用搜搜',  '更多', '是否静态')
    props = ('id', 'url', 'secondpage', 'thirdpage', 'xunxun_nickname', 'sousou_nickname','website',
                 'sitetype', 'regional', 'fetchlevel', 'yesterdaycapture', 'is_author',
                 'addpaper', 'addtime', 'updatetime', 'latestfetchtime', 'fetchstatus', 'is_process', 'note',
                'is_xuxu', 'is_sousou','many_choice', 'is_static')
    for col, title in enumerate(titles):
        sheet.write(0, col, title, get_style('Arial', color=2, bold=True))
        medialibrarys = MediaLibrary.objects.all().only(*props).order_by('yesterdaycapture')
    for row, medialibrary in enumerate(medialibrarys):
        for col, prop in enumerate(props):
            val = getattr(medialibrary, prop, '')
            if isinstance(val, MediaLibrary):
                val = val.name
            sheet.write(row + 1, col, val)
    # 提取Excel表格的数据
    buffer = StringIO()
    workbook.save(buffer)
    # 生成响应对象传输数据给浏览器
    resp = HttpResponse(buffer.getvalue())
    filename = 'models.csv'
    resp['Content-Type'] = 'application/csv'
    resp['content-disposition'] = 'attachment; filename="models.csv"'
    return resp


def get_search_data(request):
    if request.method == 'POST':
        page = int(request.POST.get('page', '1'))
        fetchstatus = request.POST.get('fetchstatus')
        is_auther = request.POST.get('is_auther')
        fetchlevel = request.POST.get('fetchlevel')
        url = request.POST.get('url')
        is_static = request.POST.get('is_static')
        is_xunxun = request.POST.get('is_xunxun')
        is_sousou = request.POST.get('is_sousou')
        page_n = 10 * (page - 1)
        page_m = 10 * page
        data = MediaLibrary.objects.filter(fetchstatus=fetchstatus).order_by('-id')
        if data:
            seconddata = data.filter(is_author=is_auther).order_by('-id')
        else:
            error = '请输入筛选内容'
            return render(request, 'medialibary/download_mode.html', {'error': error})
        if seconddata:
            thirddata = seconddata.filter(fetchlevel=fetchlevel).order_by('-id')
        else:
            error = '没有符合要求的作者状态'
            return render(request, 'medialibary/download_mode.html', {'error': error})
        if thirddata:
            fourdata = thirddata.filter(is_static=is_static).order_by('-id')
        else:
            error = '抓取等级没有符合要求的数据'
            return render(request, 'medialibary/download_mode.html', {'error': error})
        if fourdata:
            sixdata = fourdata.filter(is_xuxu=is_xunxun).order_by('-id')
        else:
            error = '是否静态在数据库没有符合状态的数据'
            return render(request, 'medialibary/download_mode.html', {'error': error})
        if sixdata:
            filter_all_count = sixdata.filter(is_sousou=is_sousou).count()
            search_data = sixdata.filter(is_sousou=is_sousou).all().order_by('-id')[page_n:page_m]
            page_items = Pagenate(page, range(0, filter_all_count), 10).json_result()
            searchdatas = []
            for s in search_data:
                searchdatas.append({
                    'id': s.id,
                    'url': s.url,
                    'secondpage': s.secondpage,
                    'thirdpage': s.thirdpage,
                    'xunxun_nickname': s.xunxun_nickname,
                    'sousou_nickname': s.sousou_nickname,
                    'website': s.website,
                    'sitetype': s.sitetype,
                    'regional': s.regional,
                    'fetchlevel': s.fetchlevel,
                    'yesterdaycapture': s.yesterdaycapture,
                    'is_author': s.is_author,
                    'addpaper': s.addpaper,
                    'addtime': s.addtime.strftime("%Y-%m-%d %H:%M:%S"),
                    'updatetime': s.updatetime.strftime("%Y-%m-%d %H:%M:%S"),
                    'latestfetchtime': s.latestfetchtime.strftime("%Y-%m-%d %H:%M:%S"),
                    'fetchstatus': s.fetchstatus,
                    'is_process': s.is_process,
                    'note': s.note,
                    'is_xuxu': s.is_xuxu,
                    'is_sousou': s.is_sousou,
                    'many_choice': s.many_choice,
                    'is_static': s.is_static
                })
                print(searchdatas)
            return HttpResponse(json.dumps({'searchdatas': searchdatas, 'page_items': page_items}))
        else:
            error = '搜索的是否应用迅迅数据库没有对应的返回值'
        return HttpResponse('ok')



def edit_brand(request, id):
    if request.method == 'GET':
        edit_medialibary = MediaLibrary.objects.filter(pk=id).first()
        return render(request, 'medialibary/edit_brand.html', {'edit_medialibary': edit_medialibary})
    if request.method == 'POST':
        url = request.POST.get('url')
        secondpage = request.POST.get('secondpage', '')
        thirdpage = request.POST.get('thirdpage', '')
        xunxun_nickname = request.POST.get('xunxun_nickname', '')
        sousou_nickname = request.POST.get('sousou_nickname', '')
        website = request.POST.get('website', '')
        sitetype = request.POST.get('sitetype', '')
        regional = request.POST.get('regional', '')
        fetchlevel = int(request.POST.get('fetchlevel', ''))
        yesterdaycapture = request.POST.get('yesterdaycapture', '')
        is_author = int(request.POST.get('is_author', ''))
        addpaper = request.POST.get('addpaper', '')
        fetchstatus = int(request.POST.get('fetchstatus', ''))
        is_process = int(request.POST.get('is_process', ''))
        note = request.POST.get('note', '')
        is_xuxu = int(request.POST.get('is_xuxu', ''))
        is_sousou = int(request.POST.get('is_sousou', ''))
        many_choice = request.POST.get('many_choice', '')
        is_static = int(request.POST.get('is_static', ''))
        pass
        try:
            # 跟新数据库数据
            MediaLibrary.objects.filter(id=id).update(
                url=url,
                secondpage=secondpage,
                thirdpage=thirdpage,
                xunxun_nickname=xunxun_nickname,
                sousou_nickname=sousou_nickname,
                website=website,
                sitetype=sitetype,
                regional=regional,
                fetchlevel=fetchlevel,
                yesterdaycapture=yesterdaycapture if yesterdaycapture else 0,
                is_author=is_author,
                addpaper=addpaper,
                fetchstatus=fetchstatus,
                is_process=is_process,
                note=note,
                is_xuxu=is_xuxu,
                is_sousou=is_sousou,
                many_choice=many_choice if many_choice else 0,
                is_static=is_static
            )
            return HttpResponse('ok')
        except Exception as e:
            return HttpResponse(e)


def del_medialibary(request, id):
    if request.method == 'POST':
        MediaLibrary.objects.filter(pk=id).update(is_del=1)
        return JsonResponse({'code': 200, 'msg': '请求成功'})