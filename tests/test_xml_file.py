from collections import OrderedDict
import scripts.script2.questions
import pytest
import pandas as pd
from numpy import nan


@pytest.fixture(scope='module')
def df_raw():
    return pd.DataFrame(
        {
            '@type': ['category',
                      'category',
                      'category',
                      'multichoice',
                      'multichoice',
                      'multichoice',
                      'multichoice',
                      'multichoice',
                      'multichoice',
                      'multichoice',
                      'multichoice',
                      'multichoice',
                      'multichoice'],
            'name': [nan,
                     nan,
                     nan,
                     OrderedDict([('text', 'T1 - simple - LIKE')]),
                     OrderedDict([('text', 'T1 - simple - LIKE 2')]),
                     OrderedDict([('text', 'T1 - simple - LIKE 3')]),
                     OrderedDict([('text', 'T1 - simple - LIKE 4')]),
                     OrderedDict([('text', 'T1 - simple - LIKE 5')]),
                     OrderedDict([('text', 'T1 - simple - NULL')]),
                     OrderedDict([('text', 'T1 - simple - NULL 2')]),
                     OrderedDict([('text', 'T1 - simple - NULL 3')]),
                     OrderedDict([('text', 'T1 - simple - NULL 4')]),
                     OrderedDict([('text', 'T1 - simple - NULL 5')])],
            'answer': [nan,
                       nan,
                       nan,
                       [OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre LIKE 'J%' AND nombre NOT LIKE '%m%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre IN 'J*' AND nombre NOT IN '*m*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre = 'J*' AND nombre != '*m*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre IN ('J%') AND nombre NOT IN ('n');</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre LIKE 'J%' AND nombre NOT LIKE '%m%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre IN 'J*' AND nombre IN '*m*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre = 'J*' AND nombre = '*m*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre LIKE 'J%m%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre not LIKE 'J%' AND nombre LIKE '%m%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre NOT IN 'J*' AND nombre IN '*m*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre != 'J*' AND nombre = '*m*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre LIKE '!J%m%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre LIKE ('Juan','Juana','Alberto') AND apellido1 NOT LIKE 'T*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre IN ('Juan','Juana','Alberto') AND apellido1 NOT LIKE 'T';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre IN ('Juan','Juana','Alberto') AND apellido1 NOT LIKE 'T%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre LIKE ('Juan','Juana','Alberto') AND apellido1 NOT LIKE 'T%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre NOT LIKE ('Juan','Juana','Alberto') AND apellido1 LIKE 'T*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE (nombre &lt;&gt; 'Juan' OR nombre &lt;&gt; 'Juana' OR nombre &lt;&gt; 'Alberto') AND apellido1 LIKE 'T%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE nombre NOT IN ('Juan','Juana','Alberto') AND apellido1 LIKE 'T%';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      "<p>SELECT * FROM socios WHERE (nombre &lt;&gt; 'Juan' AND nombre &lt;&gt; 'Juana' AND nombre &lt;&gt; 'Alberto')\xa0AND apellido1 LIKE 'T*';</p>"),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text', '<p>SELECT * FROM socios WHERE telefono IS NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text', '<p>SELECT * FROM socios WHERE telefono = NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono = "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono LIKE "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono IS NOT NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono &lt;&gt; NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono &lt;&gt; "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono NOT LIKE "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono IS NOT NULL AND apellido2 IS NOT NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono &lt;&gt; NULL and apellido2 &lt;&gt; NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono &lt;&gt; "NULL" and apellido2 &lt;&gt; "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE (telefono, apellido2) IS NOT LIKE "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono IS NULL AND apellido2 IS NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono = NULL and apellido2 = NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono = "NULL" and apellido2 = "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE (telefono, apellido2) IS LIKE "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])],
                       [OrderedDict([('@fraction', '100'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono IS NULL AND apellido2 IS NOT NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono = NULL and apellido2 != NULL;</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono = "NULL" and apellido2 != "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))]),
                        OrderedDict([('@fraction', '-25'),
                                     ('@format', 'html'),
                                     ('text',
                                      '<p>SELECT * FROM socios WHERE telefono LIKE "NULL" AND apellido2 NOT LIKE "NULL";</p>'),
                                     ('feedback',
                                      OrderedDict([('@format', 'html'), ('text', None)]))])]]
        }
    )


