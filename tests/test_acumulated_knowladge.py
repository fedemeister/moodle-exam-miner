from pandas import testing
from tests.fixtures_global.fixtures_global_anonimizados import fixture_merge_df_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_py_cheat_df_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_answers_df_cleaned_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_df_answer_times_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_conocimiento_acumulado_anonymized
from tests.fixtures_global.fixtures_global_anonimizados import fixture_merge_df_json_anonymized

from tests.fixtures_global.fixtures_global import fixture_xml_dataframe_with_answers_from_answers_df
from tests.fixtures_global.fixtures_global import fixture_ratio_pregunta
from tests.fixtures_global.fixtures_global_anonimizados import fixture_json_marks_formatted_anonymized

from moodle_exam_miner.script7_acumulated_knowladge import run_script07


def test_merge_df(fixture_merge_df_anonymized,
                  fixture_answers_df_cleaned_anonymized,
                  fixture_xml_dataframe_with_answers_from_answers_df,
                  fixture_df_answer_times_anonymized,
                  fixture_py_cheat_df_anonymized,
                  fixture_json_marks_formatted_anonymized
                  ):
    merge_df, ignore1, ignore2, ignore3 = run_script07(fixture_answers_df_cleaned_anonymized,
                                                       fixture_xml_dataframe_with_answers_from_answers_df,
                                                       fixture_df_answer_times_anonymized,
                                                       fixture_py_cheat_df_anonymized,
                                                       fixture_json_marks_formatted_anonymized,
                                                       num_preguntas=10)
    actual = merge_df
    expected = fixture_merge_df_anonymized
    testing.assert_frame_equal(actual, expected)


def test_ratio_preguntas(fixture_ratio_pregunta,
                         fixture_answers_df_cleaned_anonymized,
                         fixture_xml_dataframe_with_answers_from_answers_df,
                         fixture_df_answer_times_anonymized,
                         fixture_py_cheat_df_anonymized,
                         fixture_json_marks_formatted_anonymized
                         ):
    ignore1, ratio_preguntas, ignore2, ignore3 = run_script07(fixture_answers_df_cleaned_anonymized,
                                                              fixture_xml_dataframe_with_answers_from_answers_df,
                                                              fixture_df_answer_times_anonymized,
                                                              fixture_py_cheat_df_anonymized,
                                                              fixture_json_marks_formatted_anonymized, num_preguntas=10)
    actual = ratio_preguntas
    expected = fixture_ratio_pregunta
    assert all([a == b for a, b in zip(actual, expected)])


def test_conocimiento_acumulado(fixture_conocimiento_acumulado_anonymized,
                                fixture_answers_df_cleaned_anonymized,
                                fixture_xml_dataframe_with_answers_from_answers_df,
                                fixture_df_answer_times_anonymized,
                                fixture_py_cheat_df_anonymized,
                                fixture_json_marks_formatted_anonymized
                                ):
    ignore1, ignore2, conocimiento_acumulado, ignore3 = run_script07(fixture_answers_df_cleaned_anonymized,
                                                                     fixture_xml_dataframe_with_answers_from_answers_df,
                                                                     fixture_df_answer_times_anonymized,
                                                                     fixture_py_cheat_df_anonymized,
                                                                     fixture_json_marks_formatted_anonymized,
                                                                     num_preguntas=10)
    actual = conocimiento_acumulado
    expected = fixture_conocimiento_acumulado_anonymized
    assert all([a == b for a, b in zip(actual, expected)])


def test_merge_df_json(fixture_merge_df_json_anonymized,
                       fixture_answers_df_cleaned_anonymized,
                       fixture_xml_dataframe_with_answers_from_answers_df,
                       fixture_df_answer_times_anonymized,
                       fixture_py_cheat_df_anonymized,
                       fixture_json_marks_formatted_anonymized
                       ):
    ignore1, ignore2, ignore3, merge_df_json = run_script07(fixture_answers_df_cleaned_anonymized,
                                                            fixture_xml_dataframe_with_answers_from_answers_df,
                                                            fixture_df_answer_times_anonymized,
                                                            fixture_py_cheat_df_anonymized,
                                                            fixture_json_marks_formatted_anonymized,
                                                            num_preguntas=10)
    actual = merge_df_json
    expected = fixture_merge_df_json_anonymized
    assert all([a == b for a, b in zip(actual, expected)])
