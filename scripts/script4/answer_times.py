import pandas as pd
import json


def run_script04() -> pd.DataFrame:
    """
    Script para obtener un dataframe con el minuto en el que el estudiante respondió a cada pregunta durante el examen.
    El proceso es sencillo, obtenemos los datos a través del log de interacciones durante el proceso que dura el examen
    y a través del df de notas obtenermos: la hora de inicio, la hora de fin, nombre y nota.


    Returns: df_answer_times: Dataframe que contiene las horas de respuesta para cada pregunta por cada estudiante.

    """
    marks_df = pd.read_excel('files/tool_output/03_anwers_and_califications_dataframe/marks.xlsx')

    # leemos el log durante el examen
    with open('files/tool_output/01_anonymized_input/exam_logs_utf8_anonymized.json', encoding='utf-8') as json_file:
        log_json = json.load(json_file)

    json_df = pd.DataFrame(log_json)
    json_df.columns = ['Hora', 'Nombre', 'Nombre_aux', 'Tipo', 'Clase', 'Resumen', 'Descripción', 'Web', 'IP']
    json_df['Hora'] = pd.to_datetime(json_df['Hora'])  # creamos el dataframe y asignamos la hora en formato datetime

    # preparamos el dataframe que vamos a devolver
    df_answer_times = pd.DataFrame(columns=
                                   ['Nombre', 'Inicio', 'Q1_t', 'Q2_t', 'Q3_t', 'Q4_t',
                                    'Q5_t', 'Q6_t', 'Q7_t', 'Q8_t', 'Q9_t', 'Q10_t'])

    for i in range(0, marks_df.shape[0]):
        name = marks_df.iloc[i].Nombre
        start = marks_df.iloc[i].Inicio
        end = marks_df.iloc[i].Fin
        mark = marks_df.iloc[i].Nota

        json_particular_df = json_df[(json_df['Hora'] >= start)
                                     & (json_df['Hora'] <= end)
                                     & (json_df['Nombre'] == name)
                                     & (json_df['Clase'] == "Cuestionario")
                                     & ((json_df['Resumen'] == "Intento de cuestionario visualizado")
                                        | (json_df['Resumen'] == "Intento enviado"))
                                     ]
        # guardamos cuántas filas tenía antes de hacer el preprocesado.
        # Esto sirve para saber cuáles tenían > 10 visualizaciones de respuestas
        n_rows = (json_particular_df.shape[0] - 1)

        json_particular_df.reset_index(drop=True, inplace=True)

        # eliminamos la primera fila,
        # porque coincide con la hora de inicio no con la 1º respuesta
        json_particular_df = json_particular_df.drop(index=0, axis=0)
        if json_particular_df.shape[0] >= 11:
            media = (end - start) / 10
            lista_horas = []
            lista_nombre = []
            aux = start
            for _ in range(10):
                aux = aux + media
                lista_horas.append(aux)
                lista_nombre.append(name)
            datos = {'Horas': lista_horas}
            json_particular_df = pd.DataFrame(datos)

        columns = ['Q1_t', 'Q2_t', 'Q3_t', 'Q4_t', 'Q5_t', 'Q6_t', 'Q7_t', 'Q8_t', 'Q9_t', 'Q10_t']
        json_T = json_particular_df.T
        json_T.columns = columns
        json_T = json_T.head(1)
        json_T.insert(0, "Nombre", [name])
        json_T.insert(1, "Inicio", [start])
        json_T.reset_index(drop=True, inplace=True)

        df_answer_times = df_answer_times.append(json_T)

        json_T.to_excel(
            'files/tool_output/04_answers_time/individual_answer_times/'
            + str(name) + '_' + str(mark) + "#" + str(n_rows) + '.xlsx', index=False)

    df_answer_times.reset_index(drop=True, inplace=True)
    df_answer_times.to_excel('files/tool_output/04_answers_time/answer_times_merged.xlsx')
