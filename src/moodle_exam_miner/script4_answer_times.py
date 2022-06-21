import pandas as pd


def get_answer_times_df(marks_df, log_json, num_preguntas) -> pd.DataFrame:
    """
    Script para obtener un dataframe con el minuto en el que el estudiante respondió a cada pregunta durante el examen.
    El proceso es sencillo, obtenemos los datos a través del log de interacciones durante el proceso que dura el examen
    y a través del df de notas obtenermos: la hora de inicio, la hora de fin, nombre y nota.


    Returns: df_answer_times: Dataframe que contiene las horas de respuesta para cada pregunta por cada estudiante.

    """

    json_df = pd.DataFrame(log_json)
    json_df.columns = ['Hora', 'Nombre', 'Nombre_aux', 'Tipo', 'Clase', 'Resumen', 'Descripción', 'Web', 'IP']
    json_df['Hora'] = pd.to_datetime(json_df['Hora'])  # creamos el dataframe y asignamos la hora en formato datetime
    columnas_basicas = ['Nombre', 'Inicio']
    columnas_preguntas = ['Q' + str(i + 1) + "_t" for i in range(num_preguntas)]
    columnas_finales = columnas_basicas + columnas_preguntas
    # preparamos el dataframe que vamos a devolver
    df_answer_times = pd.DataFrame(columns=columnas_finales)

    for i in range(0, marks_df.shape[0]):
        name = marks_df.iloc[i].Nombre
        start = marks_df.iloc[i].Inicio
        end = marks_df.iloc[i].Fin

        json_particular_df = json_df[(json_df['Hora'] >= start)
                                     & (json_df['Hora'] <= end)
                                     & (json_df['Nombre'] == name)
                                     & (json_df['Clase'] == "Cuestionario")
                                     & ((json_df['Resumen'] == "Intento de cuestionario visualizado")
                                        | (json_df['Resumen'] == "Intento enviado"))
                                     ]

        json_particular_df.reset_index(drop=True, inplace=True)

        # eliminamos la primera fila,
        # porque coincide con la hora de inicio no con la 1º respuesta
        json_particular_df = json_particular_df.drop(index=0, axis=0)
        if json_particular_df.shape[0] >= num_preguntas + 1:
            media = (end - start) / num_preguntas
            lista_horas = []
            lista_nombre = []
            aux = start
            for _ in range(num_preguntas):
                aux = aux + media
                lista_horas.append(aux)
                lista_nombre.append(name)
            datos = {'Horas': lista_horas}
            json_particular_df = pd.DataFrame(datos)
        if json_particular_df.shape[0] >= 10:
            json_T = json_particular_df.T
            json_T.columns = columnas_preguntas
            json_T = json_T.head(1)
            json_T.insert(0, "Nombre", [name])
            json_T.insert(1, "Inicio", [start])
            json_T.reset_index(drop=True, inplace=True)

            df_answer_times = pd.concat([df_answer_times, json_T])

    df_answer_times.reset_index(drop=True, inplace=True)

    df_answer_times[['Inicio']] = df_answer_times[['Inicio']].apply(pd.to_datetime)
    df_answer_times[columnas_preguntas] = df_answer_times[columnas_preguntas].apply(pd.to_datetime)

    return df_answer_times
