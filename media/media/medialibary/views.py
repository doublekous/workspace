# -*- coding: utf-8 -*-
import csv
import json
import os
import sys
import time
import xlrd
import xlwt
import traceback
import dateformatting
import datetime
import xlsxwriter
import medialibary

from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from io import BytesIO, StringIO
from urllib import quote
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from media.settings import BASE_DIR
from utils.common import Pagenate
from medialibary.models import MediaLibrary

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


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
    path = os.path.join(BASE_DIR, 'static', 'download', 'medialibary_model_test1.csv')
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="medialibary_model_test.csv"'
    return response


@csrf_protect
def download_mode(request):
    """导入csv到数据库"""
    if request.method == 'GET':
        return render(request, 'medialibary/download_mode.html')
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
                update_id = MediaLibrary.objects.all().first()
                parts = [e.decode('GB2312', 'ignore').encode('utf8') for e in parts]
                try:
                    if parts[0] != '':
                        MediaLibrary.objects.filter(id=parts[0]).update(
                            url=parts[1],
                            secondpage=parts[2],
                            thirdpage=parts[3],
                            xunxun_nickname=parts[4],
                            sousou_nickname=parts[5],
                            website=parts[6],
                            sitetype=parts[7],
                            regional=parts[8],
                            fetchlevel=int(parts[9]) if parts[9] else 2,
                            yesterdaycapture=int(parts[10]) if parts[10] else None,
                            is_author=int(parts[11]) if parts[11] else None,
                            addpaper=parts[12],
                            fetchstatus=int(parts[16]) if parts[16] else 1,
                            is_process=int(parts[17]) if parts[17] else 4,
                            note=parts[18],
                            is_xuxu=int(parts[19]) if parts[19] else 3,
                            is_sousou=int(parts[20]) if parts[20] else 3,
                            many_choice=int(parts[21]) if parts[21] else None,
                            is_static=int(parts[22]) if parts[22] else 1,
                        )
                        counts += 1
                    else:
                        MediaLibrary.objects.create(
                            url=parts[1],
                            secondpage=parts[2],
                            thirdpage=parts[3],
                            xunxun_nickname=parts[4],
                            sousou_nickname=parts[5],
                            website=parts[6],
                            sitetype=parts[7],
                            regional=parts[8],
                            fetchlevel=int(parts[9]) if parts[9] else 2,
                            yesterdaycapture=int(parts[10]) if parts[10] else None,
                            is_author=int(parts[11]) if parts[11] else None,
                            addpaper=parts[12],
                            addtime=parts[13], updatetime=parts[14],
                            latestfetchtime=parts[15],
                            fetchstatus=int(parts[16]) if parts[16] else 1,
                            is_process=int(parts[17]) if parts[17] else 4,
                            note=parts[18],
                            is_xuxu=int(parts[19]) if parts[19] else 3,
                            is_sousou=int(parts[20]) if parts[20] else 3,
                            many_choice=int(parts[21]) if parts[21] else None,
                            is_static=int(parts[22]) if parts[22] else 1,
                        )
                        count += 1
                except Exception as e:
                    counts2 += 1
            return HttpResponse('插入了%s条数据,修改了%s条数据,重复插入数据%s条，点击网址刷新页面返回' % (count, counts, counts2))
        return HttpResponse('插入数据格式有误，请检查')


