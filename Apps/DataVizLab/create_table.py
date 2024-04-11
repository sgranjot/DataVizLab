from .models import CSVFile
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.table as table
import xlsxwriter


def create (request):
    selected_columns = request.POST.get('selected_columns')
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
    tabla = table.table(cellText=df_selected_columns.values, colLabels=df_selected_columns.columns, loc='center', cellLoc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.2)
    plt.show()

    # Guardar la tabla en un archivo XLSX
    nombre_archivo_xlsx = 'DataVizLab/xlsx/tabla.xlsx'
    workbook = xlsxwriter.Workbook(nombre_archivo_xlsx)
    worksheet = workbook.add_worksheet()

    # Escribir los datos en el archivo XLSX
    for i, row in enumerate(df_selected_columns.values):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)

    workbook.close()