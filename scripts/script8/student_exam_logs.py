import pandas as pd
import json
import os

# leemos nuestro maravilloso excel con toda la información
merge_df = pd.read_excel('files/tool_output/07_acumulated_knowladge/merge_df.xlsx')

# leemos el log durante el examen
with open('files/tool_output/01_anonymized_input/exam_logs_utf8_anonymized.json', encoding='utf-8') as json_file:
    log_json = json.load(json_file)

columnas = ['Hora', 'Nombre', 'Nombre_aux', 'Tipo', 'Clase', 'Resumen', 'Descripción', 'Web', 'IP']

json_df = pd.DataFrame(log_json)
json_df.columns = columnas
json_df['Hora'] = pd.to_datetime(json_df['Hora'])  # creamos el dataframe y asignamos la hora en formato datetime

lista_ip = []  # creamos una lista que contendrá las IP, para que si dos alumnos tienen la misma IP nos salte el aviso
for i in range(0, merge_df.shape[0]):
    nombre = merge_df.iloc[i].Nombre
    inicio = merge_df.iloc[i].Inicio
    fin = merge_df.iloc[i].Fin
    nota = merge_df.iloc[i].Nota

    ip = json_df['IP'][json_df['Nombre'] == nombre].iloc[0]

    # cuando un alumno tenga la misma IP que otra persona, esta IP se pondrá al final del nombre del fichero
    if (ip in lista_ip):
        json_particular_df = json_df[(json_df['Hora'] >= inicio)
                                     & (json_df['Hora'] <= fin)
                                     & (json_df['Nombre'] == nombre)
                                     & (json_df['Clase'] == "Cuestionario")
                                     & (json_df['Resumen'] == "Intento de cuestionario visualizado")
                                     ]
        json_particular_df.to_excel(
            'files/tool_output/08_student_exam_logs/individual_logs/' + str(nombre) + '_' + str(nota) + "#" + str(
                json_particular_df.shape[0]) + '_ip_' + str(ip) + '.xlsx', index=False)

    else:  # si no, se añade la IP a la lista y se imprime solamente con nombre_nota#nºrespuestas
        lista_ip.append(json_df['IP'][json_df['Nombre'] == nombre].iloc[0])

        json_particular_df = json_df[(json_df['Hora'] >= inicio)
                                     & (json_df['Hora'] <= fin)
                                     & (json_df['Nombre'] == nombre)
                                     & (json_df['Clase'] == "Cuestionario")
                                     & (json_df['Resumen'] == "Intento de cuestionario visualizado")
                                     ]
        json_particular_df.to_excel(
            'files/tool_output/08_student_exam_logs/individual_logs/' + str(nombre) + '_' + str(nota) + "#" + str(
                json_particular_df.shape[0]) + '.xlsx', index=False)
