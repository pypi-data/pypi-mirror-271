import re

import pytest

from nerval import evaluate
from nerval.parse import get_type_label, parse_line

expected_parsed_annot = {
    "entity_count": {"All": 3, "DAT": 1, "LOC": 1, "PER": 1},
    "labels": [
        "B-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "B-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "O",
        "O",
        "O",
        "O",
        "B-DAT",
        "I-DAT",
        "I-DAT",
        "I-DAT",
        "O",
        "O",
    ],
    "words": "Gérard de Nerval was born in Paris in 1808 .",
}

expected_parsed_predict = {
    "entity_count": {"All": 3, "DAT": 1, "***": 1, "PER": 1},
    "labels": [
        "B-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "O",
        "B-***",
        "I-***",
        "I-***",
        "I-***",
        "I-***",
        "O",
        "O",
        "O",
        "O",
        "B-DAT",
        "I-DAT",
        "I-DAT",
        "I-DAT",
        "O",
        "O",
        "O",
    ],
    "words": "G*rard de *N*erval bo*rn in Paris in 1833 *.",
}

expected_parsed_end_of_file = {
    "entity_count": {"All": 3, "LOC": 2, "PER": 1},
    "labels": [
        "B-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "B-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "I-PER",
        "O",
        "B-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
        "I-LOC",
    ],
    "words": "Louis par la grâce de Dieu roy de France et de Navarre",
}


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        (pytest.lazy_fixture("fake_annot_bio"), expected_parsed_annot),
        (pytest.lazy_fixture("fake_predict_bio"), expected_parsed_predict),
        (pytest.lazy_fixture("empty_bio"), None),
        (pytest.lazy_fixture("fake_annot_with_empty_lines_bio"), expected_parsed_annot),
        (pytest.lazy_fixture("bioeslu_bio"), expected_parsed_annot),
        (pytest.lazy_fixture("end_of_file_bio"), expected_parsed_end_of_file),
    ],
)
def test_parse_bio(test_input, expected):
    lines = test_input.read_text().strip().splitlines()
    assert evaluate.parse_bio(lines) == expected


def test_parse_bio_bad_input(bad_bio):
    lines = bad_bio.read_text().strip().splitlines()
    with pytest.raises(
        Exception, match=re.escape("The file is not in BIO format: check line 1 (file)")
    ):
        evaluate.parse_bio(lines)


@pytest.mark.parametrize(
    ("line", "word", "label"),
    [
        ("Hi B-ORG", "Hi", "B-ORG"),
        ("Hi B-Org or maybe not org", "Hi", "B-Org or maybe not org"),
        ("1258 B-Date et Lieu", "1258", "B-Date et Lieu"),
        ("Devoti B-Sous-titre", "Devoti", "B-Sous-titre"),
    ],
)
def test_parse_line(line, word, label):
    assert parse_line(index=0, line=line) == (word, label)


@pytest.mark.parametrize(
    "line",
    [("HiB-ORG"), ("HiB-ORG or maybe not")],
)
def test_parse_line_crash(line):
    with pytest.raises(
        Exception,
        match=re.escape(f"The file is not in BIO format: check line 0 ({line})"),
    ):
        parse_line(index=0, line=line)


@pytest.mark.parametrize(
    ("label", "expected_type"),
    [
        ("B-ORG", "ORG"),
        ("B-Date et Lieu", "Date et Lieu"),
        ("I-Date et Lieu", "Date et Lieu"),
        ("B-Sous-titre", "Sous-titre"),
    ],
)
def test_get_type_label(label, expected_type):
    assert get_type_label(label) == expected_type
