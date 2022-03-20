import pandas as pd


def function(x, merge_df):
    df_merged = merge_df.copy()
    df_merged = df_merged.rename(columns={
        'Q1_m': 'Pregunta 1',
        'Q2_m': 'Pregunta 2',
        'Q3_m': 'Pregunta 3',
        'Q4_m': 'Pregunta 4',
        'Q5_m': 'Pregunta 5',
        'Q6_m': 'Pregunta 6',
        'Q7_m': 'Pregunta 7',
        'Q8_m': 'Pregunta 8',
        'Q9_m': 'Pregunta 9',
        'Q10_m': 'Pregunta 10',
    })

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


def questions_chart(df_merged):
    questions_chart_df = pd.DataFrame()
    for i in range(1, 11):
        questions_chart_df = questions_chart_df.append(function(i, df_merged))
    questions_chart_df = questions_chart_df.reset_index(drop=True)
    questions_chart_df.to_excel('questions_chart_df.xlsx')
    return questions_chart_df
