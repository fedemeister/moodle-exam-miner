from typing import Tuple, Dict, List

import numpy as np
import pandas as pd
import json

IDENTIFICADOR = 'Código'


def merge_dataframes(py_cheat_df: pd.DataFrame, respuestas_df: pd.DataFrame, preguntas_df: pd.DataFrame,
                     hora_respuestas_df: pd.DataFrame, marks_df: pd.DataFrame, num_preguntas: int) -> pd.DataFrame:
    """
    Esta función une cada uno de los dataframes de entrada en un único dataframe
    Args:
        py_cheat_df: Dataframe py_collaborator.
        respuestas_df: Dataframe de las respuestas de los estudiantes durante el examen.
        preguntas_df: Dataframe sacado del XML con el conjunto global de preguntas ya limpio.
        hora_respuestas_df: Dataframe con las horas de cada respuesta para cada estudiante.
        marks_df: Dataframe con las notas para cada respuesta que tuvieron los estudiantes
        num_preguntas: número de preguntas que tiene el examen (se calcula al principio del algoritmo y se va usando)
    Returns:
        Un dataframe "merge_df" que tiene todos la información unida.
    """
    columnas_basicas = ['Nombre', 'Código', 'Tiempo', 'Inicio', 'Fin', 'Segundos', 'Nota', 'Productividad']
    columnas_q0 = ['Q0_t', 'Q0_q', 'Q0_a', 'Q0_m']
    columnas_preguntas_t = ['Q' + str(i + 1) + '_t' for i in range(num_preguntas)]
    columnas_preguntas_q = ['Q' + str(i + 1) + '_q' for i in range(num_preguntas)]
    columnas_preguntas_a = ['Q' + str(i + 1) + '_a' for i in range(num_preguntas)]
    columnas_preguntas_m = ['Q' + str(i + 1) + '_m' for i in range(num_preguntas)]

    columnas_finales = \
        columnas_q0 + columnas_basicas + columnas_preguntas_t + \
        columnas_preguntas_q + columnas_preguntas_a + columnas_preguntas_m
    merge_df = pd.DataFrame(
        data=py_cheat_df[columnas_basicas],
        columns=columnas_finales)

    for i in range(0, merge_df.shape[0]):
        merge_df['Q0_t'][i] = respuestas_df['Inicio'][i]
        merge_df['Q0_a'][i] = '-'
        merge_df['Q0_q'][i] = '-'
        merge_df['Q0_m'][i] = 0
        for x in range(1, num_preguntas + 1):
            aux = respuestas_df['Q' + str(x)][i]
            nota = float(marks_df['Q' + str(x)][i])
            time = hora_respuestas_df['Q' + str(x) + '_t'][i]
            pregunta = \
                preguntas_df['Question'][(preguntas_df['Answer'] == aux) & (preguntas_df['Mark'] == nota)].values[0]
            if aux != '-':
                merge_df['Q' + str(x) + '_t'][i] = time
                merge_df['Q' + str(x) + '_a'][i] = aux
                merge_df['Q' + str(x) + '_q'][i] = pregunta
                merge_df['Q' + str(x) + '_m'][i] = nota
            else:
                merge_df['Q' + str(x) + '_t'][i] = time
                merge_df['Q' + str(x) + '_a'][i] = aux
                merge_df['Q' + str(x) + '_q'][i] = 'Desconocida'
                merge_df['Q' + str(x) + '_m'][i] = np.float64(0)
    merge_df = merge_df.set_index('Nombre')
    return merge_df


