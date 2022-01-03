import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import scripts.graph_functions.functions_for_clusters as functions_for_clusters
import web.graph_scatter_plot
import web.graph_fig_estudiantes
from app import app


nube_puntos = web.graph_scatter_plot.nube_puntos()

fig_estudiantes = web.graph_fig_estudiantes.fig_estudiantes()

#functions_for_clusters.creacion_padre_hijo()
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


df_line_chart = pd.read_excel('df_line_chart.xlsx')
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






layout = html.Div(children=[
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
