import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dashboard import app


@app.callback(
    Output("fig_clusters", "figure"),
    [Input("checklist_clusters", "value")])
def fig_clusters(clusters, df_clusters_total):
    cluster = df_clusters_total.Cluster.isin(clusters)
    fig_clusters = px.line(df_clusters_total[cluster],
                           x="Hora",
                           y="Nota",
                           markers=True,
                           color="Código",
                           # color="Cluster",
                           hover_name='variable',
                           hover_data={"Cluster": True,
                                       "Pregunta": True,
                                       'Respuesta': True,
                                       'Tiempo que tardó en hacer el examen': True,
                                       'Productividad al final del examen': ':.2f',
                                       # 'Nombre':True
                                       },
                           render_mode='svg',
                           line_shape="spline",
                           symbol="Cluster",
                           title="Representación gráfica de cómo ha ido la nota del estudiante durante el examen. Para enfocarse en un solo estudiante, dar doble click al estudiante en la leyenda de la derecha.")
    # fig_clusters.update_layout(hovermode="x unified")
    fig_clusters.update_layout(
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
    return fig_clusters


def get_melt_df_merged(x, df_merged):
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
                   # value_vars=['Q'+str(x)+'_m'],
                   value_vars=['Pregunta ' + str(x)],
                   var_name=['Número'],
                   value_name='Nota obtenida para esa pregunta')

    melt = melt.rename(columns={'Q' + str(x) + '_t': 'Hora',
                                'Q' + str(x) + '_q': 'Pregunta',
                                'Q' + str(x) + '_a': 'Respuesta',
                                })

    melt = melt.sort_values(by=['Hora'])
    return melt


@app.callback(
    Output("fig_questions", "figure"),
    [Input("checklist_questions", "value")])
def fig_questions(questions, df_line_chart):
    mask = df_line_chart['Número'].isin(questions)
    fig_questions = px.line(df_line_chart[mask],
                            x="Hora",
                            y="Nota obtenida para esa pregunta",
                            markers=True,
                            color="Pregunta",
                            hover_name='Respuesta',
                            hover_data={"Código": True,
                                        "Número": True},
                            render_mode='svg',
                            # line_shape="spline",
                            title="Notas obtenidas en la pregunta durante la duración del examen. Para enfocarse en una sola pregunta, dar doble click a la pregunta deseada.")
    fig_questions.update_yaxes(range=[-0.35, 1.10])
    fig_questions.update_layout(hovermode="x unified")

    fig_questions.update_layout(
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

    return fig_questions
