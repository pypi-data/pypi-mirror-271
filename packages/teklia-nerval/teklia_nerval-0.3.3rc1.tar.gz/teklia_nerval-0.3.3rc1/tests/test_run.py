import re
from pathlib import Path

import pytest

from nerval import evaluate


@pytest.mark.parametrize(
    ("annotation", "prediction", "expected"),
    [
        (
            pytest.lazy_fixture("fake_annot_bio"),
            pytest.lazy_fixture("fake_predict_bio"),
            {
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
                "All": {
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
            },
        ),
        (
            pytest.lazy_fixture("nested_bio"),
            pytest.lazy_fixture("nested_bio"),
            {
                "All": {
                    "P": 1.0,
                    "R": 1.0,
                    "F1": 1.0,
                    "predicted": 3,
                    "matched": 3,
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
                    "P": 1.0,
                    "R": 1.0,
                    "F1": 1.0,
                    "predicted": 2,
                    "matched": 2,
                    "Support": 2,
                },
            },
        ),
    ],
)
def test_run(annotation, prediction, expected):
    assert (
        evaluate.run(
            annotation=annotation,
            prediction=prediction,
            threshold=0.3,
            verbose=False,
        )
        == expected
    )


def test_run_empty_bio(empty_bio):
    with pytest.raises(
        Exception, match="No content found in annotation or prediction files."
    ):
        evaluate.run(empty_bio, empty_bio, 0.3, False)


def test_run_empty_entry():
    with pytest.raises(
        AssertionError,
        match=re.escape("Error: Input file invalid.bio does not exist"),
    ):
        evaluate.run(Path("invalid.bio"), Path("invalid.bio"), 0.3, False)


def test_run_invalid_header(csv_file_error, folder_bio):
    with pytest.raises(
        Exception, match="Columns in the CSV mapping should be: Annotation,Prediction"
    ):
        evaluate.run_multiple(csv_file_error, folder_bio, 0.3, False)


def test_run_multiple(csv_file, folder_bio):
    with pytest.raises(
        Exception, match="No file found for files demo_annot.bio, demo_predict.bio"
    ):
        evaluate.run_multiple(csv_file, folder_bio, 0.3, False)
