import pandas as pd


#def by_departamento_area(request):
#TABLA COMPLETA
#file_excel = ExcelFile.objects.get(id=36)

#decrypted_data = file_excel.get_decrypted_file()

# Creamos un objeto BytesIO para leer los datos
#buffer = BytesIO(decrypted_data)
# Leemos el archivo Excel utilizando pd.read_excel
df = pd.read_excel('C:\\sw\\DataVizLab\\DataVizLab_env\\DataVizLab\\Apps\\DataVizLab\\xlsx\\datos anonimos.xlsx')
print(df.columns)

# Calculamos el número de hombres y mujeres por departamento/área
gender_counts = df.groupby('Depto/ Área')['Género'].value_counts().unstack(fill_value=0)

# Calculamos el total de personas por departamento/área
total_people = gender_counts.sum(axis=1)

# Calculamos el porcentaje horizontal de hombres y mujeres
horizontal_male_percentage = (gender_counts['Male'] / total_people) * 100
horizontal_female_percentage = (gender_counts['Female'] / total_people) * 100

# Calculamos el porcentaje vertical de hombres y mujeres
total_male = gender_counts['Male'].sum()
total_female = gender_counts['Female'].sum()
vertical_male_percentage = (gender_counts['Male'] / total_male) * 100
vertical_female_percentage = (gender_counts['Female'] / total_female) * 100

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
    'Total % Vertical': (total_people / total_people.sum()) * 100
})

# Reiniciamos el índice para obtener un DataFrame más limpio
new_df = new_df.reset_index(drop=True)



# Establecer la opción para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(new_df)





# #GRAFICA