import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import json
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


def alumnos_terminarion_antes(hora, py_cheat_df):
    return py_cheat_df["Fin"] <= hora


def personas_menor_productividad(productividad, py_cheat_df):
    return py_cheat_df["Productividad"] <= productividad


def respuestas_del_alumno(codigo, respuestas_df):
    alumno = respuestas_df[respuestas_df["Código"] == codigo]
    return alumno[["Código", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]]


def calificacinoes_del_alumno(codigo, calificaciones_df):
    calificaciones = calificaciones_df[calificaciones_df["Código"] == codigo]
    return calificaciones[["Código", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]]


def function(i, columnas, py_cheat_df, respuestas_df, calificaciones_df, edge_list=False):
    pers_productividad = personas_menor_productividad(py_cheat_df["Productividad"][i], py_cheat_df)
    inic = py_cheat_df["Inicio"][i]
    pers_antes = alumnos_terminarion_antes(inic, py_cheat_df)

    dataf = py_cheat_df[pers_productividad & pers_antes]

    respuestas_otros_df = pd.DataFrame(columns=columnas)

    cod_alumno = py_cheat_df["Código"][i]

    respuestas_alumno_i_df = respuestas_del_alumno(cod_alumno, respuestas_df)
    calificaciones_alumno_i_df = calificacinoes_del_alumno(cod_alumno, calificaciones_df)

    for i in range(len(dataf)):
        df2 = respuestas_del_alumno(dataf['Código'].iloc[i], respuestas_df)
        respuestas_otros_df = respuestas_otros_df.append(df2, ignore_index=True)

    respuestas_contadas = []

    student = {}
    lista_alumnos = []

    for respuesta in range(1, 11):  # respuestas de la 1 a la 10
        answer = {}
        sospechosos_respuesta = []
        flag_not_answer = True
        for alumno in range(len(respuestas_otros_df)):  # alumnos desde el primero hasta el último
            if respuestas_otros_df.iloc[alumno][respuesta] == respuestas_alumno_i_df.iloc[0][respuesta]:
                if respuestas_otros_df.iloc[alumno][respuesta] not in respuestas_contadas:
                    respuestas_contadas.append(respuestas_alumno_i_df.iloc[0][respuesta])
                    answer["question_id"] = respuesta
                    answer["text"] = respuestas_alumno_i_df.iloc[0][respuesta]
                    answer["score"] = calificaciones_alumno_i_df.iloc[0][respuesta]
                    answer["counter"] = 1
                    sospechosos_respuesta.append(respuestas_otros_df.loc[alumno]["Código"])
                else:  # hay que tener en cuenta el caso de la respuesta "-" porque se puede dar más de una vez
                    # por lo que no vale solo con mirar en respuestas_contadas
                    if respuestas_alumno_i_df.iloc[0][respuesta] == "-":
                        if flag_not_answer == True:
                            # aquí inicializamos la variable por primera vez porque si no al estar ya en
                            # respuestas_contadas haría directamente answer["counter"] = answer["counter"] + 1
                            # y daría error porque primero hay que hacer answer["counter"] = 1
                            answer["counter"] = 1
                            flag_not_answer = False
                        else:
                            answer["counter"] = answer["counter"] + 1
                    else:
                        answer["counter"] = answer["counter"] + 1
                        sospechosos_respuesta.append(respuestas_otros_df.loc[alumno]["Código"])
        if sospechosos_respuesta:  # si sospechosos_respuesta contiene algo
            answer["suspects"] = sospechosos_respuesta
            lista_alumnos.append(answer)

    student["student_id"] = cod_alumno
    student["start"] = py_cheat_df["Inicio"][i]
    student["end"] = py_cheat_df["Fin"][i]
    student["time_seconds"] = py_cheat_df["Segundos"][i]
    student["grade"] = py_cheat_df["Nota"][i]
    student["productividad"] = py_cheat_df["Productividad"][i]

    student["answers"] = lista_alumnos
    return student


def run_script06():

    respuestas_df = pd.read_excel("files/tool_output/05_answers_and_questions_cleaned/answers_cleaned.xlsx")
    calificaciones_df = pd.read_excel("files/tool_output/03_anwers_and_califications_dataframe/marks.xlsx")
    # hacer dataframe con "Inicio-Fin-Segundos-Nota"
    py_cheat_df = calificaciones_df[["Nombre", "Código", "Inicio", "Fin", "Segundos", "Nota"]]
    py_cheat_df["Productividad"] = (py_cheat_df["Nota"] / (py_cheat_df["Segundos"] / 60))
    py_cheat_df.to_excel('files/tool_output/06_py_collaborator_outputs/py_cheat_df.xlsx', index=False)

    columnas = ["Código", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]

    salida = []
    for i in range(len(py_cheat_df)):
        salida.append(function(i, columnas, py_cheat_df, respuestas_df, calificaciones_df))

    diccionario = {}
    diccionario["students"] = salida

    with open('files/tool_output/06_py_collaborator_outputs/new_output.json', 'w', encoding='utf8') as outfile:
        json.dump(diccionario, outfile, indent=2, cls=NumpyEncoder, ensure_ascii=False)


#run_script06()
