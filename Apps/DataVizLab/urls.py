from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views
from Apps.account.views import dashboard

app_name = 'DataVizLab'
urlpatterns = [
    path('', login_required(dashboard), name='index'),            # ex: /Apps/DataVizLab/
    path('create_ExcelFile/', login_required(views.CreateExcelFileView.as_view()), name='create_ExcelFile'),
    #path('create_table/', views.create_table, name='create_table'),
    path('list_ExcelFiles/', login_required(views.ListExcelFileView.as_view()), name='list_ExcelFiles'),
    path('delete_ExcelFile/<int:pk>/', login_required(views.DeleteExcelFileView.as_view()), name='delete_ExcelFile'),
    path('detail_ExcelFile/<int:pk>/', login_required(views.DetailExcelFileView.as_view()), name='detail_ExcelFile'),
    path('estructura_de_plantilla_segmentaciones/<int:pk>/', login_required(views.estructura_de_plantilla_segmentaciones), name='estructura_de_plantilla_segmentaciones'),
]
