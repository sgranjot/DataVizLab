from .models import ExcelFile


def by_genero(request):
    #GRAFICA
    # archivo excel recuperado de la DB
    file_excel = ExcelFile.objects.get(id=36)

    decrypted_data = file_excel.get_decrypted_file()

    # Creamos un objeto BytesIO para leer los datos
    buffer = BytesIO(decrypted_data)
    # Leemos el archivo Excel utilizando pd.read_excel
    df = pd.read_excel(buffer)

    #TABLA SIMPLE

    #TARTA