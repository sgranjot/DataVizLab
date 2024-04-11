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

    # Guardar la tabla en un archivo XLSX
    nombre_archivo_xlsx = os.path.join('E:\proyectos\DataVizLab\DataVizLab_env\DataVizLab\\xlsx', 'tabla.xlsx')
    workbook = xlsxwriter.Workbook(nombre_archivo_xlsx)
    worksheet = workbook.add_worksheet()

    # Escribir los datos en el archivo XLSX
    for i, row in enumerate(df_selected_columns.values):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)

    workbook.close()

    return render(request, 'DataVizLab/view_table.html')