def misma_pregunta_luego(x, pregunta: str, respuesta: str, hora_respuesta, merge_df: pd.DataFrame) -> (bool, str):
    """
    Devuelve el siguiente alumno que ha respondido correctamente a la misma pregunta que el estudiante_sub_i.
    Esta función sirve para la función conocimiento_acumulado (Conocimiento Acumulado) que mide una posible cadena de colaboración
    entre los estudiantes encadenando preguntas correctamente respondidas.
    Args:
        x: Número de la pregunta (1 a num_preguntas).
        pregunta: Pregunta que estamos mirando (depende del valor de X que marca qué orden de pregunta fue).
        respuesta: Respuesta que se utilizó.
        hora_respuesta: Hora en la que se respondió.
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.

    Returns:
        Código del estudiante que respondió igual que el estudiante_sub_i la siguiente vez que esa pregunta apareció
        o puede devolver 0, False si no encuentra ese estudiante.
    """
    if len(merge_df[IDENTIFICADOR]
           [(merge_df['Q' + str(x) + '_q'] == pregunta) &
            (merge_df['Q' + str(x) + '_t'] > hora_respuesta)]) > 0:
        cod1 = merge_df[IDENTIFICADOR][(merge_df['Q' + str(x) + '_q'] == pregunta) &
                                       (merge_df['Q' + str(x) + '_t'] > hora_respuesta)].iloc[0]  # el siguiente
        if len(merge_df[IDENTIFICADOR]
               [(merge_df['Q' + str(x) + '_q'] == pregunta) &
                (merge_df['Q' + str(x) + '_t'] > hora_respuesta) &
                (merge_df['Q' + str(x) + '_a'] == respuesta)]) > 0:
            cod2 = merge_df[IDENTIFICADOR][
                (merge_df['Q' + str(x) + '_q'] == pregunta) & (merge_df['Q' + str(x) + '_t'] > hora_respuesta) &
                (merge_df['Q' + str(x) + '_a'] == respuesta)].iloc[0]  # el siguiente
            return cod1 == cod2, cod1
        else:
            return False, '0'
    else:
        return False, '0'


def conocimiento_acumulado(i: int, merge_df: pd.DataFrame, num_preguntas: int) -> {}:
    """
    conocimiento_acumulado (Conocimiento Acumulado) es una función que mide una posible red sospechosa de intercambio de preguntas
    observando si se producen cadenas de estudiantes que van respondiendo la misma pregunta de forma seguida
    de manera correcta.
    Args:
        i: estudiante_sub_i
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.
        num_preguntas: número de preguntas que tiene el examen (se calcula al principio del algoritmo y se va usando)
    Returns:
        El conocimiento acumulado del estudiante (preguntas que el siguiente estudiante que la tuvo, respondió
        también correctamente)

    """
    student = {}
    codigo = merge_df[IDENTIFICADOR][i]
    inicio = merge_df['Inicio'][i]
    fin = merge_df['Fin'][i]
    segundos = merge_df['Segundos'][i]
    nota = merge_df['Nota'][i]

    lista_ca_r = []  # respuestas
    lista_ca_i = []  # 1 si es pregunta 1, 2 si es pregunta 2 y así sucesivamente
    lista_ca_p = []  # pregunta
    lista_ca_c = []  # código del alumno o userXYZ
    for x in range(1, num_preguntas + 1):
        pregunta = merge_df['Q' + str(x) + '_q'][i]
        puntuacion = merge_df['Q' + str(x) + '_m'][i]
        respuesta = merge_df['Q' + str(x) + '_a'][i]
        hora = merge_df['Q' + str(x) + '_t'][i]

        if puntuacion == 1.0:
            flag, cod = misma_pregunta_luego(x, pregunta, respuesta, hora, merge_df)
            if flag:
                lista_ca_r.append(respuesta)
                lista_ca_i.append(x)
                lista_ca_p.append(pregunta)
                lista_ca_c.append(cod)

    student["student_id"] = codigo
    student["start"] = inicio
    student["end"] = fin
    student["time_seconds"] = segundos
    student["grade"] = nota
    student["productividad"] = merge_df["Productividad"][i]
    student["respuestas"] = lista_ca_r
    student['qx'] = lista_ca_i
    student['preguntas'] = lista_ca_p
    student['cod'] = lista_ca_c

    return student


