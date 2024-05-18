import json

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .dimensions import export
from .dimensions.estructura_plantilla import departamento_area
from .dimensions.estructura_plantilla import genero
from .models import ExcelFile


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
                titles.append('Segmentación por departamento-area')
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
            # TODO Agregar mas segmentaciones....

        # Combina los títulos y las tablas en una lista de tuplas
        data_zipped = zip(titles, html_tables, graphics, dataFrames)

        # Convertir lista de dataFrames y titulos en json
        list_dataFrames_json = [df.to_json(orient='split') for df in dataFrames]
        dataFrames_json = json.dumps(list_dataFrames_json)
        titles_json = json.dumps(titles)

        return render(request, 'DataVizLab/show_data.html', {'data_zipped': data_zipped,
                                                         'titles_json': titles_json, 'dataFrames_json': dataFrames_json})
    else:
        return HttpResponse("Error: Método no permitido")


@csrf_exempt
def exportToXlsX (request):
    if request.method == 'POST':
        titles_json = request.POST.get('titles_json')
        titles = json.loads(titles_json)
        dataFrames_json = request.POST.get('dataFrames_json')
        dataFrames_str = json.loads(dataFrames_json)
        # Convertir cada cadena JSON a un DataFrame de pandas
        dataFrames = [pd.read_json(df_json, orient='split') for df_json in dataFrames_str]
        file_name = request.POST.get('file_name')
        return export.export_to_xlsx(request=request, titles=titles, dataFrames=dataFrames, file_name=file_name)
    else:
        return HttpResponse("Error: Método no permitido")
