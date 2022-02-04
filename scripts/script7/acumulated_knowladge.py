import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import json
from datetime import datetime
from scripts.script6.py_collaborator_outputs import NumpyEncoder


def merge_dataframes(py_collaboartor_df: pd.DataFrame, respuestas_df: pd.DataFrame, preguntas_df: pd.DataFrame,
                     hora_respuestas_df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función une cada uno de los dataframes de entrada en un único dataframe
    Args:
        py_collaboartor_df: Dataframe pycollaborator.
        respuestas_df: Dataframe de las respuestas de los estudiantes durante el examen.
        preguntas_df: Dataframe sacado del XML con el conjunto global de preguntas ya limpio.
        hora_respuestas_df: Dataframe con las horas de cada respuesta para cada estudiante.

    Returns:
        Un dataframe "merge_df" que tiene todos la información unida.
    """
    merge_df = pd.DataFrame(data=py_collaboartor_df[['Nombre', 'Código', 'Tiempo',
                                                     'Inicio', 'Fin', 'Segundos', 'Nota', 'Productividad']]
                            , columns=['Nombre', 'Código', 'Tiempo',
                                       'Inicio', 'Fin', 'Segundos', 'Nota', 'Productividad',
                                       'Q0_t', 'Q0_q', 'Q0_a', 'Q0_m',
                                       'Q1_t', 'Q1_q', 'Q1_a', 'Q1_m',
                                       'Q2_t', 'Q2_q', 'Q2_a', 'Q2_m',
                                       'Q3_t', 'Q3_q', 'Q3_a', 'Q3_m',
                                       'Q4_t', 'Q4_q', 'Q4_a', 'Q4_m',
                                       'Q5_t', 'Q5_q', 'Q5_a', 'Q5_m',
                                       'Q6_t', 'Q6_q', 'Q6_a', 'Q6_m',
                                       'Q7_t', 'Q7_q', 'Q7_a', 'Q7_m',
                                       'Q8_t', 'Q8_q', 'Q8_a', 'Q8_m',
                                       'Q9_t', 'Q9_q', 'Q9_a', 'Q9_m',
                                       'Q10_t', 'Q10_q', 'Q10_a', 'Q10_m'])

    for i in range(0, merge_df.shape[0]):
        merge_df['Q0_t'][i] = respuestas_df['Inicio'][i]
        merge_df['Q0_a'][i] = '-'
        merge_df['Q0_q'][i] = '-'
        merge_df['Q0_m'][i] = 0
        for x in range(1, 11):
            # merge_df['Código'][i] = respuestas_df['Código'][i]
            aux = respuestas_df['Q' + str(x)][i]
            time = hora_respuestas_df['Q' + str(x) + '_t'][i]
            if aux != '-':
                merge_df['Q' + str(x) + '_t'][i] = time
                merge_df['Q' + str(x) + '_a'][i] = aux
                merge_df['Q' + str(x) + '_q'][i] = preguntas_df['Question'][preguntas_df['Answer'] == aux].values[0]
                merge_df['Q' + str(x) + '_m'][i] = preguntas_df['Mark'][preguntas_df['Answer'] == aux].values[0]
            else:
                merge_df['Q' + str(x) + '_t'][i] = time
                merge_df['Q' + str(x) + '_a'][i] = aux
                merge_df['Q' + str(x) + '_q'][i] = 'Desconocida'
                merge_df['Q' + str(x) + '_m'][i] = np.float64(0)
    merge_df = merge_df.set_index('Nombre')
    merge_df.to_excel('files/tool_output/07_acumulated_knowladge/merge_df.xlsx')
    return merge_df


def misma_pregunta_luego(x, pregunta: str, respuesta: str, hora_respuesta, merge_df: pd.DataFrame) -> (bool, str):
    """
    Devuelve el siguiente alumno que ha respondido correctamente a la misma pregunta que el estudiante_sub_i.
    Esta función sirve para la función CA (Conocimiento Acumulado) que mide una posible cadena de colaboración
    entre los estudiantes encadenando preguntas correctamente respondidas.
    Args:
        x: Número de la pregunta (1 a la 10).
        pregunta: Pregunta que estamos mirando (depende del valor de X que marca qué orden de pregunta fue).
        respuesta: Respuesta que se utilizó.
        hora_respuesta: Hora en la que se respondió.
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.

    Returns:
        Código del estudiante que respondió igual que el estudiante_sub_i la siguiente vez que esa pregunta apareció
        o puede devolver 0, False si no encuentra ese estudiante.
    """
    if len(merge_df['Código'][
               (merge_df['Q' + str(x) + '_q'] == pregunta) & (merge_df['Q' + str(x) + '_t'] > hora_respuesta)]) > 0:
        cod1 = merge_df['Código'][
            (merge_df['Q' + str(x) + '_q'] == pregunta) & (merge_df['Q' + str(x) + '_t'] > hora_respuesta)].iloc[
            0]  # el siguiente
        if len(merge_df['Código'][
                   (merge_df['Q' + str(x) + '_q'] == pregunta) & (merge_df['Q' + str(x) + '_t'] > hora_respuesta) &
                   (merge_df['Q' + str(x) + '_a'] == respuesta)]) > 0:
            cod2 = merge_df['Código'][
                (merge_df['Q' + str(x) + '_q'] == pregunta) & (merge_df['Q' + str(x) + '_t'] > hora_respuesta) &
                (merge_df['Q' + str(x) + '_a'] == respuesta)].iloc[0]  # el siguiente
            return cod1 == cod2, cod1
        else:
            return False, '0'
    else:
        return False, '0'


def CA(i: int, merge_df: pd.DataFrame) -> {}:
    """
    CA (Conocimiento Acumulado) es una función que mide una posible red sospechosa de intercambio de preguntas
    observando si se producen cadenas de estudiantes que van respondiendo la misma pregunta de forma seguida
    de manera correcta.
    Args:
        i: estudiante_sub_i
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.

    Returns:
        El conocimiento acumulado del estudiante (preguntas que el siguiente estudiante que la tuvo, respondió
        también correctamente)

    """
    student = {}
    codigo = merge_df['Código'][i]
    inicio = merge_df['Inicio'][i]
    fin = merge_df['Fin'][i]
    segundos = merge_df['Segundos'][i]
    nota = merge_df['Nota'][i]

    lista_CA_r = []  # respuestas
    lista_CA_i = []  # 1 si es pregunta 1, 2 si es pregunta 2 y así sucesivamente
    lista_CA_p = []  # pregunta
    lista_CA_c = []  # código del alumno o userXYZ
    for x in range(1, 11):
        pregunta = merge_df['Q' + str(x) + '_q'][i]
        puntuacion = merge_df['Q' + str(x) + '_m'][i]
        respuesta = merge_df['Q' + str(x) + '_a'][i]
        hora = merge_df['Q' + str(x) + '_t'][i]

        if puntuacion == 1.0:
            flag, cod = misma_pregunta_luego(x, pregunta, respuesta, hora, merge_df)
            if flag:
                lista_CA_r.append(respuesta)
                lista_CA_i.append(x)
                lista_CA_p.append(pregunta)
                lista_CA_c.append(cod)

    student["student_id"] = codigo
    student["start"] = inicio
    student["end"] = fin
    student["time_seconds"] = segundos
    student["grade"] = nota
    student["productividad"] = merge_df["Productividad"][i]
    student["respuestas"] = lista_CA_r
    student['qx'] = lista_CA_i
    student['preguntas'] = lista_CA_p
    student['cod'] = lista_CA_c

    return student


def ratio_preg(i, preguntas_df, merge_df, verbose=True) -> {}:
    """
    Ratio de aciertos y fallos para cada pregunta
    Args:
        i: pregunta_sub_i (pregunta que toca averiguar)
        preguntas_df: Dataframe sacado del XML con el conjunto global de preguntas ya limpio.
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.
        verbose: True por defecto para devolver la mayor cantidad de detalle para la salida.

    Returns:

    """
    questions = {}
    preg = preguntas_df['Question'].iloc[i]
    lista_c = []
    lista_i = []
    for x in range(1, 11):
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


def run_script07(answers_df_cleaned, df_xml_cleaned, answer_times_merged_df, py_cheat_df):
    merge_df = merge_dataframes(py_cheat_df, answers_df_cleaned, df_xml_cleaned, answer_times_merged_df)

    salida_preg = []
    for i in range(0, len(df_xml_cleaned), 4):
        salida_preg.append(ratio_preg(i, df_xml_cleaned, merge_df, verbose=False))

    ratio_preguntas = {"questions": salida_preg}

    with open('files/tool_output/07_acumulated_knowladge/outputRatioPreg.json', 'w', encoding='utf8') as outfile:
        json.dump(ratio_preguntas, outfile, indent=2, cls=NumpyEncoder, ensure_ascii=False)

    salida = []
    for i in range(len(merge_df)):
        salida.append(CA(i, merge_df))

    conocimiento_acumulado = {"students": salida}

    with open('files/tool_output/07_acumulated_knowladge/outputCA.json', 'w', encoding='utf8') as outfile:
        json.dump(conocimiento_acumulado, outfile, indent=2, cls=NumpyEncoder, ensure_ascii=False)

    result = merge_df.to_json(index='Nombre', orient="index", date_format='iso', date_unit='s')
    merge_df_json = json.loads(result)

    with open('files/tool_output/07_acumulated_knowladge/merge_df.json', 'w', encoding='utf8') as outfile:
        json.dump(merge_df_json, outfile, indent=2, cls=NumpyEncoder, ensure_ascii=False)

    merge_df = merge_df_columns_to_datetime64(merge_df)

    return merge_df, ratio_preguntas, conocimiento_acumulado, merge_df_json


def merge_df_columns_to_datetime64(merge_df):
    """
    Función que cambia las columnas con formato object a datetime64 para mayor precisión
    Args:
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.

    Returns:
        merge_df con las columnas _t en formato datetime.
    """
    merge_df['Q0_t'] = pd.to_datetime(merge_df['Q0_t'])
    merge_df['Q1_t'] = pd.to_datetime(merge_df['Q1_t'])
    merge_df['Q2_t'] = pd.to_datetime(merge_df['Q2_t'])
    merge_df['Q3_t'] = pd.to_datetime(merge_df['Q3_t'])
    merge_df['Q4_t'] = pd.to_datetime(merge_df['Q4_t'])
    merge_df['Q5_t'] = pd.to_datetime(merge_df['Q5_t'])
    merge_df['Q6_t'] = pd.to_datetime(merge_df['Q6_t'])
    merge_df['Q7_t'] = pd.to_datetime(merge_df['Q7_t'])
    merge_df['Q8_t'] = pd.to_datetime(merge_df['Q8_t'])
    merge_df['Q9_t'] = pd.to_datetime(merge_df['Q9_t'])
    merge_df['Q10_t'] = pd.to_datetime(merge_df['Q10_t'])
    return merge_df
