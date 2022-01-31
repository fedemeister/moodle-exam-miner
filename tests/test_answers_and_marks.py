import pytest
import scripts.script3.answers_and_califications_dataframe
from tests.fixtures_global.fixtures_global import fixture_json_marks
from tests.fixtures_global.fixtures_global import fixture_json_answers

from tests.fixtures_global.fixtures_global import fixture_json_marks_formatted
from tests.fixtures_global.fixtures_global import fixture_json_answers_formatted


def test_format_json_answers(fixture_json_answers, fixture_json_answers_formatted):
    actual = scripts.script3.answers_and_califications_dataframe.formateo_json(fixture_json_answers, True)
    expected = fixture_json_answers_formatted
    assert all([a == b for a, b in zip(actual, expected)])


def test_format_json_marks(fixture_json_marks, fixture_json_marks_formatted):
    actual = scripts.script3.answers_and_califications_dataframe.formateo_json(fixture_json_marks, True)
    expected = fixture_json_marks_formatted
    assert all([a == b for a, b in zip(actual, expected)])
