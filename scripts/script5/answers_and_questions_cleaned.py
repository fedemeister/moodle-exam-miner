from typing import Tuple
import pandas as pd


def clean_df_xml(df_xml_output: pd.DataFrame) -> pd.DataFrame:
    df_xml_output['Answer'] = df_xml_output['Answer'].str.strip()
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['<p> '], '', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['<p>'], '', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['</p>'], '', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].str.strip()
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['\\n'], ' ', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['\\t\t'], ' ', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['\n'], ' ', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['  '], ' ', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['&lt;&gt;'], '<>', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['&lt;='], '<=', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['=&gt;'], '=>', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['&lt;'], '<', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['&gt;'], '>', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['=&gt;'], '=>', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['<br />'], u'\n', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['\n'], u'', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['  '], ' ', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u' IN\('], u' IN( ', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].str.strip()
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'\xa0'], '', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].str.strip()
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['l.idGROUP'], 'l.id GROUP', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace(['l.idGROUP'], 'l.id GROUP', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'A1.nacionalidadHAVING COUNT'],
                                                              u'A1.nacionalidad HAVING COUNT', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'AND A1.nacionalidad'],
                                                              u' AND A1.nacionalidad', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'NOT IN\( SELECT socio_id'],
                                                              u'NOT IN (SELECT socio_id', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'WHERE socio_id IN\( SELECT'],
                                                              u'WHERE socio_id IN (SELECT', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'socio_id =\(SELECT'], u'socio_id = (SELECT',
                                                              regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'libros L\)GROUP BY'], u'libros L) GROUP BY',
                                                              regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'A.apellido1HAVING'], u'A.apellido1 HAVING',
                                                              regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'WHERE id <>\(SELECT socio_id'],
                                                              u'WHERE id <> (SELECT socio_id', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'WHERE id <>\(SELECT socio_id'],
                                                              u'WHERE id <> (SELECT socio_id', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u's.idLEFT OUTER JOIN'],
                                                              u's.id LEFT OUTER JOIN', regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u's.apellido1HAVING'], u's.apellido1 HAVING',
                                                              regex=True)
    df_xml_output['Answer'] = df_xml_output['Answer'].replace([u'SELECTnacionalidad'], u'SELECT nacionalidad',
                                                              regex=True)
    return df_xml_output


def limpiar_respuestas_df(df: pd.DataFrame, Q: int):
    df['Q' + str(Q)] = df['Q' + str(Q)].str.strip()
    df['Q' + str(Q)] = df['Q' + str(Q)].replace(['\\n'], ' ', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].replace(['\\t\t'], ' ', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].replace(['\n'], ' ', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].replace(['  '], ' ', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].str.strip()
    df['Q' + str(Q)] = df['Q' + str(Q)].replace([u'\xa0'], '', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].str.strip()
    df['Q' + str(Q)] = df['Q' + str(Q)].replace([u'SELECTnacionalidad'], u'SELECT nacionalidad', regex=True)


def run_script05(answers_df: pd.DataFrame, df_xml_output: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    En esta función vamos a hacer que las respuestas que vienen del conjunto XML y las que vienen a través del
    conjunto answers_df (que previamente viene del json answers) contengan los mismos elementos.

    Esto nos servirá para sacar posteriormente qué preguntas les tocó a los alumnos y poder hacer agregaciones.

    Args:
        answers_df: Dataframe con las respuestas de cada alumno (nombre, email, respuestas, tiempo, etc)
        df_xml_output: Dataframe sacado del script02 que contiene las preguntas y las respuestas del conjunto
            contenido en el XML que sube el profesor a la plataforma.

    Returns:
        df_xml_cleaned, df_check, answers_df_cleaned.
    """

    [limpiar_respuestas_df(answers_df, i) for i in range(1, 11)]  # limpia cada columna modificando answers_df

    # utilizamos el dataframe con las preguntas ya limpias de caracteres extraños
    answers_df_cleaned = answers_df

    respuestas = []
    for i in range(1, 11):
        lista = list(answers_df_cleaned["Q" + str(i)])
        respuestas.append(lista)

    df_xml_cleaned = clean_df_xml(df_xml_output)

    # creamos una lista con las respuestas que respondieron los estudiantes durante el examen.
    flat_list = [item for sublist in respuestas for item in sublist]
    flat_list = list(dict.fromkeys(flat_list))  # eliminamos duplicados
    answer_Series = pd.DataFrame(flat_list, columns=['Answer'])  # lo pasamos a Series

    # cuando una respuesta no está en el conjunto global de respuestas nos quedamos con ella
    # df_check guarda las respuestas que están o no están en el fichero xml ya limpio: 1 sí está, 0 no está
    df_check = answer_Series.Answer.isin(df_xml_output.Answer).astype(int)
    # print(df_check[df_check == 0].shape[0]) #aquí mostramos cuánta cantidad hay.

    return df_xml_cleaned, df_check, answers_df_cleaned
