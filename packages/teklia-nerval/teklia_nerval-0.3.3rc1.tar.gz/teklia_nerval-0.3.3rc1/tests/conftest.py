from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture()
def fake_annot_bio():
    return FIXTURES / "test_annot.bio"


@pytest.fixture()
def fake_annot_with_empty_lines_bio():
    return FIXTURES / "test_annot_with_empty_lines.bio"


@pytest.fixture()
def fake_predict_bio():
    return FIXTURES / "test_predict.bio"


@pytest.fixture()
def empty_bio():
    return FIXTURES / "test_empty.bio"


@pytest.fixture()
def bad_bio():
    return FIXTURES / "test_bad.bio"


@pytest.fixture()
def bioeslu_bio():
    return FIXTURES / "bioeslu.bio"


@pytest.fixture()
def end_of_file_bio():
    return FIXTURES / "end_of_file.bio"


@pytest.fixture()
def nested_bio():
    return FIXTURES / "test_nested.bio"


@pytest.fixture()
def folder_bio():
    return FIXTURES


@pytest.fixture()
def csv_file_error():
    return FIXTURES / "test_mapping_file_error.csv"


@pytest.fixture()
def csv_file():
    return FIXTURES / "test_mapping_file.csv"
