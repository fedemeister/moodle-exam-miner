from tests.fixtures_global.fixtures_global import fixture_json_logs
from tests.fixtures_global.fixtures_global import fixture_json_answers
from tests.fixtures_global.fixtures_global import fixture_json_marks

from tests.fixtures_global_anonimizados import fixture_json_logs_anonymized
from tests.fixtures_global_anonimizados import fixture_json_answers_anonymized
from tests.fixtures_global_anonimizados import fixture_json_marks_anonymized
from tests.fixtures_global_anonimizados import fixture_name_user_dictionary

import scripts.script1.anonymize_input as anonymize_input
from operator import itemgetter


def test_get_promedio_general(fixture_json_marks):
    actual = anonymize_input.get_promedio_general(fixture_json_marks)
    expected = ["6,25", "1,00", "0,50", "0,75", "0,50", "0,75", "0,75", "0,25", "0,50", "1,00", "1,00"]
    assert all([a == b for a, b in zip(actual, expected)])


def test_promedio_general_is_len_11(fixture_json_marks):
    actual = anonymize_input.get_promedio_general(fixture_json_marks)
    expected = 11
    assert (len(actual) == expected)


def test_anonymize_log(fixture_json_logs, fixture_json_logs_anonymized, fixture_name_user_dictionary):
    fixture_json_logs = fixture_json_logs[0]
    fixture_json_logs_anonymized = fixture_json_logs_anonymized[0]

    actual = anonymize_input.anonymize_log(fixture_json_logs, fixture_name_user_dictionary)
    expected = fixture_json_logs_anonymized
    assert all([a == b for a, b in zip(actual, expected)])


def test_anonymize_marks(fixture_json_marks, fixture_json_marks_anonymized, fixture_name_user_dictionary):
    fixture_json_marks = anonymize_input.anonymize_others(fixture_json_marks, fixture_name_user_dictionary)
    actual = sorted(fixture_json_marks, key=itemgetter(0))

    expected = sorted(fixture_json_marks_anonymized, key=itemgetter(0))
    assert all([a == b for a, b in zip(actual, expected)])


def test_anonymize_answers(fixture_json_answers, fixture_json_answers_anonymized, fixture_name_user_dictionary):
    fixture_json_answers = anonymize_input.anonymize_others(fixture_json_answers, fixture_name_user_dictionary)
    actual = sorted(fixture_json_answers, key=itemgetter(0))

    expected = sorted(fixture_json_answers_anonymized, key=itemgetter(0))
    assert all([a == b for a, b in zip(actual, expected)])
