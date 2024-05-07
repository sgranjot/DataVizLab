from django.shortcuts import render
import os

import matplotlib.pyplot as plt
import matplotlib.table as table
import pandas as pd
import xlsxwriter
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse

from .models import ExcelFile

from .dimensions.estructura_plantilla import departamento_area
from .dimensions.estructura_plantilla import genero


class CreateExcelFileView(generic.CreateView):
    model = ExcelFile
    fields = ['file']
    template_name = 'DataVizLab/upload_excel.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Asignar el usuario actual al objeto ExcelFile
        response = super().form_valid(form)

        # Verificar si el formulario es válido y si el archivo está presente
        if form.is_valid():
            # Leer el archivo xlsx cargado
            excel_file = form.save(commit=False)
            excel_file.user = self.request.user               # Asignar el usuario actual al campo user
            excel_file.save()
        return response


class ListExcelFileView(generic.ListView):
    template_name = 'DataVizLab/list_ExcelFiles.html'
    context_object_name = 'excelFile_list'

    def get_queryset(self):
        return ExcelFile.objects.filter(user=self.request.user)


class DeleteExcelFileView(generic.DeleteView):
    model = ExcelFile
    template_name = 'DataVizLab/deleteExcelFile.html'
    success_url = reverse_lazy('DataVizLab:list_ExcelFiles')


class DetailExcelFileView(generic.DetailView):
    model = ExcelFile
    template_name = 'DataVizLab/excelFileDetail.html'
    context_object_name = 'object'


def estructura_de_plantilla_segmentaciones(request, pk):
    excel_file = ExcelFile.objects.get(id=pk)
    return render(request, 'DataVizLab/estructura_de_plantilla_segmentaciones.html', {'object':excel_file})


def manage_selected_segmentations(request):
    if request.method == 'POST':
        options = request.POST.getlist('selected_segmentation')  # opciones seleccionadas
        pk = request.POST.get('excel_file_id')
        titles = []
        html_tables = []
        graphics = []
        dataFrames = []

        for option in options:
            if option == 'Departamento/area':
                titles.append('Segmentación por departamento/area')
                datas = departamento_area.by_departamento_area(request=request, pk=pk)
                html_tables.append(datas['html_table'])
                graphics.append(datas['graphic'])
                dataFrames.append(datas['df'])
            elif option == 'Género':
                titles.append('Segmentación por género')
                datas = genero.by_genero(request=request, pk=pk)
                html_tables.append(datas['html_table'])
                graphics.append(datas['graphic'])
                dataFrames.append(datas['df'])
                print('este es le dataframe en la vista',datas['df'])
            # Agrega más condiciones según tus opciones y funciones

        # Combina los títulos y las tablas en una lista de tuplas
        data = list(zip(titles, html_tables, graphics, dataFrames))

        return render(request, 'DataVizLab/tabla.html', {'data': data})
    else:
        return HttpResponse("Error: Método no permitido")


def export_to_xlsx(request):
    dataFrames = request.POST.get('dataFrames')
    print('este es el dataframe en la function',dataFrames)
    return render(request, 'DataVizLab/successful_export.html', {'dataFrames':dataFrames})
