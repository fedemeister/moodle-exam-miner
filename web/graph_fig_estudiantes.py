import pandas as pd
import plotly.express as px

def fig_estudiantes():
    df_final = pd.read_excel('df_final.xlsx')
    fig_estudiantes = px.line(df_final,
                x="Hora",
                y="Nota",
                markers=True,
                color="Nombre",
                hover_name='variable',
                hover_data={"Pregunta": True,
                            'Respuesta': True,
                            'Tiempo que tardó en hacer el examen': True,
                            'Productividad al final del examen': ':.2f'
                            },
                render_mode ='svg',
                #line_shape="spline",
            title="Representación gráfica de cómo ha ido la nota del alumno durante el examen. Doble click en el menú para enfocarse.")

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
