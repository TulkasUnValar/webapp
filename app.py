from flask import Flask, render_template
import pandas as pd
import requests
import matplotlib.pyplot as plt
app = Flask(__name__,
        template_folder='templates',
        static_folder='static')
@app.route('/')
def index():
    # crear un Dataframe con los datos de thingspeak, usando el API
    # https://www.mathworks.com/help/thingspeak/readdata.html
    df = pd.read_csv('https://api.thingspeak.com/channels/1293177/feeds.csv?results=8000')
    # convertir el tipo de la fecha/hora
    df['created_at'] = pd.to_datetime(df['created_at'])
    # eliminar las columnas que no necesitamos
    df.drop(['entry_id', 'field4', 'field5', 'field6', 'field7', 'field8'], axis=1, inplace=True)
    # renombrar las columnas que si vamos a utilizar
    df.columns = ['Fecha', 'Temperatura', 'Humedad', 'Presión Atmosférica']
    # crear las gráficas de las imágenes
    for columna in df.columns[1:]:
        fig, ax = plt.subplots()
        ax.plot(df['Fecha'], df[columna])
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Pronostico de {columna}')
        plt.grid()
        # grabar la imagen
        plt.savefig(f'static/graf_{columna[:4]}.png')
        plt.close()
    # generar la página con la plantilla
    return render_template('index.html')
@app.route('/autores')
def autores():
    return '<h1>Juan Perez, Maria Lopez</h1>'
# ejecutar la aplicación
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)