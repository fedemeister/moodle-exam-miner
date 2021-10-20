import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
from datetime import datetime, timedelta
import csv

def convert(o): # hay que convertir los np.int64 a enteros porque np.int64 is not JSON serializable
    if isinstance(o, np.int64): return int(o)
    raise TypeError

def cambiar_formato_fecha(fecha:str):
    '''
    Devuelve un string en formato "dia mes año" para poder ser procesado por
    datetime.strptime con el siguiente formato datetime.strptime(fecha,"%d %m %Y %H:%M")

    Parameters:
        fecha (str):Cadena parecida con el siguiente formato "22 de mayo de 2020  11:23"
    Returns:
        fecha(str):Cadena de entrada donde han sido eliminado lo innecesario para ser procesado correctamente
        Ejemplo de salida --> 22 05 2020 11:23
    '''
    #print(fecha)
    fecha = fecha.replace("de", "")
    fecha = fecha.replace("enero", "01")
    fecha = fecha.replace("febrero", "02")
    fecha = fecha.replace("marzo", "03")
    fecha = fecha.replace("abril", "04")
    fecha = fecha.replace("mayo", "05")
    fecha = fecha.replace("junio", "06")
    fecha = fecha.replace("julio", "07")
    fecha = fecha.replace("agosto", "08")
    fecha = fecha.replace("septiembre", "09")
    fecha = fecha.replace("octubre", "10")
    fecha = fecha.replace("noviembre", "11")
    fecha = fecha.replace("diciembre", "12")

    fecha = fecha.replace("  ", " ")

    #print(fecha)

    return fecha

def duracion_a_segundos(fecha:str):
    '''
    Devuelve un entero con la cantidad de segundos que han pasado entre el inicio y el fin del examen.

    Parameters:
        fecha (str):Cadena parecida con alguno de los siguientes formatos:
            1 - "10 minutos y 59 segundos"
            2 - "10 minutos"
            3 - "59 segundos"
    Returns:
        segundos(int):Duración en segundos de la cadena recibida correspondiente a la duración del examen
    '''
    if 'minutos' in fecha and 'segundos' in fecha: # Por ejemplo: "23 minutos 46 segundos"
        fecha = fecha.replace('minutos ', '')
        fecha = fecha.replace(' segundos', '')
        split_list = fecha.split() #split string into a list
        segundos = int(split_list[0])*60 + int(split_list[1])
    elif 'segundos' in fecha: # Por ejemplo: "46 segundos"
        segundos = fecha.replace(' segundos', '')
    else: # Por ejemplo: "23 minutos"
        fecha = fecha.replace(' minutos', '')
        segundos = int(fecha)*60
    return int(segundos)


def formateo_json(my_json:list, devolver:bool=False):
    '''
    Formatea el JSON para dejarlo con las columnas de las notas en formato float, 
    la columna de duración del examen como un número entero y las columnas de Inicio y Fin como datetime:    

    Parameters:
        my_json (list): JSON sin procesar
    Returns:
        NO DEVUELVE NADA, MODIFICA EL JSON RECIBIDO
    '''
    for alumno in my_json:
        if alumno[0] != 'Promedio general':
            for i in range(5,7):
                fecha = cambiar_formato_fecha(alumno[i])
                alumno[i] = datetime.strptime(fecha,"%d %m %Y %H:%M") #%d=22 %m=05 %Y=2020 %H=11:%M=23

            alumno[7] = duracion_a_segundos(alumno[7])
            if "SELECT" in alumno[9] or "FROM" in alumno[9] or "WHERE" in alumno[9] or "LIKE" in alumno[9]:   #estamos en respuestas_json
                if (alumno[8] == '-'):
                    alumno[8] = alumno[8].replace("-", "0.00")
                    alumno[8] = float(alumno[8])
                else:
                    alumno[8] = alumno[8].replace(",", ".")
                    alumno[8] = float(alumno[8])
            else:
                for i in range(8,19):
                    if (alumno[i] == '-'):
                        alumno[i] = alumno[i].replace("-", "0.00")
                        alumno[i] = float(alumno[i])
                    else:
                        alumno[i] = alumno[i].replace(",", ".")
                        alumno[i] = float(alumno[i])
        else:
            for i in range(8,19):
                alumno[i] = alumno[i].replace(",", ".")
    if devolver == True:
        return my_json



def guardar_json_formateado_csv(data:list):
    for i in range(len(data)):
        with open('calificaciones1.csv', 'a', encoding='utf-8-sig') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(data[i])

def execution():
    columnas = ['Apellidos', 'Nombre', 'Código', 'Email', 'Estado', 'Inicio', 'Fin', 'Segundos', 'Nota',
            'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']

    with open('files/tool_output/01_anonymized_input/exam_answers_utf8_anonymized.json', encoding='utf-8') as json_file:
        respuestas_json = json.load(json_file)

    with open('files/tool_output/01_anonymized_input/exam_califications_utf8_anonymized.json', encoding='utf-8') as json_file:
        calificaciones_json = json.load(json_file)


    calificaciones_json = formateo_json(calificaciones_json, devolver = True)
    respuestas_json = formateo_json(respuestas_json, devolver = True)

    np_array_promedio = np.array(calificaciones_json[len(calificaciones_json)-1][8:19])
    np_array_promedio = np_array_promedio.astype(np.float64)

    calificaciones_df = pd.DataFrame(calificaciones_json)
    calificaciones_df.columns = columnas
    calificaciones_df.drop(calificaciones_df[calificaciones_df['Apellidos'] == "Promedio general"].index, inplace = True)
    calificaciones_df.drop(calificaciones_df[calificaciones_df['Código'] == "0002760"].index, inplace = True) 
    calificaciones_df.sort_values(by=['Inicio', 'Fin'], inplace=True, ascending=True, ignore_index=True)
    calificaciones_df.to_excel('files/tool_output/03_anwers_and_califications_dataframe/marks.xlsx', index = False)

    respuestas_df = pd.DataFrame(respuestas_json)
    respuestas_df.columns = columnas
    respuestas_df.drop(respuestas_df[respuestas_df['Código'] == "0002760"].index, inplace = True) 
    respuestas_df.sort_values(by=['Inicio', 'Fin'], inplace=True, ascending=True, ignore_index=True)
    respuestas_df.reindex(calificaciones_df.index)
    respuestas_df.to_excel('files/tool_output/03_anwers_and_califications_dataframe/answers.xlsx', index = False)


execution()