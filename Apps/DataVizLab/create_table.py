from .models import ExcelFile
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.table as table
import xlsxwriter


def create (request):
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
    tabla = table.table(ax, cellText=df_selected_columns.values, colLabels=df_selected_columns.columns, loc='center',
                        cellLoc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1.2, 1.2)
    # plt.show()

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