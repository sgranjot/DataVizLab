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

        '''
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            sheet_file_name = f"{original_file_name}_{sheet_name}.xlsx"
            file = df.to_excel(sheet_file_name, index=False)
            new_excel_file = ExcelFile(user=self.request.user, file=file)
            new_excel_file.save()'''

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

        for option in options:
            if option == 'Departamento/area':
                html_table = departamento_area.by_departamento_area(request=request, pk=pk)
            elif option == 'option2':
                function_for_option2()
            # Agrega más condiciones según tus opciones y funciones

        return render(request, 'DataVizLab/tabla.html', {'html_table': html_table})
    else:
        return HttpResponse("Error: Método no permitido")



'''
@login_required
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save(commit=False)
            excel_file.user = request.user            # Asignar el usuario actual al campo user
            excel_file.save()

            decrypted_data = excel_file.get_decrypted_file()
            # Creamos un objeto BytesIO para leer los datos
            buffer = BytesIO(decrypted_data)
            # Leemos el archivo Excel utilizando pd.read_excel
            df = pd.read_excel(buffer)

            columns = df.columns
            id = excel_file.id

            return render(request, 'DataVizLab/column_select.html', {'columns': columns, 'excel_file_id': id})
    else:
        form = ExcelForm()
    return render(request, 'DataVizLab/upload_excel.html', {'form': form})
'''



def create_table (request):
    selected_columns = request.POST.getlist('selected_columns')
    id = request.POST.get('excel_file_id')

    # archivo excel recuperado de la DB
    file_excel = ExcelFile.objects.get(id=id)

    decrypted_data = file_excel.get_decrypted_file()
    # Creamos un objeto BytesIO para leer los datos
    buffer = BytesIO(decrypted_data)
    # Leemos el archivo Excel utilizando pd.read_excel
    df = pd.read_excel(buffer)

    # filtramos por las columnas seleccionadas
    df_selected_columns = df[selected_columns]

    # Crear la tabla con Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    tabla = table.table(ax, cellText=df_selected_columns.values, colLabels=df_selected_columns.columns, loc='center', cellLoc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.2)
    #plt.show()

    # Obtener el nombre del archivo EXCEL sin la extensión
    excel_file_name = os.path.splitext(os.path.basename(file_excel.file.name))[0]

    # Obtener la ruta absoluta del directorio donde se guardará el archivo XLSX
    current_directory = os.path.abspath(os.path.dirname(__file__))
    xlsx_directory = os.path.join(current_directory, 'xlsx')

    # Crear el directorio 'xlsx' si no existe
    if not os.path.exists(xlsx_directory):
        os.makedirs(xlsx_directory)

    # Definir el nombre del archivo XLSX de salida con el nombre del archivo XLSX de entrada
    xlsx_file_name = f"{excel_file_name}.xlsx"
    xlsx_file_path = os.path.join(xlsx_directory, xlsx_file_name)

    # Crear el archivo XLSX y escribir los datos
    workbook = xlsxwriter.Workbook(xlsx_file_path)
    worksheet = workbook.add_worksheet()

    # Escribir los datos en el archivo XLSX
    for i, row in enumerate(df_selected_columns.values):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)

    workbook.close()

    return render(request, 'DataVizLab/view_table.html')





