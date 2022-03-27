import pandas as pd


def get_answer_times_df(marks_df, log_json) -> pd.DataFrame:
    """
    Script para obtener un dataframe con el minuto en el que el estudiante respondió a cada pregunta durante el examen.
    El proceso es sencillo, obtenemos los datos a través del log de interacciones durante el proceso que dura el examen
    y a través del df de notas obtenermos: la hora de inicio, la hora de fin, nombre y nota.


    Returns: df_answer_times: Dataframe que contiene las horas de respuesta para cada pregunta por cada estudiante.

    """

    json_df = pd.DataFrame(log_json)
    json_df.columns = ['Hora', 'Nombre', 'Nombre_aux', 'Tipo', 'Clase', 'Resumen', 'Descripción', 'Web', 'IP']
    json_df['Hora'] = pd.to_datetime(json_df['Hora'])  # creamos el dataframe y asignamos la hora en formato datetime

    # preparamos el dataframe que vamos a devolver
    df_answer_times = pd.DataFrame(
        columns=['Nombre', 'Inicio', 'Q1_t', 'Q2_t', 'Q3_t', 'Q4_t', 'Q5_t', 'Q6_t', 'Q7_t', 'Q8_t', 'Q9_t', 'Q10_t'])

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

        df_answer_times = pd.concat([df_answer_times, json_T])

    df_answer_times.reset_index(drop=True, inplace=True)

    df_answer_times[['Inicio', 'Q1_t', 'Q2_t', 'Q3_t', 'Q4_t', 'Q5_t', 'Q6_t', 'Q7_t', 'Q8_t', 'Q9_t', 'Q10_t']] = \
        df_answer_times[
            ['Inicio', 'Q1_t', 'Q2_t', 'Q3_t', 'Q4_t', 'Q5_t', 'Q6_t', 'Q7_t', 'Q8_t', 'Q9_t', 'Q10_t']].apply(
            pd.to_datetime)

    return df_answer_times
