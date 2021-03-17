import pytest
import util.helper

@pytest.fixture
def empty_string():
  return ''

@pytest.fixture
def escape_characters():
  return '<>\'"\\&?='

def test_gather_data(empty_string):
  assert util.helper.gather_data(empty_string) == ''

def test_gather_data(escape_characters):
  assert util.helper.gather_data(escape_characters) == ''