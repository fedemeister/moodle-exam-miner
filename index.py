from flask import Flask, render_template, redirect, request
import time
from io import BytesIO
import zipfile
import os
from flask import send_file
import plotly.express as px
from dash import dcc, html, Input, Output

app = Flask(__name__, template_folder='web/mem_flask/templates')

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


@app.route('/zipped_data')
def zipped_data():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = "tool_output_{}.zip".format(timestr)
    memory_file = BytesIO()
    file_path = 'files/tool_output'
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(file_path):
            for file in files:
                zipf.write(os.path.join(root, file))
    memory_file.seek(0)
    return send_file(memory_file,
                     attachment_filename=fileName,
                     as_attachment=True)


from scripts.script0.input_coding_to_utf8 import jsons_to_utf8
from scripts.script1.anonymize_input import anonymizer
from scripts.script2.questions import run_script02
from scripts.script3.answers_and_califications_dataframe import create_marks_and_answers_df
from scripts.script4.answer_times import get_answer_times_df
import scripts.script5.answers_and_questions_cleaned as script5
import scripts.script6.py_collaborator_outputs as script6
import scripts.script7.acumulated_knowladge as script7
from scripts.script8.student_exam_logs import get_student_exam_logs
from scripts.script_dashboard import scatter_plot
from scripts.script_dashboard import students_chart
from scripts.script_dashboard import students_clusters
from scripts.script_dashboard import questions_chart


@app.route('/scripts_run')
def scripts_run():
    tic = time.perf_counter()
    # SCRIPT 0
    json_marks_utf8, json_logs_utf8, json_answers_utf8 = jsons_to_utf8()

    # SCRIPT 1
    json_logs_anon, json_exam_answers_anon, json_exam_marks_anon, promedio_general, name_user_dictionary = anonymizer(
        json_marks_utf8,
        json_logs_utf8,
        json_answers_utf8)

    # SCRIPT 2
    df_xml_output = run_script02()

    # SCRIPT 3
    marks_df, answers_df = create_marks_and_answers_df(json_exam_marks_anon, json_exam_answers_anon)
    # marks_df, answers_df = create_marks_and_answers_df(json_marks_utf8, json_answers_utf8)

    # SCRIPT 4
    answer_times_merged_df = get_answer_times_df(marks_df, json_logs_anon)
    # answer_times_merged_df = get_answer_times_df(marks_df, json_logs_utf8)

    # SCRIPT 5
    df_xml_cleaned, df_check, answers_df_cleaned = script5.run_script05(answers_df, df_xml_output)

    # SCRIPT 6
    py_collaborator, py_cheat_df = script6.run_pycollaborator(answers_df_cleaned, marks_df)

    # SCRIPT 7
    merge_df, ratio_preguntas, conocimiento_acumulado, merge_df_json = script7.run_script07(answers_df_cleaned,
                                                                                            df_xml_cleaned,
                                                                                            answer_times_merged_df,
                                                                                            py_cheat_df)

    # SCRIPT 8
    student_exam_logs, student_exam_logs_name = get_student_exam_logs(merge_df, json_logs_anon)

    # DASHBOARD
    nube_puntos = scatter_plot.nube_puntos(py_cheat_df)
    fig_estudiantes = students_chart.fig_estudiantes(merge_df)

    df_clusters_total = students_clusters.funcion_clusters(py_cheat_df, merge_df)

    questions_chart_df = questions_chart.questions_chart(merge_df)
    all_questions = questions_chart_df['Número'].unique()
    all_clusters = df_clusters_total.Cluster.unique()
    from web.dash_app import create_dash_application

    dash_app = create_dash_application(app)

    @dash_app.callback(
        Output("fig_clusters", "figure"),
        [Input("checklist_clusters", "value")])
    def fig_clusters(clusters):
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
                               symbol="Cluster")
        # title="Representación gráfica de cómo ha ido la nota del estudiante durante el examen. Para enfocarse en un solo estudiante, dar doble click al estudiante en la leyenda de la derecha.")
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

    @dash_app.callback(
        Output("fig_questions", "figure"),
        [Input("checklist_questions", "value")])
    def fig_questions(questions):
        mask = questions_chart_df['Número'].isin(questions)
        fig_questions = px.line(questions_chart_df[mask],
                                x="Hora",
                                y="Nota obtenida para esa pregunta",
                                markers=True,
                                color="Pregunta",
                                hover_name='Respuesta',
                                hover_data={"Código": True,
                                            "Número": True},
                                render_mode='svg',
                                title="Notas obtenidas en la pregunta durante la duración del examen. Para enfocarse en "
                                      "una sola pregunta, dar doble click a la pregunta deseada.")
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

    dash_app.layout = html.Div(children=[
        html.H1(children='Su informe del examen está listo', style={'textAlign': 'center'}),
        html.Div([
            html.H1(children='Nube de puntos'),
            html.Div(children='''En esta nube de puntos se puede observar el desempeño global del examen, a partir de la 
        nota obtenida y el número de segundos requeridos para hacer el examen. El tamaño grande y el color amarillo 
        representan que necesitó mucho tiempo en hacer el examen. El tamaño pequeño y el color morado representan 
        poco tiempo haciendo el examen.''', style={'padding': 10}),

            dcc.Graph(id='nube_puntos', figure=nube_puntos)
        ]),
        html.Div([
            html.H1(children='Comportamiento de los estudiantes'),
            html.Div(children='''En este gráfico se puede observar el rendimiento de cada estudiante en el examen, 
        cada respuesta que hizo y a la hora que la completó. Haciendo click en el lista de estudiantes que aparece a 
        la derecha, el estudiante aparece o desaparece. Doble click para que solo aparezca ese estudiantes.''',
                     style={'padding': 10}),

            dcc.Graph(id='fig_estudiantes', figure=fig_estudiantes)
        ]),
        html.Div([
            html.H1(children='Agrupaciones de estudiantes encontrados (Clústers)'),
            html.Div(children='''Este gráfico tiene la misma información que el gráfico superior pero con estudiantes 
        divididos en agrupaciones (Clúster). Se pueden comparar más de un cluster seleccionando en la lista que 
        está justo debajo de este mensaje.''', style={'padding': 10}),
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
            html.Div(children='''En este gráfico con mayor detalle cada una de las preguntas del examen. Se pueden 
        comparar más de una pregunta seleccionando aquí abajo las preguntas deseadas de la 1 a la 10.''',
                     style={'padding': 10}),
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
    toc = time.perf_counter()

    print(f"run_scripts {toc - tic:0.4f} seconds")

    return redirect('dash')


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('base.html', title='Home Page')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/features')
def features():
    return render_template('features.html', title='Features')


@app.route('/faqs')
def faqs():
    return render_template('faqs.html', title='FAQs')


app.config["UPLOAD_FOLDER"] = "files/tool_input"
app.config["ALLOWED_FILES_EXTENSIONS"] = ["JSON", "XML"]


def allowed_extensions(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_FILES_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/scripts', methods=['POST', 'GET'])
def scripts():
    if request.method == "POST":

        files = request.files.getlist("formFileMultiple")
        if len(files) == 0:
            print("Select a file")
            return redirect(request.url)

        for file in files:
            if allowed_extensions(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            else:
                print("Only upload json or XML files")
                return redirect(request.url)

        print("Ficheros subidos")
        return redirect('scripts_run')


if __name__ == '__main__':
    app.run()
