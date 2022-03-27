import pandas as pd
import plotly.express as px


def fig_estudiantes(merge_df):
    df_merged = merge_df.copy()
    for i in range(0, len(df_merged)):
        for j in range(2, 11):
            aux = j - 1
            df_merged['Q' + str(j) + '_m'][i] = df_merged['Q' + str(j) + '_m'][i] + df_merged['Q' + str(aux) + '_m'][i]

    df_merged = df_merged.rename(columns={'Q1_m': 'Pregunta 1',
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

    df_final = pd.DataFrame()
    for x in range(1, 11):
        melt = pd.melt(df_merged,
                       id_vars=['Código', 'Segundos', 'Productividad', 'Q' + str(x) + '_t', 'Q' + str(x) + '_q',
                                'Q' + str(x) + '_a'],
                       value_vars=['Pregunta ' + str(x)],
                       value_name='Nota')

        melt = melt.rename(columns={'Q' + str(x) + '_t': 'Hora',
                                    'Q' + str(x) + '_q': 'Pregunta',
                                    'Q' + str(x) + '_a': 'Respuesta',
                                    'Segundos': 'Segundos que tardó en hacer el examen',
                                    'Productividad': 'Productividad al final del examen'
                                    })

        df_final = df_final.append(melt)
    title_fig_estudiantes = "Representación gráfica de cómo ha ido la nota del alumno durante el examen. " \
                            "Para enfocarse en un solo alumno, dar doble click al alumno en la leyenda de la derecha."
    fig_estudiantes = px.line(df_final,
                              x="Hora",
                              y="Nota",
                              markers=True,
                              color="Código",
                              hover_name='variable',
                              hover_data=["Pregunta", 'Respuesta', 'Segundos que tardó en hacer el examen',
                                          'Productividad al final del examen'],
                              render_mode='svg',
                              # line_shape="spline",
                              title=title_fig_estudiantes)

    fig_estudiantes.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=30,
                         label="Seleccionar intervalo de 30 minutos",
                         step="minute",
                         stepmode="todate"),
                    dict(count=1,
                         label="Seleccionar intervalo de 1 hora",
                         step="hour",
                         stepmode="backward"),
                    dict(step="all",
                         label="Todo el intervalo")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    return fig_estudiantes
