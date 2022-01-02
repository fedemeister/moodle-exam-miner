# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import scripts.graph_functions.functions_for_clusters as functions_for_clusters
import web.graph_scatter_plot
import web.graph_fig_estudiantes

app = dash.Dash(__name__)


nube_puntos = web.graph_scatter_plot.nube_puntos()

fig_estudiantes = web.graph_fig_estudiantes.fig_estudiantes()

functions_for_clusters.creacion_padre_hijo()
df_clusters_total = pd.read_excel('files/tool_output/clustering/df_clusters_total.xlsx')
all_clusters = df_clusters_total.Cluster.unique()
@app.callback(
    Output("fig_clusters", "figure"),
    [Input("checklist_clusters", "value")])
def fig_clusters(clusters):
    cluster = df_clusters_total.Cluster.isin(clusters)
    fig_clusters = px.line(df_clusters_total[cluster],
            x="Hora",
            y="Nota",
            markers=True,
            color="Nombre",
            #color="Cluster",
            hover_name='variable',
            hover_data={ "Cluster": True,
                        "Pregunta": True,
                        'Respuesta': True,
                        'Tiempo que tardó en hacer el examen': True,
                        'Productividad al final del examen': ':.2f',
                        #'Nombre':True
                        },
            render_mode ='svg',
            line_shape="spline",
            symbol="Cluster",
        title="Representación gráfica de cómo ha ido la nota del estudiante durante el examen. Para enfocarse en un solo estudiante, dar doble click al estudiante en la leyenda de la derecha."    )
    #fig_clusters.update_layout(hovermode="x unified")
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




def function (x, df_merged):
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
                id_vars=['Nombre', 'Q'+str(x)+'_t', 'Q'+str(x)+'_q', 'Q'+str(x)+'_a'],
                #value_vars=['Q'+str(x)+'_m'],
                value_vars=['Pregunta '+str(x)],
                var_name=['Número'],
                value_name='Nota obtenida para esa pregunta')

    melt = melt.rename(columns={'Q'+str(x)+'_t': 'Hora',
                            'Q'+str(x)+'_q': 'Pregunta',
                            'Q'+str(x)+'_a': 'Respuesta',
                            })

    melt = melt.sort_values(by=['Hora'])
    return melt

df_merged = pd.read_excel("files/tool_output/07_acumulated_knowladge/merge_df.xlsx")
df_line_chart = pd.DataFrame()
for i in range (1,11):
    df_line_chart = df_line_chart.append(function (i, df_merged))

df_line_chart = df_line_chart.reset_index(drop=True)
all_questions = df_line_chart['Número'].unique()

@app.callback(
    Output("fig_questions", "figure"),
    [Input("checklist_questions", "value")])
def fig_questions(questions):
    mask = df_line_chart['Número'].isin(questions)
    fig_questions = px.line(df_line_chart[mask],
            x="Hora",
            y="Nota obtenida para esa pregunta",
            markers=True,
            color="Pregunta",
            hover_name='Respuesta',
            hover_data={"Nombre": True,
                        "Número": True},
            render_mode ='svg',
            #line_shape="spline",
        title="Notas obtenidas en la pregunta durante la duración del examen. Para enfocarse en una sola pregunta, dar doble click a la pregunta deseada.")
    fig_questions.update_yaxes(range = [-0.35,1.10])
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






app.layout = html.Div(children=[
    html.Div([
        html.H1(children='Nube de puntos'),

        html.Div(children='''
            En esta nube de puntos se puede observar el desempeño global del examen, a partir de la nota obtenida y el número de segundos requeridos para hacer el examen.
            El tamaño grande y el color amarillo representan que necesitó mucho tiempo en hacer el examen. El tamaño pequeño y el color morado representan poco tiempo haciendo el examen.
        '''),

        dcc.Graph(id='nube_puntos', figure=nube_puntos)
    ]),
        html.Div([
        html.H1(children='Comportamiento de cada estudiante'),

        html.Div(children='''
            En este gráfico se puede observar el rendimiento de cada estudiante en el examen, cada respuesta que hizo y a la hora que la completó.
            Haciendo click en el lista de estudiantes que aparece a la derecha, el estudiante aparece o desaparece. Doble click para que solo aparezca ese estudiantes.
        '''),

        dcc.Graph(id='fig_estudiantes', figure=fig_estudiantes)
    ]),
        html.Div([
        html.H1(children='Agrupaciones de estudiantes encontrados (Clústers)'),
        html.Div(children='''
            Este gráfico tiene la misma información que el gráfico superior pero con estudiantes divididos en agrupaciones (Clúster).
            Se pueden comparar más de un cluster seleccionando en la lista que está justo debajo de este mensaje.
        '''),
        dcc.Checklist(
            id="checklist_clusters",
            options=[
                {"label": x, "value": x} for x in all_clusters
            ],
            value=all_clusters[:1],
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='fig_clusters')
    ]),
        html.Div([
            html.H1(children='Comportamiento de cada pregunta'),
            html.Div(children='''
                En este gráfico con mayor detalle cada una de las preguntas del examen. Se pueden comparar más de una pregunta seleccionando aquí abajo las preguntas deseadas de la 1 a la 10.
                '''),
            dcc.Checklist(
                id="checklist_questions",
                options=[{"label": x, "value": x}
                        for x in all_questions],
                value=all_questions[:1],
                labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id="fig_questions")
    ])
])











if __name__ == '__main__':
    app.run_server(debug=True)
    app.run_server()