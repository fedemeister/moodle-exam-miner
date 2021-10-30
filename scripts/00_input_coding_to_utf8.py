import io
import json
import codecs

with io.open('files/tool_input/exam_califications.json', 'r', encoding='utf-8-sig') as json_file:
    data = json.load(json_file)
with codecs.open('files/tool_input/exam_califications_utf8.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with io.open('files/tool_input/exam_logs.json', 'r', encoding='utf-8-sig') as json_file:
    data = json.load(json_file)
with codecs.open('files/tool_input/exam_logs_utf8.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with io.open('files/tool_input/exam_answers.json', 'r', encoding='utf-8-sig') as json_file:
    data = json.load(json_file)
with codecs.open('files/tool_input/exam_answers_utf8.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
