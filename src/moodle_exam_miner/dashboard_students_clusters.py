import pandas as pd
from datetime import timedelta


def funcion_clusters(py_cheat_df, merge_df, config_num_stud_cluster, config_dif_minutos_cl, num_preguntas):
    py_cheat = py_cheat_df.copy()
    lista_i = []
    lista_j = []
    for i in range(0, len(py_cheat)):
        for j in range(0, len(py_cheat)):
            if ((py_cheat.iloc[i]['Productividad'] <= py_cheat.iloc[j]['Productividad']) &
                    ((py_cheat.iloc[i]['Fin'] >= (py_cheat.iloc[j]['Inicio'] -
                                                  timedelta(minutes=config_dif_minutos_cl))) &
                     (py_cheat.iloc[i]['Fin'] <= (py_cheat.iloc[j]['Inicio'] +
                                                  timedelta(minutes=config_dif_minutos_cl))))):
                lista_i.append(py_cheat.iloc[i]['Código'])
                lista_j.append(py_cheat.iloc[j]['Código'])

    data_tuples = list(zip(lista_i, lista_j))
    salida = pd.DataFrame(data_tuples, columns=['i', 'j'])

    lista_de_cluster = []
    lista_de_usuarios = salida.i.to_list()
    lista_de_usuarios = list(dict.fromkeys(lista_de_usuarios))  # nos quedamos con los usuarios sin duplicados
    for usuario in lista_de_usuarios:
        minitabla = salida[salida['i'] == usuario]
        jotas = minitabla.j.to_list()
        longitud_minitabla = len(minitabla)
        if len(lista_de_cluster) == 0:
            lista_de_cluster = minitabla.values.tolist()
        else:
            flag_encontrado = False
            for cluster in range(0, len(lista_de_cluster)):
                if usuario == lista_de_cluster[cluster][-1] and longitud_minitabla > 1:  # preparamos los cluster
                    # para albergar los nuevos
                    flag_encontrado = True
                    for f in range(0, longitud_minitabla - 1):
                        cluster_a_copiar = lista_de_cluster[cluster].copy()
                        lista_de_cluster.append(cluster_a_copiar)
                else:
                    if usuario == lista_de_cluster[cluster][-1] and longitud_minitabla == 1:
                        flag_encontrado = True
            if flag_encontrado:
                count = 0
                for cluster2 in range(0, len(lista_de_cluster)):  # albergamos los nuevos
                    if usuario == lista_de_cluster[cluster2][-1]:
                        count += 1

                if count == longitud_minitabla:
                    for cluster2 in range(0, len(lista_de_cluster)):  # alvergamos los nuevos
                        if usuario == lista_de_cluster[cluster2][-1] and longitud_minitabla > 1:
                            lista_de_cluster[cluster2].append(jotas[-1])
                            jotas.pop()
                        if usuario == lista_de_cluster[cluster2][-1] and longitud_minitabla == 1:
                            lista_de_cluster[cluster2].append(jotas[-1])
                else:
                    operacion = count / longitud_minitabla  # hacemos jota tantas veces como sea necesario para alojar
                    operacion = int(operacion)
                    jotas = jotas * operacion
                    jotas.sort()
                    for cluster2 in range(0, len(lista_de_cluster)):  # alojamos los nuevos
                        if usuario == lista_de_cluster[cluster2][-1]:
                            lista_de_cluster[cluster2].append(jotas[-1])
                            jotas.pop()
            else:
                aux = minitabla.values.tolist()
                for x in range(0, len(aux)):
                    lista_de_cluster.append(aux[x])

    lista_usuarios_sin_repetir = []
    lista_de_cluster_2 = []
    for row in lista_de_cluster:
        # para formar un cluster hay que tener al menos config_num_stud_cluster estudiantes (parámetro web)
        if len(row) >= config_num_stud_cluster:
            for user in row:
                if user not in lista_usuarios_sin_repetir:
                    lista_usuarios_sin_repetir.append(user)
            lista_de_cluster_2.append(row)

    df_merged = merge_df.copy()
    df_merged2 = pd.DataFrame(columns=df_merged.columns)
    for user in lista_usuarios_sin_repetir:
        df_aux = df_merged[df_merged['Código'] == user]
        df_merged2 = df_merged2.append(df_aux)

    df_merged2.reset_index(drop=True, inplace=True)

    for i in range(0, len(df_merged2)):
        for j in range(2, num_preguntas + 1):
            aux = j - 1
            df_merged2['Q' + str(j) + '_m'][i] = \
                df_merged2['Q' + str(j) + '_m'][i] + df_merged2['Q' + str(aux) + '_m'][i]

    # transformamos las columnas Q0_m, Q1_m... a Pregunta 0, Pregunta 1...
    for preg in range(0, num_preguntas + 1):
        df_merged2 = df_merged2.rename(columns={'Q' + str(preg) + '_m': 'Pregunta ' + str(preg)})

    df_final = pd.DataFrame()
    for x in range(0, num_preguntas + 1):
        melt = pd.melt(df_merged2,
                       id_vars=['Código', 'Tiempo', 'Productividad', 'Q' + str(x) + '_t', 'Q' + str(x) + '_q',
                                'Q' + str(x) + '_a'],
                       value_vars=['Pregunta ' + str(x)],
                       value_name='Nota')

        melt = melt.rename(columns={'Q' + str(x) + '_t': 'Hora',
                                    'Q' + str(x) + '_q': 'Pregunta',
                                    'Q' + str(x) + '_a': 'Respuesta',
                                    'Tiempo': 'Tiempo que tardó en hacer el examen',
                                    'Productividad': 'Productividad al final del examen'
                                    })
        df_final = df_final.append(melt)

    df_final["variable"].replace({"Pregunta 0": "Inicio"}, inplace=True)

    df_definitivo = pd.DataFrame(columns=df_final.columns)
    id_cluster = 1

    if len(lista_de_cluster_2) > 0:
        for cluster in lista_de_cluster_2:
            for user in cluster:
                df_aux = df_final[df_final['Código'] == user]
                df_aux['Cluster'] = 'Cluster ' + str(id_cluster)
                df_definitivo = df_definitivo.append(df_aux)
            id_cluster = id_cluster + 1
    else:
        df_aux = df_final[df_final['Código'] == py_cheat.iloc[0]['Código']]
        df_aux['Cluster'] = 'Cluster ' + str(id_cluster)
        df_definitivo = df_definitivo.append(df_aux)
        print("no cluster")

    return df_definitivo