def export_emp_excel(request):
    """导出Excel报表"""
    # 创建Excel工作簿
    # import datetime
    # from django.utils.timezone import utc
    # utcnow = datetime.datetime.utcnow().replace(tzinfo=utc)
    global response
    if request.method == 'POST':
        fetchstatus = request.POST.get('fetchstatus')
        is_process = request.POST.get('is_process')
        fetchlevel = request.POST.get('fetchlevel')
        many_choice = request.POST.get('many_choice')
        second_many_choice = request.POST.get('second_many_choice')
        is_static = request.POST.get('is_static')
        is_xunxun = request.POST.get('is_xunxun')
        is_sousou = request.POST.get('is_sousou')
        export_dict = {}
        many_choice_dict = {
            '1': 'url__in',
            '2': 'website__in',
            '3': 'secondpage__in',
            '4': 'thirdpage__in',
            '5': 'xunxun_nickname__in',
            '6': 'sousou_nickname__in',
            '7': 'sitetype__in',
            '8': 'regional__in'
            }
        second_many_choice_list = [i.encode('utf8') for i in second_many_choice.split('\n') if i]
        # MediaLibrary.objects.filter(**{})
        export_dict[many_choice_dict[many_choice]] = second_many_choice_list
        if is_static != '3':
            export_dict['is_static'] = is_static
        if fetchstatus != '1':
            export_dict['fetchstatus'] = fetchstatus
        if is_process != '1':
            export_dict['is_process'] = is_process
        if fetchlevel != '1':
            export_dict['fetchlevel'] = fetchlevel
        if is_xunxun != '1':
            export_dict['is_xuxu'] = is_xunxun
        if is_sousou != '1':
            export_dict['is_sousou'] = is_sousou
        # workbook = xlsxwriter.Workbook()
        # # 向工作簿中添加工作表
        # sheet = workbook.add_worksheet(u'models')
        # # 设置表头
        # titles = ('ID', '链接','二级板面', '三级版面', '讯讯别称', '搜搜别称', '网站', '网站类型', '地域', '抓取等级',
        #           '昨日抓取量', '是否有作者/互动/原创转载', '添加人', '添加时间', '修改时间', '最新抓取时间', '抓取状态',
        #           '作者/互动/原创转载是否处理','备注',  '是否应用讯讯', '是否应用搜搜',  '更多', '是否静态')
        # props = ('id', 'url', 'secondpage', 'thirdpage', 'xunxun_nickname', 'sousou_nickname','website',
        #              'sitetype', 'regional', 'fetchlevel', 'yesterdaycapture', 'is_author',
        #              'addpaper', 'addtime', 'updatetime', 'latestfetchtime', 'fetchstatus', 'is_process', 'note',
        #             'is_xuxu', 'is_sousou','many_choice', 'is_static')
        # for col, title in enumerate(titles):
        #     sheet.write(0, col, title, get_style('Arial', color=2, bold=True))
        #     medialibrarys_list = []
        #     medialibrarys = MediaLibrary.objects.filter(**export_dict).all().only(*props).order_by('yesterdaycapture')
        #     medialibrarys_list.append(medialibrarys)
        # for row, medialibrary in enumerate(medialibrarys_list[0]):
        #     for col, prop in enumerate(props):
        #         val = getattr(medialibrary, prop, '')
        #         if isinstance(val, MediaLibrary):
        #             val = val.name
        #         sheet.write(row + 1, col, val)
        #     # 提取Excel表格的数据
        # buffer = BytesIO()
        # # 生成响应对象传输数据给浏览器
        # print(buffer)
        # resp = HttpResponse(buffer.getvalue(), content_type='application/msexcel')
        # filename = 'models.csv'
        # resp['content-disposition'] = 'attachment; filename="models.csv"'
        # return resp
        medialibrarys = MediaLibrary.objects.filter(**export_dict).all().order_by('-id')
        # if many_choice:
        #     many_choice_list = [int(i) for i in many_choice.split(',') if i]
        # medialibrarys = medialibrary.filter(many_choice__in=many_choice_list).all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="models.csv"'
        writer = csv.writer(response)
        writer.writerow(map(lambda x: x.encode("gbk", "ignore"), [
            u'ID', u'链接', u'二级板面', u'三级版面', u'讯讯别称', u'搜搜别称', u'网站', u'网站类型', u'地域', u'抓取等级',
            '昨日抓取量', '是否有作者/互动/原创转载', '添加人', '添加时间', '修改时间', '最新抓取时间', '抓取状态',
            u'作者/互动/原创转载是否处理',u'备注', u'是否应用讯讯', u'是否应用搜搜',  u'更多', u'是否静态'
        ]))
        for media in medialibrarys:
            new_r = [
                str(media.id), media.url, media.secondpage or "", media.thirdpage or "", media.xunxun_nickname or "", media.sousou_nickname or "", media.website or "", media.sitetype or "",
                media.regional or "", str(media.fetchlevel), str(media.yesterdaycapture or ""), str(media.is_author), media.addpaper or "", str(media.addtime), str(media.updatetime), str(media.latestfetchtime),
                str(media.fetchstatus), str(media.is_process), str(media.note or ""), str(media.is_xuxu), str(media.is_sousou), str(media.many_choice or ""), str(media.is_static)
            ]
            writer.writerow(map(lambda x: x.encode("gbk", "ignore"), new_r))
        return response
    return response


