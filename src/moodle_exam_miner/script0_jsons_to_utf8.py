import io
import json
import codecs
from typing import Tuple, List


def jsons_to_utf8() -> Tuple[List, List, List]:
    """
    Carga los 3 json (exam_califications, exam_logs y exam_answers) contenidos en /tool_input/ y los pasa a utf8
    Returns:
        Los 3 json en utf8
    """
    with io.open('files/tool_input/exam_califications.json', 'r', encoding='utf-8-sig') as json_marks:
        json_marks = json.load(json_marks)
    with codecs.open('files/tool_input/exam_califications_utf8.json', 'w', encoding='utf-8') as f:
        json.dump(json_marks, f, ensure_ascii=False, indent=2)

    with io.open('files/tool_input/exam_logs.json', 'r', encoding='utf-8-sig') as json_logs:
        json_logs = json.load(json_logs)
    with codecs.open('files/tool_input/exam_logs_utf8.json', 'w', encoding='utf-8') as f:
        json.dump(json_logs, f, ensure_ascii=False, indent=2)

    with io.open('files/tool_input/exam_answers.json', 'r', encoding='utf-8-sig') as json_answers:
        json_answers = json.load(json_answers)
    with codecs.open('files/tool_input/exam_answers_utf8.json', 'w', encoding='utf-8') as f:
        json.dump(json_answers, f, ensure_ascii=False, indent=2)

    return json_marks, json_logs, json_answers
