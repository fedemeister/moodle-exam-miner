import plotly.express as px


def nube_puntos(df_nube_puntos):
    df_nube_puntos = df_nube_puntos.rename(columns={'Inicio': 'Hora de inicio del examen'})
    nube_puntos = px.scatter(df_nube_puntos,
                             x="Hora de inicio del examen",
                             y="Nota",
                             color="Segundos",
                             hover_name="Código",
                             hover_data=["Tiempo"],
                             size="Segundos",
                             trendline="lowess",
                             title="Nube de puntos para los exámenes. El tamaño del círculo son los segundos empleados en el examen.")

    nube_puntos.update_layout(
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
    return nube_puntos
