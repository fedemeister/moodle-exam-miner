import pandas as pd


# Esta función imprime la localización de la fila y su contenido
# me sirve para buscar rápidamente cuál es y poder ver el contenido
# y arreglar por qué no es igual que en el otro conjunto
def imprimir_dataframe(dataframe, column):
    for i in range(0, len(dataframe)):
        print(str(i), dataframe[str(column)].iloc[i])


def limpiar_respuestas_df(df, Q):
    df['Q' + str(Q)] = df['Q' + str(Q)].str.strip()
    df['Q' + str(Q)] = df['Q' + str(Q)].replace(['\\n'], ' ', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].replace(['\\t\t'], ' ', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].replace(['\n'], ' ', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].replace(['  '], ' ', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].str.strip()
    df['Q' + str(Q)] = df['Q' + str(Q)].replace([u'\xa0'], '', regex=True)
    df['Q' + str(Q)] = df['Q' + str(Q)].str.strip()
    df['Q' + str(Q)] = df['Q' + str(Q)].replace([u'SELECTnacionalidad'], u'SELECT nacionalidad', regex=True)

    df.to_excel('files/tool_output/05_answers_and_questions_cleaned/answers_cleaned.xlsx', index=False)


def execution():
    respuestas_df = pd.read_excel('files/tool_output/03_anwers_and_califications_dataframe/answers.xlsx')
    df_todas_preguntas = pd.read_excel('files/tool_output/02_questions_and_answers_set/raw_quest_answ_output.xlsx')
    # Nos quedamos con un conjunto único de respuestas, es decir, quiero que salgan todas pero ninguna repetida.
    for i in range(1, 11):
        limpiar_respuestas_df(respuestas_df, i)

    respuestas_df = pd.read_excel('files/tool_output/05_answers_and_questions_cleaned/answers_cleaned.xlsx')

    respuestas = []
    for i in range(1, 11):
        lista = list(respuestas_df["Q" + str(i)])
        respuestas.append(lista)

    flat_list = [item for sublist in respuestas for item in sublist]
    flat_list = list(dict.fromkeys(flat_list))  # eliminamos duplicados
    # len(flat_list)
    df_respuestas = pd.DataFrame(flat_list, columns=['Answer'])

    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].str.strip()
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['<p> '], '', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['<p>'], '', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['</p>'], '', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].str.strip()
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['\\n'], ' ', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['\\t\t'], ' ', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['\n'], ' ', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['  '], ' ', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['&lt;&gt;'], '<>', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['&lt;='], '<=', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['=&gt;'], '=>', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['&lt;'], '<', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['&gt;'], '>', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['=&gt;'], '=>', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['<br />'], u'\n', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['\n'], u'', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['  '], ' ', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u' IN\('], u' IN( ', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].str.strip()
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'\xa0'], '', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].str.strip()
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['l.idGROUP'], 'l.id GROUP', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace(['l.idGROUP'], 'l.id GROUP', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'A1.nacionalidadHAVING COUNT'],
                                                                        u'A1.nacionalidad HAVING COUNT', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'AND A1.nacionalidad'],
                                                                        u' AND A1.nacionalidad', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'NOT IN\( SELECT socio_id'],
                                                                        u'NOT IN (SELECT socio_id', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'WHERE socio_id IN\( SELECT'],
                                                                        u'WHERE socio_id IN (SELECT', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'socio_id =\(SELECT'], u'socio_id = (SELECT',
                                                                        regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'libros L\)GROUP BY'], u'libros L) GROUP BY',
                                                                        regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'A.apellido1HAVING'], u'A.apellido1 HAVING',
                                                                        regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'WHERE id <>\(SELECT socio_id'],
                                                                        u'WHERE id <> (SELECT socio_id', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'WHERE id <>\(SELECT socio_id'],
                                                                        u'WHERE id <> (SELECT socio_id', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u's.idLEFT OUTER JOIN'],
                                                                        u's.id LEFT OUTER JOIN', regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u's.apellido1HAVING'], u's.apellido1 HAVING',
                                                                        regex=True)
    df_todas_preguntas['Answer'] = df_todas_preguntas['Answer'].replace([u'SELECTnacionalidad'], u'SELECT nacionalidad',
                                                                        regex=True)

    # cuando una respuesta no está en el conjunto global de respuestas nos quedamos con ella
    df_check = df_respuestas.Answer.isin(df_todas_preguntas.Answer).astype(int)
    # print(df_check[df_check == 0].shape[0]) #aquí mostramos cuánta cantidad hay.
    # En nuestro ejemplo hay 1 que no cuadra, la respuesta en blanco: "-"
    df_todas_preguntas.to_excel('files/tool_output/05_answers_and_questions_cleaned/all_questions.xlsx', index=False)
    df_respuestas.to_excel('files/tool_output/05_answers_and_questions_cleaned/df_respuestas.xlsx', index=False)


execution()
