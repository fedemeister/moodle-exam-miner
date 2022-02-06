from operator import itemgetter
from typing import Tuple, List, Dict


def anonymize_log(json_logs: List, name_user_dictionary: dict) -> List:
    """
        Anonymize the follow JSON file:
        exam_logs_utf8.json

        Parameters:
            json_logs(List): JSON que contiene los logs de moodle
            name_user_dictionary(dict): diccionario para anonimizar los campos

        Returns:
            json_logs: List
    """
    for entry in json_logs:
        if entry[1] in name_user_dictionary:
            entry[1] = name_user_dictionary.get(entry[1])
        if entry[2] in name_user_dictionary:
            entry[2] = name_user_dictionary.get(entry[2])
    return json_logs


def anonymize_others(json_answers_or_marks: List, name_user_dictionary: dict) -> List:
    """
        Anonymize the follow JSON files:
        exam_answers_utf8.json
        exam_califications_utf8.json

        Parameters:
            json_answers_or_marks(List): json que contiene los respuestas o notas del alumno
            name_user_dictionary(dict): diccionario para anonimizar los campos

        Returns:
            json_answers_or_marks: List

    """
    for entry in json_answers_or_marks:
        if (entry[1] + ' ' + entry[0]) in name_user_dictionary:
            entry[1] = name_user_dictionary.get(entry[1] + ' ' + entry[0])
            entry[0] = entry[1]
            entry[2] = entry[1]
            entry[3] = entry[1]

    return json_answers_or_marks


def anonymizer(json_exam_marks, json_logs, json_exam_answers) -> Tuple[List, List, List, List, Dict]:
    """
        Ejecuta el script para anonimizar los JSON a través de la plataforma web
            exam_answers_utf8.json
            exam_califications_utf8.json
            exam_logs_utf8.json

        Returns:
            Tuple[List, List, List, List]: json_logs, json_exam_answers, json_exam_marks, promedio_general
    """

    # this is because our json is a list of "list of lists" (three levels)
    json_exam_answers = json_exam_answers[0]
    json_exam_marks = json_exam_marks[0]
    json_logs = json_logs[0]

    list_unique_names = [(i[1] + ' ' + i[0]) for i in json_exam_answers]  # i[1] is the name

    # let's create a list with numbers between 0 to input unique names length.
    number_list = [*range(len(list_unique_names))]

    # for every number there, we put a number at the end of the 'user' word.
    user_number_list = list(map(lambda number: 'user' + str(number), number_list))

    name_user_dictionary = dict(zip(list_unique_names, user_number_list))

    # anonymize json files
    json_logs = anonymize_log(json_logs, name_user_dictionary)
    json_logs = json_logs[::-1]  # reversing log to order it

    json_exam_answers = anonymize_others(json_exam_answers, name_user_dictionary)
    json_exam_answers = sorted(json_exam_answers, key=itemgetter(0))

    json_exam_marks = anonymize_others(json_exam_marks, name_user_dictionary)
    json_exam_marks = sorted(json_exam_marks, key=itemgetter(0))

    promedio_general = get_promedio_general(json_exam_marks)
    json_exam_marks.pop(0)  # lo elimina también de json_exam_marks

    return json_logs, json_exam_answers, json_exam_marks, promedio_general, name_user_dictionary


def get_promedio_general(json_exam_marks: List) -> List:
    """
        Obtiene el promedio general de notas y elimina ese valor del conjunto de notas de los alumnos

        Returns:
            List: promedio_general. La primera posición es la nota del examen y las demás posiciones es una por cada pregunta del examen

    """
    promedio_general = json_exam_marks[0]
    promedio_general = promedio_general[8:]
    return promedio_general
