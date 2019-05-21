from django.conf.urls import url

from medialibary import views

urlpatterns = [
    url(r'download_mode/$', views.download_mode, name='download_mode'),
    url(r'export_emp_excel/$', views.export_emp_excel, name='export_emp_excel'),
    url(r'file_down/$', views.file_down, name='file_down'),
    url(r'detail_data/$', views.detail_data, name='detail_data'),
    url(r'show_data/$', views.show_data, name='show_data'),

]