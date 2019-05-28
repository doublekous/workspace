from django.conf.urls import url

from medialibary import views

urlpatterns = [
    url(r'download_mode/$', views.download_mode, name='download_mode'),
    url(r'export_emp_excel/$', views.export_emp_excel, name='export_emp_excel'),
    url(r'file_down/$', views.file_down, name='file_down'),
    url(r'get_search_data/$', views.get_search_data, name='get_search_data'),
    url(r'edit_brand/(\d+)$', views.edit_brand, name='edit_brand'),
    url(r'del_medialibary/(\d+)/$', views.del_medialibary, name='del_medialibary'),

]