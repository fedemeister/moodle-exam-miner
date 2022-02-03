from typing import Union, Any, Tuple, Dict, List

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from datetime import datetime
import json


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def estudiantes_que_terminaron_antes(hora: datetime, df_estudiantes: pd.DataFrame) -> bool:
    return df_estudiantes["Fin"] <= hora


def estudiantes_con_menor_productividad(productividad: float, df_estudiantes: pd.DataFrame) -> bool:
    return df_estudiantes["Productividad"] <= productividad


def respuestas_del_estudiante(codigo: str, respuestas_df: pd.DataFrame) -> bool:
    estudiante = respuestas_df[respuestas_df["Código"] == codigo]
    return estudiante[["Código", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]]


def calificaciones_del_estudiante(codigo: str, calificaciones_df: pd.DataFrame) -> bool:
    calificaciones = calificaciones_df[calificaciones_df["Código"] == codigo]
    return calificaciones[["Código", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]]


def function(i: int, columnas: List[str], py_cheat_df: pd.DataFrame, respuestas_df: pd.DataFrame,
             calificaciones_df: pd.DataFrame) -> dict:
    """
    En esta función tratamos de sacar los estudiantes que han podido responder a alguna de las preguntas de manera
    sospechosa. Desde fuera vamos iterando para pasar por cada uno de los estudiantes y aquí los tratamos de manera iterativa.
    Primero buscamos los estudiantes que tengan menor productividad y hayan terminado antes que nuestro estudiante_sub_i.
    Vamos iterando en cada una de sus respuestas y vemos si algún estudiante que cumpla las condiciones de arriba
    ha respondido lo mismo que nuestro estudiante_sub_i.

    Args:
        i: se refiere a ese estudiante sub_i. Necesario para buscarlo por orden de aparición
        columnas: columnas
        py_cheat_df: dataframe con los datos necesarios (productividad)
        respuestas_df: dataframe con los datos de los estudiantes + respuestas
        calificaciones_df: dataframe con los datos de los estudiantes + notas de cada respuesta

    Returns:
        Devuelve los datos del estudiante junto con la lista de las respuestas a tener en cuenta (sospechosas)
    """
    estudiantes_menor_productividad = estudiantes_con_menor_productividad(py_cheat_df["Productividad"][i], py_cheat_df)

    inic = py_cheat_df["Inicio"][i]
    fin = py_cheat_df["Fin"][i]
    time_seconds = py_cheat_df["Segundos"][i]
    grade = py_cheat_df["Nota"][i]
    prod = py_cheat_df["Productividad"][i]

    estudiantes_terminaron_antes = estudiantes_que_terminaron_antes(inic, py_cheat_df)

    df = py_cheat_df[estudiantes_menor_productividad & estudiantes_terminaron_antes]

    respuestas_otros_df = pd.DataFrame(columns=columnas)

    cod_estudiante = py_cheat_df["Código"][i]

    respuestas_estudiante_i_df = respuestas_del_estudiante(cod_estudiante, respuestas_df)
    calificaciones_estudiante_i_df = calificaciones_del_estudiante(cod_estudiante, calificaciones_df)

    for z in range(len(df)):
        df2 = respuestas_del_estudiante(df['Código'].iloc[z], respuestas_df)
        respuestas_otros_df = pd.concat([respuestas_otros_df, df2], ignore_index=True)

    contador_de_respuestas = []

    student = {}
    lista_de_respuestas_a_tener_en_cuenta = []

    for respuesta in range(1, 11):  # respuestas de la 1 a la 10
        answer = {}
        sospechosos_respuesta = []
        flag_not_answer = True
        for estudiante in range(len(respuestas_otros_df)):  # estudiantes desde el primero hasta el último
            if respuestas_otros_df.iloc[estudiante][respuesta] == respuestas_estudiante_i_df.iloc[0][respuesta]:
                if respuestas_otros_df.iloc[estudiante][respuesta] not in contador_de_respuestas:
                    contador_de_respuestas.append(respuestas_estudiante_i_df.iloc[0][respuesta])
                    answer["question_id"] = respuesta
                    answer["text"] = respuestas_estudiante_i_df.iloc[0][respuesta]
                    answer["score"] = calificaciones_estudiante_i_df.iloc[0][respuesta]
                    answer["counter"] = 1
                    sospechosos_respuesta.append(respuestas_otros_df.loc[estudiante]["Código"])
                else:  # hay que tener en cuenta el caso de la respuesta "-" porque se puede dar más de una vez
                    # por lo que no vale solo con mirar en contador_de_respuestas
                    if respuestas_estudiante_i_df.iloc[0][respuesta] == "-":
                        if flag_not_answer:
                            # aquí inicializamos la variable por primera vez porque si no al estar ya en
                            # contador_de_respuestas haría directamente answer["counter"] = answer["counter"] + 1
                            # y daría error porque primero hay que hacer answer["counter"] = 1
                            answer["counter"] = 1
                            flag_not_answer = False
                        else:
                            answer["counter"] = answer["counter"] + 1
                    else:
                        answer["counter"] = answer["counter"] + 1
                        sospechosos_respuesta.append(respuestas_otros_df.loc[estudiante]["Código"])
        if sospechosos_respuesta:  # si sospechosos_respuesta contiene algo
            answer["suspects"] = sospechosos_respuesta
            lista_de_respuestas_a_tener_en_cuenta.append(answer)

    student["student_id"] = cod_estudiante
    student["start"] = inic
    student["end"] = fin
    student["time_seconds"] = time_seconds
    student["grade"] = grade
    student["productividad"] = prod

    student["answers"] = lista_de_respuestas_a_tener_en_cuenta
    return student


def run_pycollaborator(answers_df, marks_df) -> Tuple[Dict[str, List[Dict]], pd.DataFrame]:
    py_cheat_df = marks_df[["Nombre", "Código", "Tiempo", "Inicio", "Fin", "Segundos", "Nota"]]
    py_cheat_df["Productividad"] = (py_cheat_df["Nota"] / (py_cheat_df["Segundos"] / 60))
    # py_cheat_df.to_excel('files/tool_output/06_py_collaborator_outputs/py_cheat_df.xlsx', index=False)

    columnas = ["Código", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]

    py_collaborator = []
    [py_collaborator.append(function(i, columnas, py_cheat_df, answers_df, marks_df)) for i in range(len(py_cheat_df))]

    py_collaborator = {"students": py_collaborator}

    return py_collaborator, py_cheat_df