def ratio_preg(i: int, preguntas_df: pd.DataFrame, merge_df: pd.DataFrame, num_preguntas: int, verbose=True) -> {}:
    """
    Ratio de aciertos y fallos para cada pregunta
    Args:
        i: pregunta_sub_i (pregunta que toca averiguar)
        preguntas_df: Dataframe sacado del XML con el conjunto global de preguntas ya limpio.
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.
        verbose: True por defecto para devolver la mayor cantidad de detalle para la salida.
        num_preguntas: número de preguntas que tiene el examen (se calcula al principio del algoritmo y se va usando)

    Returns:

    """
    questions = {}
    preg = preguntas_df['Question'].iloc[i]
    lista_c = []
    lista_i = []
    for x in range(1, num_preguntas + 1):
        len_p = len(merge_df['Q' + str(x) + '_q'][merge_df['Q' + str(x) + '_q'] == preg])
        if len_p > 1:
            lista_c = merge_df['Q' + str(x) + '_a'][
                (merge_df['Q' + str(x) + '_q'] == preg) & (merge_df['Q' + str(x) + '_m'] == 1.0)].tolist()
            lista_i = merge_df['Q' + str(x) + '_a'][
                (merge_df['Q' + str(x) + '_q'] == preg) & (merge_df['Q' + str(x) + '_m'] == -0.25)].tolist()
            if verbose:
                len_c = len(lista_c)
                len_i = len(lista_i)
                # if len_c and len_i != 0:
                questions['preg'] = preg
                questions['lista_c'] = lista_c
                questions['lista_i'] = lista_i
                questions['count_correctas'] = len_c
                questions['count_incorrectas'] = len_i
                questions['porcentaje_acertadas'] = (len_c / len_p)
            else:
                aux = set(lista_c)
                lista_c2 = list(aux)
                aux = set(lista_i)
                lista_i2 = list(aux)
                len_c = len(lista_c)
                len_i = len(lista_i)
                # if len_c and len_i != 0:
                questions['preg'] = preg
                questions['lista_c'] = lista_c2
                questions['lista_i'] = lista_i2
                questions['count_correctas'] = len_c
                questions['count_incorrectas'] = len_i
                questions['porcentaje_acertadas'] = (len_c / len_p)

    return questions


def run_script07(answers_df_cleaned, df_xml_cleaned, answer_times_merged_df, py_cheat_df, marks_df, num_preguntas) -> \
        Tuple[pd.DataFrame, Dict, Dict, List]:
    merge_df = merge_dataframes(py_cheat_df, answers_df_cleaned, df_xml_cleaned, answer_times_merged_df, marks_df,
                                num_preguntas)

    salida_preg = []
    for i in range(0, len(df_xml_cleaned), 4):
        salida_preg.append(ratio_preg(i, df_xml_cleaned, merge_df, num_preguntas, verbose=False))

    ratio_preguntas = {"questions": salida_preg}

    salida = []
    for i in range(len(merge_df)):
        salida.append(conocimiento_acumulado(i, merge_df, num_preguntas))

    conocimiento_acumulado_salida = {"students": salida}

    result = merge_df.to_json(index='Nombre', orient="index", date_format='iso', date_unit='s')
    merge_df_json = json.loads(result)

    merge_df = merge_df_columns_to_datetime64(merge_df, num_preguntas)

    return merge_df, ratio_preguntas, conocimiento_acumulado_salida, merge_df_json


def merge_df_columns_to_datetime64(merge_df: pd.DataFrame, num_preguntas: int) -> pd.DataFrame:
    """
    Función que cambia las columnas con formato object a datetime64 para mayor precisión
    Args:
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.
        num_preguntas: número de preguntas que tiene el examen (se calcula al principio del algoritmo y se va usando)
    Returns:
        merge_df con las columnas _t en formato datetime.
    """

    columnas_preguntas_t = ['Q' + str(i) + '_t' for i in range(num_preguntas + 1)]
    merge_df[columnas_preguntas_t] = merge_df[columnas_preguntas_t].apply(pd.to_datetime)
    return merge_df
