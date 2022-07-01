import pandas as pd
import plotly.express as px


def fig_estudiantes(merge_df, num_preguntas):
    df_merged = merge_df.copy()
    for i in range(0, len(df_merged)):
        for j in range(2, num_preguntas + 1):
            aux = j - 1
            df_merged['Q' + str(j) + '_m'][i] = df_merged['Q' + str(j) + '_m'][i] + df_merged['Q' + str(aux) + '_m'][i]

    for preg in range(1, num_preguntas + 1):
        df_merged = df_merged.rename(columns={'Q' + str(preg) + '_m': 'Pregunta ' + str(preg)})

    df_final = pd.DataFrame()
    for x in range(1, num_preguntas + 1):
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

    fig_estudiantes = px.line(df_final,
                              x="Hora",
                              y="Nota",
                              markers=True,
                              color="Código",
                              hover_name='variable',
                              hover_data=["Pregunta", 'Respuesta', 'Segundos que tardó en hacer el examen',
                                          'Productividad al final del examen'],
                              render_mode='svg',
                              title="Representación gráfica del desempeño del estudiante durante el examen. Doble click en el menú para enfocarse.")

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
