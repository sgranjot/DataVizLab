import pandas as pd


#def by_departamento_area(request):
#TABLA COMPLETA
#file_excel = ExcelFile.objects.get(id=36)

#decrypted_data = file_excel.get_decrypted_file()

# Creamos un objeto BytesIO para leer los datos
#buffer = BytesIO(decrypted_data)
# Leemos el archivo Excel utilizando pd.read_excel
df = pd.read_excel('E:\\proyectos\\DataVizLab\\DataVizLab_env\\DataVizLab\\Apps\\DataVizLab\\xlsx\\datos anonimos.xlsx')
print(df.columns)

# Calculamos el número de hombres y mujeres por departamento/área
gender_counts = df.groupby('Depto/ Área')['Género'].value_counts().unstack(fill_value=0)

# Calculamos el total de personas por departamento/área
total_people = gender_counts.sum(axis=1)

# Calculamos el porcentaje horizontal de hombres y mujeres
horizontal_male_percentage = ((gender_counts['Male'] / total_people) * 100).__round__(2)
horizontal_female_percentage = ((gender_counts['Female'] / total_people) * 100).__round__(2)

# Calculamos el porcentaje vertical de hombres y mujeres
total_male = gender_counts['Male'].sum()
total_female = gender_counts['Female'].sum()
vertical_male_percentage = ((gender_counts['Male'] / total_male) * 100).__round__(2)
vertical_female_percentage = ((gender_counts['Female'] / total_female) * 100).__round__(2)

# Creamos el nuevo DataFrame
new_df = pd.DataFrame({
    'Depto/ Área': gender_counts.index,
    'Número de hombres': gender_counts['Male'],
    '% Vertical de hombres': vertical_male_percentage,
    '% Horizontal de hombres': horizontal_male_percentage,
    'Número de mujeres': gender_counts['Female'],
    '% Vertical de mujeres': vertical_female_percentage,
    '% Horizontal de mujeres': horizontal_female_percentage,
    'Total de personas': total_people,
    'Total % Vertical': ((total_people / total_people.sum()) * 100).__round__(2)
})

# Reiniciamos el índice para obtener un DataFrame más limpio
new_df = new_df.reset_index(drop=True)

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

# Establecer la opción para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

new_df = new_df

print(new_df)



# #GRAFICA