import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd

from ...models import ExcelFile


def by_genero(request, pk):
    file_excel = ExcelFile.objects.get(id=pk)
    decrypted_data = file_excel.get_decrypted_file()
    buffer = BytesIO(decrypted_data)
    df = pd.read_excel(buffer, engine='openpyxl')

    # TABLA SIMPLE
    #gender_counts = df.groupby('Género').value_counts().unstack(fill_value=0)
    total_male = (df['Género'] == 'Hombre').sum()
    total_female = (df['Género'] == 'Mujer').sum()
    total_general = df.shape[0]

    new_df = pd.DataFrame({
        'Hombre': [total_male],
        'Mujer': [total_female],
        'Total general': [ total_general]
    })

    new_df = new_df.T

    html_table = new_df.to_html(classes='data', header=False)

    # GRAFICA TARTA
    labels = ['Hombres', 'Mujeres']
    sizes = [total_male, total_female]
    colors = ['blue', 'purple']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    for text in ax.texts:
        text.set_color('white')
    ax.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    datas = {'html_table': html_table, 'graphic': graphic, 'df': new_df}
    return datas