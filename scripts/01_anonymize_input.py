import json
import codecs
import pandas as pd


def anonymizer(reverse_log: bool = False):
    '''
        Anonymize the follow JSON files:
        exam_answers_utf8.json
        exam_califications_utf8.json
        exam_logs_utf8.json
        
        Parameters:
            reverse_log (bool): If True, the fuction reverse the JSON files
    
        Returns:
            data(list of list): Same file as the input but anonymized.     
    '''

    with open('files/tool_input/exam_answers_utf8.json', encoding='utf-8') as json_file:
        json_exam_answers = json.load(json_file)

    with open('files/tool_input/exam_califications_utf8.json', encoding='utf-8') as json_file:
        json_exam_califications = json.load(json_file)

    with open('files/tool_input/exam_logs_utf8.json', encoding='utf-8') as json_file:
        json_logs = json.load(json_file)

        # this is because our json is a list of "list of lists" (three levels)
    json_exam_answers = json_exam_answers[0]
    json_exam_califications = json_exam_califications[0]
    json_logs = json_logs[0]

    if reverse_log == True:
        json_logs = json_logs[::-1]  # reversing log
        json_exam_califications = json_exam_califications[::-1]

    set_unique_names = {(i[1]) for i in json_logs}  # i[1] is the name

    # let's create a list with numbers between 0 to input unique names lenght.
    number_list = [*range(len(set_unique_names))]

    # for every number there, we put a number at the end of the 'user' word.
    user_number_list = list(map(lambda number: 'user' + str(number), number_list))

    if (len(number_list) == len(set_unique_names)):
        name_user_dictionary = dict(zip(set_unique_names, user_number_list))
        with codecs.open('files/tool_output/01_anonymized_input/name_user_dictionary.json', 'w', encoding='utf-8') as f:
            json.dump(name_user_dictionary, f, ensure_ascii=False, indent=2)

            # df = pd.read_json ('files/tool_output/01_anonymized_input/name_user_dictionary.json', encoding='utf-8')
        # df.to_csv ('files/tool_output/01_anonymized_input/name_user_dictionary.csv', index = None)

    # anonymizing json files
    for entry in json_logs:
        if (entry[1] in name_user_dictionary):
            entry[1] = name_user_dictionary.get(entry[1])
        if (entry[2] in name_user_dictionary):
            entry[2] = name_user_dictionary.get(entry[2])

    for entry in json_exam_answers:
        if ((entry[1] + ' ' + entry[0]) in name_user_dictionary):
            entry[1] = name_user_dictionary.get(entry[1] + ' ' + entry[0])
            entry[0] = entry[1]
            entry[2] = entry[1]
            entry[3] = entry[1]

    for entry in json_exam_califications:
        if ((entry[1] + ' ' + entry[0]) in name_user_dictionary):
            entry[1] = name_user_dictionary.get(entry[1] + ' ' + entry[0])
            entry[0] = entry[1]
            entry[2] = entry[1]
            entry[3] = entry[1]
    with codecs.open('files/tool_output/01_anonymized_input/exam_answers_utf8_anonymized.json', 'w',
                     encoding='utf-8') as f:
        json.dump(json_exam_answers, f, ensure_ascii=False, indent=2)

    with codecs.open('files/tool_output/01_anonymized_input/exam_califications_utf8_anonymized.json', 'w',
                     encoding='utf-8') as f:
        json.dump(json_exam_califications, f, ensure_ascii=False, indent=2)

    with codecs.open('files/tool_output/01_anonymized_input/exam_logs_utf8_anonymized.json', 'w',
                     encoding='utf-8') as f:
        json.dump(json_logs, f, ensure_ascii=False, indent=2)


anonymizer(reverse_log=True)
