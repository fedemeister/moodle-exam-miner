from typing import Dict


def question_mining(i, merge_df, preguntas_df) -> Dict:
    """
    Función que crea una entrada con los datos de la pregunta en curso que se encuentran en merge_df
    Args:
        i: iteración (comportamiento_preguntas.append(question_mining(i, merge_df, df_xml_cleaned))
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.
        preguntas_df: Pandas dataframe con las preguntas y respuestas del examen después de la limpieza

    Returns:
        Datos para la pregunta_sub_i
    """
    iteracion = {}
    preg = preguntas_df['Question'].iloc[i]
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

            iteracion['pregunta'] = preg
            iteracion['porcentaje_acertadas'] = (len_c / len_p)
            iteracion['calificaciones'] = lista
            iteracion['horas'] = lista_horas
            iteracion['respuestas'] = lista_resp
            iteracion['count_correctas'] = len_c
            iteracion['count_incorrectas'] = len_i

    return iteracion


def run_script09(df_xml_cleaned, merge_df) -> Dict:
    """
    Función que genera un archivo con el comportamiento de cada pregunta
    Args:
        df_xml_cleaned: Pandas dataframe con las preguntas y respuestas del examen después de la limpieza
        merge_df: Dataframe con todos los datos que vamos a consultar para acceder únicamente a un dataframe.

    Returns:
        comportamiento_preguntas
    """
    comportamiento_preguntas = []
    for i in range(0, len(df_xml_cleaned), 4):
        comportamiento_preguntas.append(question_mining(i, merge_df, df_xml_cleaned))

    comportamiento_preguntas = {"questions": comportamiento_preguntas}

    return comportamiento_preguntas
