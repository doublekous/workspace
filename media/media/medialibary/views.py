# -*- coding: utf-8 -*-
import csv
import json
import os
import sys
import dateformatting
from StringIO import StringIO
import datetime

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_protect

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
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

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
    path = os.path.join(BASE_DIR, 'static', 'download', 'model2.csv')
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="model2.csv"'
    return response


@csrf_protect
def download_mode(request):
    """导入csv到数据库"""
    if request.method == 'GET':
        # try:
        #     page = int(request.GET.get('page', 1))
        # except Exception as e:
        #     page = 1
        data = MediaLibrary.objects.all()
        paginator = Paginator(data, 8)
        # page_data = Paginator.page(page)
        return render(request, 'medialibary/download_mode.html', {'data': data})
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
                         fetchlevel=parts[9].decode('GB2312').encode('utf-8'),
                        yesterdaycapture=parts[10].decode('GB2312').encode('utf-8'),
                        is_author=parts[11].decode('GB2312').encode('utf-8'), addpaper=parts[12].decode('GB2312').encode('utf-8'),
                         addtime=parts[13].decode('GB2312').encode('utf-8'), updatetime=parts[14].decode('GB2312').encode('utf-8'),
                        latestfetchtime=parts[15].decode('GB2312').encode('utf-8'),
                        fetchstatus=parts[15].decode('GB2312').encode('utf-8'),
                         is_process=parts[17].decode('GB2312').encode('utf-8'),
                        note=parts[18].decode('GB2312').encode('utf-8').decode('GB2312').encode('utf-8'),
                        is_xuxu=parts[19].decode('GB2312').encode('utf-8'), is_sousou=parts[20].decode('GB2312').encode('utf-8'),
                        many_choice=parts[21].decode('GB2312').encode('utf-8'))
                    count += 1
                    MediaLibrary.objects.update(count=count)
                    return HttpResponse('插入了%s条数据,重复插入了%s条数据，点击网址刷新页面返回' % (count, counts))
                except Exception as e:
                    counts += 1
        return HttpResponse('亲，这是您刚刚上传过的文件')
        # return render(request, 'medialibary/updata_count.html')



def show_updata_count(request):
    if request.method == 'GET':
       updata_count = MediaLibrary.objects.all()
    return render(request, 'medialibary/updata_count.html', {'updata_count': updata_count})

def export_emp_excel(request):
    """导出Excel报表"""
    # 创建Excel工作簿
    workbook = xlwt.Workbook(encoding='utf-8')
    # 向工作簿中添加工作表
    sheet = workbook.add_sheet(u'models')
    # 设置表头
    titles = ('ID', '链接','二级板面', '三级版面', '讯讯别称', '搜搜别称', '网站', '网站类型', '地域', '抓取等级',
              '昨日抓取量', '是否有作者/互动/原创转载', '添加人', '添加时间', '修改时间', '最新抓取时间', '抓取状态',
              '作者/互动/原创转载是否处理','备注',  '是否应用讯讯', '是否应用搜搜',  '更多')
    props = ('id', 'url', 'secondpage', 'thirdpage', 'xunxun_nickname', 'sousou_nickname','website',
                 'sitetype', 'regional', 'fetchlevel', 'yesterdaycapture', 'is_author',
                 'addpaper', 'addtime', 'updatetime', 'latestfetchtime', 'fetchstatus', 'is_process', 'note',
                'is_xuxu', 'is_sousou','many_choice')
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

def show_data(request):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            page = 1
        data = MediaLibrary.objects.all()
        paginator = Paginator(data, 5)
        page_data = paginator.page(page)
        return render(request, 'medialibary/download_mode.html', {'data': data, 'page_data': page_data})










