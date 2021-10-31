import pandas as pd
import json

def run_script04():
    # leemos nuestro maravilloso excel con toda la información
    calificaciones_df = pd.read_excel('files/tool_output/03_anwers_and_califications_dataframe/marks.xlsx')

    # leemos el log durante el examen
    with open('files/tool_output/01_anonymized_input/exam_logs_utf8_anonymized.json', encoding='utf-8') as json_file:
        log_json = json.load(json_file)

    columnas = ['Hora', 'Nombre', 'Nombre_aux', 'Tipo', 'Clase', 'Resumen', 'Descripción', 'Web', 'IP']
    json_df = pd.DataFrame(log_json)
    json_df.columns = columnas
    json_df['Hora'] = pd.to_datetime(json_df['Hora'])  # creamos el dataframe y asignamos la hora en formato datetime

    df_append = pd.DataFrame(columns=
                            ['Nombre', 'Inicio', 'Q1_t', 'Q2_t', 'Q3_t', 'Q4_t',
                            'Q5_t', 'Q6_t', 'Q7_t', 'Q8_t', 'Q9_t', 'Q10_t'])

    for i in range(0, calificaciones_df.shape[0]):
        nombre = calificaciones_df.iloc[i].Nombre
        inicio = calificaciones_df.iloc[i].Inicio
        fin = calificaciones_df.iloc[i].Fin
        nota = calificaciones_df.iloc[i].Nota

        json_particular_df = json_df[(json_df['Hora'] >= inicio)
                                    & (json_df['Hora'] <= fin)
                                    & (json_df['Nombre'] == nombre)
                                    & (json_df['Clase'] == "Cuestionario")
                                    & ((json_df['Resumen'] == "Intento de cuestionario visualizado")
                                        | (json_df['Resumen'] == "Intento enviado"))
                                    ]
        # guardamos cuántas filas tenía antes de hacer el preprocesado.
        # Esto sirve para saber cuáles tenían > 10 visualizaciones de respuestas
        shape = (json_particular_df.shape[0] - 1)

        json_particular_df.reset_index(drop=True, inplace=True)

        # eliminamos la primera fila,
        # porque coincide con la hora de inicio no con la 1º respuesta
        json_particular_df = json_particular_df.drop(index=0, axis=0)
        if (json_particular_df.shape[0] >= 11):
            media = (fin - inicio) / 10
            lista_horas = []
            lista_nombre = []
            aux = inicio
            for i in range(10):
                aux = aux + media
                lista_horas.append(aux)
                lista_nombre.append(nombre)
            datos = {'Horas': lista_horas}
            json_particular_df = pd.DataFrame(datos)

        columnas = ['Q1_t', 'Q2_t', 'Q3_t', 'Q4_t', 'Q5_t', 'Q6_t', 'Q7_t', 'Q8_t', 'Q9_t', 'Q10_t']
        json_T = json_particular_df.T
        json_T.columns = columnas
        json_T = json_T.head(1)
        json_T.insert(0, "Nombre", [nombre])
        json_T.insert(1, "Inicio", [inicio])
        json_T.reset_index(drop=True, inplace=True)

        df_append = df_append.append(json_T)

        json_T.to_excel(
            'files/tool_output/04_answers_time/individual_answer_times/' + str(nombre) + '_' + str(nota) + "#" + str(
                shape) + '.xlsx', index=False)

    df_append.reset_index(drop=True, inplace=True)
    df_append.to_excel('files/tool_output/04_answers_time/answer_times_merged.xlsx')
