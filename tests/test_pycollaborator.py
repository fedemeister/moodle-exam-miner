import pandas as pd

from tests.fixtures_global.fixtures_global_anonimizados import fixture_py_collaborator_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_answers_df_cleaned_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_json_marks_formatted_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_py_cheat_df_anonymized

from moodle_exam_miner.script6_py_collaborator_outputs import run_pycollaborator


def test_py_collaborator(fixture_py_collaborator_anonymized,
                         fixture_answers_df_cleaned_anonymized,
                         fixture_json_marks_formatted_anonymized):
    actual, nothing = run_pycollaborator(fixture_answers_df_cleaned_anonymized,
                                         fixture_json_marks_formatted_anonymized,
                                         num_preguntas=10)
    expected = fixture_py_collaborator_anonymized
    assert actual == expected


def test_py_cheat_df(fixture_py_cheat_df_anonymized,
                     fixture_answers_df_cleaned_anonymized,
                     fixture_json_marks_formatted_anonymized):
    nothig, actual = run_pycollaborator(fixture_answers_df_cleaned_anonymized,
                                        fixture_json_marks_formatted_anonymized,
                                        num_preguntas=10)
    expected = fixture_py_cheat_df_anonymized
    pd.testing.assert_frame_equal(actual, expected)
