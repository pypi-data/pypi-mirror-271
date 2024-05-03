import pytest

from nerval import ALL_ENTITIES, evaluate


@pytest.mark.parametrize(
    ("annot", "predict", "matches"),
    [
        (
            {ALL_ENTITIES: 3, "DAT": 1, "LOC": 1, "PER": 1},
            {ALL_ENTITIES: 3, "DAT": 1, "***": 1, "PER": 1},
            {ALL_ENTITIES: 1, "PER": 1, "LOC": 0, "DAT": 0},
        ),
    ],
)
def test_compute_scores(annot, predict, matches):
    assert evaluate.compute_scores(annot, predict, matches) == {
        "***": {
            "P": 0.0,
            "R": None,
            "F1": None,
            "predicted": 1,
            "matched": 0,
            "Support": None,
        },
        "DAT": {
            "P": 0.0,
            "R": 0.0,
            "F1": 0,
            "predicted": 1,
            "matched": 0,
            "Support": 1,
        },
        ALL_ENTITIES: {
            "P": 0.3333333333333333,
            "R": 0.3333333333333333,
            "F1": 0.3333333333333333,
            "predicted": 3,
            "matched": 1,
            "Support": 3,
        },
        "PER": {
            "P": 1.0,
            "R": 1.0,
            "F1": 1.0,
            "predicted": 1,
            "matched": 1,
            "Support": 1,
        },
        "LOC": {
            "P": None,
            "R": 0.0,
            "F1": None,
            "predicted": None,
            "matched": 0,
            "Support": 1,
        },
    }
