from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CSVFile
from .forms import CSVForm
import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.table as table
import xlsxwriter



@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = CSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.save(commit=False)
            csv_file.user = request.user            # Asignar el usuario actual al campo user
            csv_file.save()
            df = pd.read_csv(csv_file.file.path)
            columns = df.columns
            id = csv_file.id
            return render(request, 'DataVizLab/column_select.html', {'columns': columns, 'csv_file_id': id})
    else:
        form = CSVForm()
    return render(request, 'DataVizLab/upload_csv.html', {'form': form})


def create_table (request):
    selected_columns = request.POST.getlist('selected_columns')
    id = request.POST.get('csv_file_id')

    # archivo csv recuperado de la DB
    file_csv = CSVFile.objects.get(id=id)

    df = pd.read_csv(file_csv.file.path)

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

    # Obtener el nombre del archivo CSV sin la extensión
    csv_file_name = os.path.splitext(os.path.basename(file_csv.file.name))[0]

    # Obtener la ruta absoluta del directorio donde se guardará el archivo XLSX
    current_directory = os.path.abspath(os.path.dirname(__file__))
    xlsx_directory = os.path.join(current_directory, 'xlsx')

    # Crear el directorio 'xlsx' si no existe
    if not os.path.exists(xlsx_directory):
        os.makedirs(xlsx_directory)

    # Definir el nombre del archivo XLSX con el nombre del archivo CSV
    xlsx_file_name = f"{csv_file_name}.xlsx"
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





