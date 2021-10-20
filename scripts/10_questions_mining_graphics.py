import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt

merge_df = pd.read_excel('files/tool_output/07_acumulated_knowladge/merge_df.xlsx')

with open('files/tool_output/09_questions_mining/comportamientoPregunta.json', encoding='utf-8') as json_file:
        log_json = json.load(json_file)
#log_json['questions']
columnas = ['pregunta', 'porcentaje_acertadas', 'calificaciones', 'horas', 'respuestas', 'count_correctas', 'count_incorrectas']

for x in range(0,len(log_json['questions'])):
#for x in range(0,2):
    json_df = pd.DataFrame(log_json['questions'][x])
    if len(json_df)>0: # hay preguntas que no salieron nunca
        json_df.columns = columnas
        json_df.set_index('horas', inplace=True)

        json_df['porcentaje_acertadas'] = 0.0
        json_df['porcentaje_errores'] = 0.0
        json_df['count_correctas'] = 0
        json_df['count_incorrectas'] = 0


        for i in range(0,json_df.shape[0]):
            if i == 0 :
                nota = json_df.calificaciones[i]
                if nota == 1.0:
                    json_df.count_correctas[i] = json_df.count_correctas[i] + 1
                else:
                    json_df.count_incorrectas[i] = json_df.count_incorrectas[i] + 1
                json_df.porcentaje_acertadas[i] = (json_df.count_correctas[i] / (json_df.count_correctas[i] + json_df.count_incorrectas[i]))
                json_df.porcentaje_errores[i] = (json_df.count_incorrectas[i] / (json_df.count_correctas[i] + json_df.count_incorrectas[i]))
            else:
                nota = json_df.calificaciones[i]
                if nota == 1.0:
                    json_df.count_correctas[i] = json_df.count_correctas[i-1] + 1
                    json_df.count_incorrectas[i] = json_df.count_incorrectas[i-1]
                else:
                    json_df.count_incorrectas[i] = json_df.count_incorrectas[i-1] + 1
                    json_df.count_correctas[i] = json_df.count_correctas[i-1]
                json_df.porcentaje_acertadas[i] = (json_df.count_correctas[i] / (json_df.count_correctas[i] + json_df.count_incorrectas[i]))
                json_df.porcentaje_errores[i] = (json_df.count_incorrectas[i] / (json_df.count_correctas[i] + json_df.count_incorrectas[i]))


        titulo = str(json_df.pregunta[0])

        plot = sns.lineplot(data=json_df[['porcentaje_acertadas', 'porcentaje_errores']], markers=True, linewidth=2.0)
        plot.set_title("Comportamiento de :  " + titulo)

        plot.set_xlabel('Fecha del suceso')
        plt.xticks(rotation=60,  ha='right')
        plt.tight_layout()
        plt.savefig('files/tool_output/10_questions_mining_graphics/comportamiento_preguntas/'+titulo+'.png')
        #plt.show()
        plt.close('all')