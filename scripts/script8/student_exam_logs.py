from typing import Tuple, List

import pandas as pd


def get_student_exam_logs(merge_df, json_logs) -> Tuple[List, List]:
    """
    Función que separa los logs de cada estudiante en posiciones de una lista.
    Args:
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.
        json_logs: Logs del examen

    Returns:
        student_exam_logs (Lista con los logs de los estudiantes en una lista que contiene pandas Dataframe), student_exam_logs_name (Lista que contiene en cada posición el nombre que tendrá el archivo para guardarse.
    """
    log_json = json_logs
    student_exam_logs = []  # almacenará en cada posición un pandas Dataframe que contiene los logs de ese estudiante
    student_exam_logs_name = []  # almacenará el nombre que tendrá ese archivo

    columnas = ['Hora', 'Nombre', 'Nombre_aux', 'Tipo', 'Clase', 'Resumen', 'Descripción', 'Web', 'IP']

    json_df = pd.DataFrame(log_json)
    json_df.columns = columnas
    json_df['Hora'] = pd.to_datetime(json_df['Hora'])  # creamos el dataframe y asignamos la hora en formato datetime

    lista_ip = []  # creamos una lista que contendrá las IP, para que si dos alumnos tienen la misma IP nos avise
    for i in range(0, merge_df.shape[0]):
        nombre = merge_df.iloc[i].Código
        inicio = merge_df.iloc[i].Inicio
        fin = merge_df.iloc[i].Fin
        nota = merge_df.iloc[i].Nota

        ip = json_df['IP'][json_df['Nombre'] == nombre].iloc[0]
        json_particular_df = json_df[(json_df['Hora'] >= inicio)
                                     & (json_df['Hora'] <= fin)
                                     & (json_df['Nombre'] == nombre)
                                     & (json_df['Clase'] == "Cuestionario")
                                     & (json_df['Resumen'] == "Intento de cuestionario visualizado")
                                     ]

        # cuando un alumno tenga la misma IP que otra persona, esta IP se pondrá al final del nombre del fichero
        if ip in lista_ip:
            student_exam_logs.append(json_particular_df)
            student_exam_logs_name.append(
                str(nombre) + '_' + str(nota) + "#" + str(json_particular_df.shape[0]) + '_ip_' + str(ip) + '.xlsx'
            )

        else:  # si no, se añade la IP a la lista y se imprime solamente con nombre_nota#nºrespuestas
            lista_ip.append(json_df['IP'][json_df['Nombre'] == nombre].iloc[0])
            student_exam_logs.append(json_particular_df)
            student_exam_logs_name.append(
                str(nombre) + '_' + str(nota) + "#" + str(json_particular_df.shape[0]) + '.xlsx'
            )

    return student_exam_logs, student_exam_logs_name
