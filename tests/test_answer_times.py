import pandas as pd
import pytest
from tests.fixtures_global.fixtures_global_anonimizados import fixture_df_answer_times_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_new_json_logs_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_json_marks_formatted_anonymized

from scripts.script4.answer_times import run_script04


def test_answer_times_df(fixture_json_marks_formatted_anonymized, fixture_new_json_logs_anonymized,
                         fixture_df_answer_times_anonymized):
    marks_df = fixture_json_marks_formatted_anonymized
    json = fixture_new_json_logs_anonymized
    actual = run_script04(marks_df, json)
    expected = fixture_df_answer_times_anonymized
    pd.testing.assert_frame_equal(actual, expected)
