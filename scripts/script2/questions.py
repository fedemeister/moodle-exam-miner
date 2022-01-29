import pandas_read_xml as pdx
import pandas as pd
from typing import Tuple

df = pdx.read_xml('files/tool_input/exam_questions_set.xml',
                  ['quiz', 'question'],
                  root_is_rows=False,
                  transpose=False,
                  encoding='UTF8')


def get_just_multichoice_dataframe(df_raw_xml: pd.DataFrame) -> pd.DataFrame:
    """
    Funcion para eliminar elementos innecesarios del df_xml obteniendo únicamente el campo multichoice.

    Parameters:
        df_raw_xml(pd.DataFrame):Dataframe
    Returns:
        df_multichoice(pd.DataFrame): Dataframe solo multichoice
    """
    df_multichoice = df_raw_xml[df_raw_xml['@type'] == 'multichoice'].reset_index(drop=True)
    return df_multichoice


def execution(df_raw_xml: pd.DataFrame) -> pd.DataFrame:
    """
    Funcion para ejecutar el flujo del script2 (lectura de xml y devolver un dataframe con los campos importantes).

    Parameters:
        df_raw_xml(pd.DataFrame):Dataframe
    Returns:
        df_xml_output(pd.DataFrame): Dataframe limpia con ['Question', 'Answer', 'Mark']
    """
    df_multichoice = get_just_multichoice_dataframe(df_raw_xml)

    rows, columns = df_multichoice.shape

    raw_answers, raw_questions, raw_marks = extract_xml_information(df_multichoice, rows)

    raw_data = {'Question': raw_questions, 'Answer': raw_answers, 'Mark': raw_marks}

    df_xml_output = pd.DataFrame(raw_data)
    df_xml_output["Mark"].replace({"100": float(1), "-25": float(-0.25)}, inplace=True)

    df_xml_output.to_excel('files/tool_output/02_questions_and_answers_set/raw_quest_answ_output.xlsx', index=False)
    return df_xml_output


def extract_xml_information(df_multichoice_new: pd.DataFrame, rows: int) -> Tuple[list, list, list]:
    """
    Funcion para ejecutar el flujo del script2 (lectura de xml y devolver un dataframe con los campos importantes).

    Parameters:
        df_multichoice_new(pd.DataFrame):Dataframe
        rows(int): cantidad de filas del dataframe
    Returns:
        raw_answers, raw_questions, raw_marks(tuple of (list, list, list)): Tupla de listas
    """
    raw_questions = []
    raw_answers = []
    raw_marks = []
    rows = int(rows)
    for i in range(0, rows):
        raw_questions.append(df_multichoice_new.name.iloc[i]['text'])
        raw_questions.append(df_multichoice_new.name.iloc[i]['text'])
        raw_questions.append(df_multichoice_new.name.iloc[i]['text'])
        raw_questions.append(df_multichoice_new.name.iloc[i]['text'])
        for j in range(0, 4):
            raw_answers.append(df_multichoice_new.answer.iloc[i][j]['text'])
            raw_marks.append(df_multichoice_new.answer.iloc[i][j]['@fraction'])
    return raw_answers, raw_questions, raw_marks


def run_script02() -> pd.DataFrame:
    df_xml_output = execution(df_raw_xml=df)
    return df_xml_output
