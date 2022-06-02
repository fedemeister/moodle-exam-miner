from flask import Flask, render_template, redirect, request
import time
from io import BytesIO, open
import zipfile
import os
from flask import send_file
import plotly.express as px
from dash import dcc, html, Input, Output
import json
import warnings

app = Flask(__name__, template_folder='web/mem_flask/templates', static_folder='web/mem_flask/static')

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


from src.moodle_exam_miner.script0_jsons_to_utf8 import jsons_to_utf8
from src.moodle_exam_miner.script1_anonymize_input import anonymizer
from src.moodle_exam_miner.script2_questions import run_script02
from src.moodle_exam_miner.script3_answers_and_califications_dataframe import create_marks_and_answers_df
from src.moodle_exam_miner.script4_answer_times import get_answer_times_df
import src.moodle_exam_miner.script5_answers_and_questions_cleaned as script5
import src.moodle_exam_miner.script6_py_collaborator_outputs as script6
import src.moodle_exam_miner.script7_acumulated_knowladge as script7
from src.moodle_exam_miner import dashboard_scatter_plot
from src.moodle_exam_miner import dashboard_students_chart
from src.moodle_exam_miner import dashboard_students_clusters
from src.moodle_exam_miner import dashboard_questions_chart


@app.route('/scripts_run')
def scripts_run():
    tic = time.perf_counter()
    with open('files/tool_input/config.json', 'r') as f:
        config = json.load(f)

    config_num_stud_cluster = int(config['config_num_stud_cluster'])
    config_dif_minutos_cl = int(config['config_dif_minutos_cl'])

    # SCRIPT 0
    json_marks_utf8, json_logs_utf8, json_answers_utf8 = jsons_to_utf8()

    # SCRIPT 1
    json_logs_anon, json_exam_answers_anon, json_exam_marks_anon, promedio_general, name_user_dictionary = anonymizer(
        json_marks_utf8,
        json_logs_utf8,
        json_answers_utf8)

    num_preguntas = int(len(json_marks_utf8[0][0][9:]))
    # SCRIPT 2
    df_xml_output = run_script02()

    # SCRIPT 3
    marks_df, answers_df = create_marks_and_answers_df(json_exam_marks_anon, json_exam_answers_anon, num_preguntas)

    # SCRIPT 4
    answer_times_merged_df = get_answer_times_df(marks_df, json_logs_anon, num_preguntas)

    # SCRIPT 5
    df_xml_cleaned, df_check, answers_df_cleaned = script5.run_script05(answers_df, df_xml_output, num_preguntas)

    # SCRIPT 6
    py_collaborator, py_cheat_df = script6.run_pycollaborator(answers_df_cleaned, marks_df, num_preguntas)
    # SCRIPT 7
    merge_df, ratio_preguntas, conocimiento_acumulado, merge_df_json = script7.run_script07(answers_df_cleaned,
                                                                                            df_xml_cleaned,
                                                                                            answer_times_merged_df,
                                                                                            py_cheat_df,
                                                                                            marks_df,
                                                                                            num_preguntas)
    # DASHBOARD
    nube_puntos = dashboard_scatter_plot.nube_puntos(py_cheat_df)
    fig_estudiantes = dashboard_students_chart.fig_estudiantes(merge_df, num_preguntas)

    df_clusters_total = dashboard_students_clusters.funcion_clusters(py_cheat_df,
                                                                     merge_df,
                                                                     config_num_stud_cluster,
                                                                     config_dif_minutos_cl,
                                                                     num_preguntas)

    questions_chart_df = dashboard_questions_chart.questions_chart(merge_df, num_preguntas)
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
                               symbol="Cluster",
                               title="Posibles clusters de estudiante durante el examen. Doble click en el menú para "
                                     "enfocarse.")
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
                                title="Notas obtenidas en la pregunta durante la duración del examen. Doble click en "
                                      "el menú para enfocarse.")
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
        comparar más de una pregunta seleccionando aquí abajo las preguntas deseadas.''',
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
    return render_template('base.html', title='Inicio')


@app.route('/upload')
def upload():
    return render_template('upload.html', title='Subir archivos')


@app.route('/features')
def features():
    return render_template('features.html', title='Características')


@app.route('/faqs')
def faqs():
    return render_template('faqs.html', title='Preguntas frecuentes (FAQs)')


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
        config_num_stud_cluster = request.form['flexRadioDefault']
        config_dif_minutos_cl = request.form['radioFormMinutos']

        dictionary = {
            "config_num_stud_cluster": config_num_stud_cluster,
            "config_dif_minutos_cl": config_dif_minutos_cl
        }

        with open("files/tool_input/config.json", "w") as outfile:
            json.dump(dictionary, outfile)

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
