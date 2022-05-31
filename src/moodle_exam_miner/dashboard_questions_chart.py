import pandas as pd


def function(x, merge_df, num_preguntas):
    df_merged = merge_df.copy()
    for preg in range(1, num_preguntas + 1):
        df_merged = df_merged.rename(columns={'Q' + str(preg) + '_m': 'Pregunta ' + str(preg)})

    melt = pd.melt(df_merged,
                   id_vars=['Código', 'Q' + str(x) + '_t', 'Q' + str(x) + '_q', 'Q' + str(x) + '_a'],
                   value_vars=['Pregunta ' + str(x)],
                   var_name=['Número'],
                   value_name='Nota obtenida para esa pregunta')

    melt = melt.rename(columns={'Q' + str(x) + '_t': 'Hora',
                                'Q' + str(x) + '_q': 'Pregunta',
                                'Q' + str(x) + '_a': 'Respuesta',
                                })

    melt = melt.sort_values(by=['Hora'])
    return melt


def questions_chart(df_merged, num_preguntas):
    questions_chart_df = pd.DataFrame()
    for i in range(1, num_preguntas + 1):
        questions_chart_df = questions_chart_df.append(function(i, df_merged, num_preguntas))
    questions_chart_df = questions_chart_df.reset_index(drop=True)
    questions_chart_df.to_excel('questions_chart_df.xlsx')
    return questions_chart_df