@pytest.fixture(scope='module')
def df_transformed():
    return pd.DataFrame(
        {
            'Question': ['T1 - simple - LIKE',
                         'T1 - simple - LIKE',
                         'T1 - simple - LIKE',
                         'T1 - simple - LIKE',
                         'T1 - simple - LIKE 2',
                         'T1 - simple - LIKE 2',
                         'T1 - simple - LIKE 2',
                         'T1 - simple - LIKE 2',
                         'T1 - simple - LIKE 3',
                         'T1 - simple - LIKE 3',
                         'T1 - simple - LIKE 3',
                         'T1 - simple - LIKE 3',
                         'T1 - simple - LIKE 4',
                         'T1 - simple - LIKE 4',
                         'T1 - simple - LIKE 4',
                         'T1 - simple - LIKE 4',
                         'T1 - simple - LIKE 5',
                         'T1 - simple - LIKE 5',
                         'T1 - simple - LIKE 5',
                         'T1 - simple - LIKE 5',
                         'T1 - simple - NULL',
                         'T1 - simple - NULL',
                         'T1 - simple - NULL',
                         'T1 - simple - NULL',
                         'T1 - simple - NULL 2',
                         'T1 - simple - NULL 2',
                         'T1 - simple - NULL 2',
                         'T1 - simple - NULL 2',
                         'T1 - simple - NULL 3',
                         'T1 - simple - NULL 3',
                         'T1 - simple - NULL 3',
                         'T1 - simple - NULL 3',
                         'T1 - simple - NULL 4',
                         'T1 - simple - NULL 4',
                         'T1 - simple - NULL 4',
                         'T1 - simple - NULL 4',
                         'T1 - simple - NULL 5',
                         'T1 - simple - NULL 5',
                         'T1 - simple - NULL 5',
                         'T1 - simple - NULL 5'],
            'Answer': ["<p>SELECT * FROM socios WHERE nombre LIKE 'J%' AND nombre NOT LIKE '%m%';</p>",
                       "<p>SELECT * FROM socios WHERE nombre IN 'J*' AND nombre NOT IN '*m*';</p>",
                       "<p>SELECT * FROM socios WHERE nombre = 'J*' AND nombre != '*m*';</p>",
                       "<p>SELECT * FROM socios WHERE nombre IN ('J%') AND nombre NOT IN ('n');</p>",
                       "<p>SELECT * FROM socios WHERE nombre LIKE 'J%' AND nombre NOT LIKE '%m%';</p>",
                       "<p>SELECT * FROM socios WHERE nombre IN 'J*' AND nombre IN '*m*';</p>",
                       "<p>SELECT * FROM socios WHERE nombre = 'J*' AND nombre = '*m*';</p>",
                       "<p>SELECT * FROM socios WHERE nombre LIKE 'J%m%';</p>",
                       "<p>SELECT * FROM socios WHERE nombre not LIKE 'J%' AND nombre LIKE '%m%';</p>",
                       "<p>SELECT * FROM socios WHERE nombre NOT IN 'J*' AND nombre IN '*m*';</p>",
                       "<p>SELECT * FROM socios WHERE nombre != 'J*' AND nombre = '*m*';</p>",
                       "<p>SELECT * FROM socios WHERE nombre LIKE '!J%m%';</p>",
                       "<p>SELECT * FROM socios WHERE nombre LIKE ('Juan','Juana','Alberto') AND apellido1 NOT LIKE 'T*';</p>",
                       "<p>SELECT * FROM socios WHERE nombre IN ('Juan','Juana','Alberto') AND apellido1 NOT LIKE 'T';</p>",
                       "<p>SELECT * FROM socios WHERE nombre IN ('Juan','Juana','Alberto') AND apellido1 NOT LIKE 'T%';</p>",
                       "<p>SELECT * FROM socios WHERE nombre LIKE ('Juan','Juana','Alberto') AND apellido1 NOT LIKE 'T%';</p>",
                       "<p>SELECT * FROM socios WHERE nombre NOT LIKE ('Juan','Juana','Alberto') AND apellido1 LIKE 'T*';</p>",
                       "<p>SELECT * FROM socios WHERE (nombre &lt;&gt; 'Juan' OR nombre &lt;&gt; 'Juana' OR nombre &lt;&gt; 'Alberto') AND apellido1 LIKE 'T%';</p>",
                       "<p>SELECT * FROM socios WHERE nombre NOT IN ('Juan','Juana','Alberto') AND apellido1 LIKE 'T%';</p>",
                       "<p>SELECT * FROM socios WHERE (nombre &lt;&gt; 'Juan' AND nombre &lt;&gt; 'Juana' AND nombre &lt;&gt; 'Alberto')\xa0AND apellido1 LIKE 'T*';</p>",
                       '<p>SELECT * FROM socios WHERE telefono IS NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono = NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono = "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE telefono LIKE "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE telefono IS NOT NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono &lt;&gt; NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono &lt;&gt; "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE telefono NOT LIKE "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE telefono IS NOT NULL AND apellido2 IS NOT NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono &lt;&gt; NULL and apellido2 &lt;&gt; NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono &lt;&gt; "NULL" and apellido2 &lt;&gt; "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE (telefono, apellido2) IS NOT LIKE "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE telefono IS NULL AND apellido2 IS NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono = NULL and apellido2 = NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono = "NULL" and apellido2 = "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE (telefono, apellido2) IS LIKE "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE telefono IS NULL AND apellido2 IS NOT NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono = NULL and apellido2 != NULL;</p>',
                       '<p>SELECT * FROM socios WHERE telefono = "NULL" and apellido2 != "NULL";</p>',
                       '<p>SELECT * FROM socios WHERE telefono LIKE "NULL" AND apellido2 NOT LIKE "NULL";</p>'],
            'Mark': [1.0,
                     -0.25,
                     -0.25,
                     -0.25,
                     -0.25,
                     -0.25,
                     -0.25,
                     1.0,
                     1.0,
                     -0.25,
                     -0.25,
                     -0.25,
                     -0.25,
                     -0.25,
                     1.0,
                     -0.25,
                     -0.25,
                     -0.25,
                     1.0,
                     -0.25,
                     1.0,
                     -0.25,
                     -0.25,
                     -0.25,
                     1.0,
                     -0.25,
                     -0.25,
                     -0.25,
                     1.0,
                     -0.25,
                     -0.25,
                     -0.25,
                     1.0,
                     -0.25,
                     -0.25,
                     -0.25,
                     1.0,
                     -0.25,
                     -0.25,
                     -0.25]
        }
    )


def test_raw_lists_are_not_empty(df_raw):
    actual = scripts.script2.questions.get_just_multichoice_dataframe(df_raw)
    rows, columns = actual.shape
    raw_answers, raw_questions, raw_marks = scripts.script2.questions.extract_xml_information(actual, rows)
    assert (len(raw_answers) > 0 and len(raw_questions) > 0 and len(raw_marks) > 0)


def test_raw_lists_are_equal(df_raw):
    actual = scripts.script2.questions.get_just_multichoice_dataframe(df_raw)
    rows, columns = actual.shape
    raw_answers, raw_questions, raw_marks = scripts.script2.questions.extract_xml_information(actual, rows)
    assert (len(raw_answers) == len(raw_questions) == len(raw_marks) > 0)


def test_xml_data_is_transformed_in_a_correct_dataframe(df_raw, df_transformed):
    actual = scripts.script2.questions.execution(df_raw)
    expected = df_transformed
    pd.testing.assert_frame_equal(actual, expected)


def test_get_multichoice_dataframe(df_raw):
    actual = scripts.script2.questions.get_just_multichoice_dataframe(df_raw)
    expected = df_raw[df_raw['@type'] == 'multichoice'].reset_index(drop=True)
    pd.testing.assert_frame_equal(actual, expected)