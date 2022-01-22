import pandas as pd
import json
import numpy as np
from datetime import datetime
from scripts.script6.py_collaborator_outputs import NumpyEncoder


def funcion(i, merge_df, preguntas_df):
    questions = {}
    preg = preguntas_df['Question'].iloc[i]
    lista = []
    for x in range(1, 11):
        len_p = len(merge_df['Q' + str(x) + '_q'][merge_df['Q' + str(x) + '_q'] == preg])
        if len_p > 1:
            lista_c = merge_df['Q' + str(x) + '_a'][
                (merge_df['Q' + str(x) + '_q'] == preg) & (merge_df['Q' + str(x) + '_m'] == 1.0)].tolist()
            lista_i = merge_df['Q' + str(x) + '_a'][
                (merge_df['Q' + str(x) + '_q'] == preg) & (merge_df['Q' + str(x) + '_m'] == -0.25)].tolist()
            lista = merge_df['Q' + str(x) + '_m'][(merge_df['Q' + str(x) + '_q'] == preg)].tolist()
            lista_horas = merge_df['Q' + str(x) + '_t'][(merge_df['Q' + str(x) + '_q'] == preg)].tolist()
            lista_resp = merge_df['Q' + str(x) + '_a'][(merge_df['Q' + str(x) + '_q'] == preg)].tolist()

            len_c = len(lista_c)
            len_i = len(lista_i)

            questions['pregunta'] = preg
            questions['porcentaje_acertadas'] = (len_c / len_p)
            questions['calificaciones'] = lista
            questions['horas'] = lista_horas
            questions['respuestas'] = lista_resp
            questions['count_correctas'] = len_c
            questions['count_incorrectas'] = len_i

    return questions


def run_script09():
    preguntas_df = pd.read_excel('files/tool_output/05_answers_and_questions_cleaned/all_questions.xlsx')
    merge_df = pd.read_excel('files/tool_output/07_acumulated_knowladge/merge_df.xlsx')

    salida_preg = []
    for i in range(0, len(preguntas_df), 4):
        salida_preg.append(funcion(i, merge_df, preguntas_df))

    diccionario = {"questions": salida_preg}

    with open('files/tool_output/09_questions_mining/comportamientoPregunta.json', 'w', encoding='utf8') as outfile:
        json.dump(diccionario, outfile, indent=2, cls=NumpyEncoder, ensure_ascii=False)
