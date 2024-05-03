import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
from io import BytesIO

from django.shortcuts import render
from ...models import ExcelFile

def by_departamento_area(request, pk):
    #TABLA COMPLETA
    file_excel = ExcelFile.objects.get(id=pk)

    decrypted_data = file_excel.get_decrypted_file()

    # Creamos un objeto BytesIO para leer los datos
    buffer = BytesIO(decrypted_data)
    # Leemos el archivo Excel utilizando pd.read_excel
    #current_directory = os.getcwd()
    #print("Directorio de trabajo actual:", current_directory)
    df = pd.read_excel('Apps/DataVizLab/xlsx/datos.xlsx')
    #print(df.columns)

    # Calculamos el número de hombres y mujeres por departamento/área
    gender_counts = df.groupby('Depto/ Área')['Género'].value_counts().unstack(fill_value=0)

    # Calculamos el total de personas por departamento/área
    total_people = gender_counts.sum(axis=1)

    # Calculamos el porcentaje horizontal de hombres y mujeres
    horizontal_male_percentage = ((gender_counts['Hombre'] / total_people) * 100).__round__(2)
    horizontal_female_percentage = ((gender_counts['Mujer'] / total_people) * 100).__round__(2)

    # Calculamos el porcentaje vertical de hombres y mujeres
    total_male = gender_counts['Hombre'].sum()
    total_female = gender_counts['Mujer'].sum()
    vertical_male_percentage = ((gender_counts['Hombre'] / total_male) * 100).__round__(2)
    vertical_female_percentage = ((gender_counts['Mujer'] / total_female) * 100).__round__(2)

    # Creamos el nuevo DataFrame
    new_df = pd.DataFrame({
        'Depto/ Área': gender_counts.index,
        'Número de hombres': gender_counts['Hombre'],
        '% Vertical de hombres': vertical_male_percentage,
        '% Horizontal de hombres': horizontal_male_percentage,
        'Número de mujeres': gender_counts['Mujer'],
        '% Vertical de mujeres': vertical_female_percentage,
        '% Horizontal de mujeres': horizontal_female_percentage,
        'Total de personas': total_people,
        'Total % Vertical': ((total_people / total_people.sum()) * 100).__round__(2)
    })

    # Reiniciamos el índice para obtener un DataFrame más limpio
    new_df = new_df.reset_index(drop=True)

    # Añadir fila de totales:
    # Definir el texto para la primera columna
    texto_primera_columna = 'Total general'

    # Eliminar la primera columna
    df_sin_primera_columna = new_df.drop(columns=['Depto/ Área'])

    # Calcular la suma de las columnas restantes
    suma_columnas = df_sin_primera_columna.sum().__round__(2)

    # Agregar una fila al DataFrame con las sumas
    fila_suma = pd.DataFrame([texto_primera_columna] + list(suma_columnas), index=new_df.columns).T
    new_df = new_df._append(fila_suma, ignore_index=True)

    #calcular la % horizontal de hombres y mujeres total y remplazarla por el valor de la suma
    last_row = new_df.iloc[-1]
    last_row['% Horizontal de hombres'] = (last_row['Número de hombres'] / last_row['Total de personas'] * 100).__round__(2)
    last_row['% Horizontal de mujeres'] = (last_row['Número de mujeres'] / last_row['Total de personas'] * 100).__round__(2)

    new_df.iloc[-1] = last_row

    # Establecer la opción para mostrar todas las filas y columnas en la salida por consola
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    new_df = new_df

    #print(new_df)

    #reenderizamos la tabla en el html
    html_table = new_df.to_html(classes='data', index=False)
    #return html_table


    # GRAFICA
    df_grafica = pd.DataFrame({
        'Depto/ Área': gender_counts.index,
        '% Horizontal de hombres': horizontal_male_percentage,
        '% Horizontal de mujeres': horizontal_female_percentage
    })

    df_grafica.reset_index(drop=True)

    # Crea la gráfica de barras horizontales
    num_departamentos = len(df_grafica)
    #fig_width = num_departamentos * 0.5
    plt.figure(figsize=(12, num_departamentos * 0.35))
    # Crea las barras de hombres
    bars1 = plt.barh(df_grafica['Depto/ Área'], df_grafica['% Horizontal de hombres'], color='blue', label='Hombres', zorder=2)
    # Crea las barras de mujeres
    bars2 = plt.barh(df_grafica['Depto/ Área'], df_grafica['% Horizontal de mujeres'],
                     left=df_grafica['% Horizontal de hombres'],
                     color='purple', label='Mujeres', zorder=2)

    # Imprime los porcentajes dentro de las barras de hombres
    for bar in bars1:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height() / 2, f'{width}%', ha='left', va='center', color='white', zorder=3)

    # Imprime los porcentajes dentro de las barras de mujeres
    for bar in bars2:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height() / 2, f'{width}%', ha='right', va='center', color='white', zorder=3)
    plt.xlabel('Porcentaje')
    plt.ylabel('Departamento')
    plt.title('Porcentaje de Hombres y Mujeres por Departamento')
    plt.legend()
    plt.grid(True)
    #plt.show()

    # Ajusta el espacio entre el borde superior del lienzo y el comienzo de las barras
    plt.ylim(-3, num_departamentos + 0.5)
    # Ajusta el espacio entre el borde inferior del lienzo y el final de las barras
    plt.gca().invert_yaxis()
    plt.tight_layout()

    # Personaliza los límites y los intervalos del eje x
    plt.xticks(range(0, 101, 10))

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    datas = {'html_table': html_table, 'graphic': graphic}

    return datas