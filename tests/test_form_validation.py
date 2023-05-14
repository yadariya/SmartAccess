import pytest
import re
from sqr import FormColor, FormDateTime


@pytest.mark.parametrize("color_input", [
    'rgb(0, 0, 0)',
    'rgb(255, 255, 255)',
    'rgb(128, 0, 255)',
    'rgb(0, 255, 128)',
])
def test_form_color_valid(color_input):
    form_color = FormColor()
    assert re.fullmatch(form_color.regex, color_input)


@pytest.mark.parametrize("color_input", [
    'rgb(0,0,0)',
    'rgb(-1, 0, 255)',
    'rgba(0, 255, 128, 0.5)',
    'rgb(0, 255)',
    'rgb()',
])
def test_form_color_invalid(color_input):
    form_color = FormColor()
    assert not re.fullmatch(form_color.regex, color_input)


@pytest.mark.parametrize("datetime_input", [
    '2006-01-02T15:04:05+01:00',
    '2006-01-02T15:04+01:00',
    '2006-01-02T15:04:05Z',
    '2006-01-02T15:04Z',
])
def test_form_date_time_valid(datetime_input):
    form_datetime = FormDateTime()
    assert re.fullmatch(form_datetime.regex, datetime_input)


@pytest.mark.parametrize("datetime_input", [
    '2006-01-02T25:04+01:00',
    '2006-01-02T15:04:05',
    '2006-01-02 15:04:05Z',
    '2006/01/02T15:04Z',
])
def test_form_date_time_invalid(datetime_input):
    form_datetime = FormDateTime()
    assert not re.fullmatch(form_datetime.regex, datetime_input)
