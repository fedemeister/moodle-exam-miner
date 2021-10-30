import pandas_read_xml as pdx
import pandas as pd


def execution():
    df = pdx.read_xml('files/tool_input/exam_questions_set.xml',
                      ['quiz', 'question'],
                      root_is_rows=False,
                      transpose=False,
                      encoding='UTF8')

    is_multichoice = df['@type'] == 'multichoice'
    df_multichoice = df[is_multichoice]
    df_multichoice_new = df_multichoice.reset_index(drop=True)

    rows, columns = df_multichoice_new.shape

    raw_q = []
    raw_ans = []
    raw_qual = []
    for i in range(0, rows):
        raw_q.append(df_multichoice_new.name.iloc[i]['text'])
        raw_q.append(df_multichoice_new.name.iloc[i]['text'])
        raw_q.append(df_multichoice_new.name.iloc[i]['text'])
        raw_q.append(df_multichoice_new.name.iloc[i]['text'])
        for j in range(0, 4):
            raw_ans.append(df_multichoice_new.answer.iloc[i][j]['text'])
            raw_qual.append(df_multichoice_new.answer.iloc[i][j]['@fraction'])

    raw_data = {'Question': raw_q, 'Answer': raw_ans, 'Qualification': raw_qual}

    raw_output = pd.DataFrame(raw_data)
    raw_output["Qualification"].replace({"100": float(1), "-25": float(-0.25)}, inplace=True)

    raw_output.to_excel('files/tool_output/02_questions_and_answers_set/raw_quest_answ_output.xlsx', index=False)


execution()