# @cache_page(60, key_prefix=None)
def get_search_data(request):
    """过滤展示数据"""
    if request.method == 'POST':
        searchdatas = MediaLibrary.objects.all()
        page = int(request.POST.get('page', '1'))
        fetchstatus = request.POST.get('fetchstatus')
        is_process = request.POST.get('is_process')
        fetchlevel = request.POST.get('fetchlevel')
        many_choice = int(request.POST.get('many_choice'))
        second_many_choice = (request.POST.get('second_many_choice'))
        is_static = request.POST.get('is_static')
        is_xunxun = request.POST.get('is_xunxun')
        is_sousou = request.POST.get('is_sousou')
        page_n = 10 * (page - 1)
        page_m = 10 * page
        export_dict = {}
        many_choice_dict = {
        1: 'url__in',
        2: 'website__in',
        3: 'secondpage__in',
        4: 'thirdpage__in',
        5: 'xunxun_nickname__in',
        6: 'sousou_nickname__in',
        7: 'sitetype__in',
        8: 'regional__in'
        }
        second_many_choice_list = [i.encode('utf8') for i in second_many_choice.split('\n') if i]
        # MediaLibrary.objects.filter(**{})
        export_dict[many_choice_dict[many_choice]] = second_many_choice_list
        if fetchstatus != '1':
            export_dict['fetchstatus'] = fetchstatus
        if is_process != '1':
            export_dict['is_process'] = is_process
        if fetchlevel != '1':
            export_dict['fetchlevel'] = fetchlevel
        if is_xunxun != '1':
            export_dict['is_xuxu'] = is_xunxun
        if is_sousou != '1':
            export_dict['is_sousou'] = is_sousou
        if is_static != '3':
            export_dict['is_static'] = is_static
        search_data = MediaLibrary.objects.filter(**export_dict).all().order_by('-id')[page_n: page_m]
        filter_all_count = MediaLibrary.objects.filter(**export_dict).all().count()
        page_items = Pagenate(page, range(0, filter_all_count), 10).json_result()
        # if many_choice != 7:
        #     export_dict[many_choice_dict[many_choice]] = second_many_choice
        #     search_data =MediaLibrary.objects.filter(**export_dict).all().order_by('-id')[page_n: page_m]
        #     filter_all_count = MediaLibrary.objects.filter(**export_dict).all().count()
        #     page_items = Pagenate(page, range(0, filter_all_count), 10).json_result()
        # elif many_choice == 7:
        #     search_data = data.filter(sitetype__in=second_many_choice_list).order_by('-id')[page_n: page_m]
        #     filter_all_count = data.filter(sitetype__in=second_many_choice_list).all().count()
        #     page_items = Pagenate(page, range(0, filter_all_count), 10).json_result()
        searchdatas = []
        for s in search_data:
            is_auther_dict = {1: '无',
                    2: '有作者',
                    3: '有互动',
                    4: '有原创',
                    23: '有作者，有互动',
                    24: '有作者，有原创',
                    25: '有作者，有转载',
                    235: '有作者，有互动，有转载',
                    234: '有作者,有互动，有原创',
                    34: '有互动，有原创',
                    35: '有互动，有转载',
                    345: '有互动，有原创，有转载',
                    2345: '有作者，有互动，有原创，有转载'
                    }
            fetchstatus_dict = {
                1: '全部',
                2: '失败',
                3: '完成'
            }
            fetchlevel_dict = {
                1: '全部',
                2: '高',
                3: '中',
                4: '低'
            }
            many_choice_dict = {
                1: '链接',
                2: '网站',
                3: '二级版面',
                4: '三级版面',
                5: '迅迅别称',
                6: '搜搜别称',
                7: '网站类型',
                8: '地域'
            }
            is_process_dict = {
                1: '全部',
                2: '已处理',
                3: '未处理',
                4: '无'
            }
            is_xuxu_dict = {
                1: '全部',
                2: '是',
                3: '否'
            }
            is_static_dict = {
                1: '静态',
                2: '动态'
            }
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
                'fetchlevel': fetchlevel_dict[s.fetchlevel],
                'yesterdaycapture': s.yesterdaycapture,
                'is_author': is_auther_dict[s.is_author],
                'addpaper': s.addpaper,
                'addtime': s.addtime.strftime("%Y-%m-%d %H:%M:%S") if s.addtime else '',
                'updatetime': s.updatetime.strftime("%Y-%m-%d %H:%M:%S") if s.updatetime else '',
                'latestfetchtime': s.latestfetchtime.strftime("%Y-%m-%d %H:%M:%S") if s.latestfetchtime else '',
                'fetchstatus': fetchstatus_dict[s.fetchstatus],
                'is_process': is_process_dict[s.is_process],
                'note': s.note,
                'is_xuxu': is_xuxu_dict[s.is_xuxu],
                'is_sousou': is_xuxu_dict[s.is_sousou],
                # 'many_choice': many_choice_dict[s.many_choice] if many_choice_dict[s.many_choice] else None,
                'is_static': is_static_dict[s.is_static]
            })
        return HttpResponse(json.dumps({'code': 200,'searchdatas': searchdatas, 'page_items': page_items}))


def edit_brand(request, id):
    """编辑媒体库数据"""
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
        fetchlevel = int(request.POST.get('fetchlevel'))
        yesterdaycapture = request.POST.get('yesterdaycapture', '')
        is_author = int(request.POST.get('is_author'))
        addpaper = request.POST.get('addpaper', '')
        fetchstatus = int(request.POST.get('fetchstatus'))
        is_process = int(request.POST.get('is_process'))
        note = request.POST.get('note', '')
        is_xuxu = int(request.POST.get('is_xuxu'))
        is_sousou = int(request.POST.get('is_sousou'))
        many_choice = request.POST.get('many_choice', '')
        is_static = int(request.POST.get('is_static'))
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
    """跟新数据库is_del状态"""
    if request.method == 'POST':
        MediaLibrary.objects.filter(pk=id).update(is_del=1)
        return JsonResponse({'code': 200, 'msg': '请求成功'})