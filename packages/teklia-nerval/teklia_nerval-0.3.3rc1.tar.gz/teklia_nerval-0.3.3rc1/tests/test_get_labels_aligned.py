import pytest

from nerval import evaluate

fake_annot_original = "Gérard de Nerval was born in Paris in 1808 ."
fake_predict_original = "G*rard de *N*erval bo*rn in Paris in 1833 *."

fake_annot_aligned = "Gérard de -N-erval was bo-rn in Paris in 1808 -."
fake_predict_aligned = "G*rard de *N*erval ----bo*rn in Paris in 1833 *."

fake_annot_tags_original = [
    # Labels 1
    "B-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 2
    "I-PER",
    # Labels 3
    "I-PER",
    "I-PER",
    # Labels 4
    "I-PER",
    # Labels 5
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 6
    "O",
    # Labels 7
    "O",
    "O",
    "O",
    # Labels 8
    "O",
    # Labels 9
    "O",
    "O",
    "O",
    "O",
    # Labels 10
    "O",
    # Labels 11
    "O",
    "O",
    # Labels 12
    "O",
    # Labels 13
    "B-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    # Labels 14
    "O",
    # Labels 15
    "O",
    "O",
    # Labels 16
    "O",
    # Labels 17
    "B-DAT",
    "I-DAT",
    "I-DAT",
    "I-DAT",
    # Labels 18
    "O",
    # Labels 19
    "O",
]

fake_predict_tags_original = [
    # Labels 1
    "B-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 2
    "I-PER",
    # Labels 3
    "I-PER",
    "I-PER",
    # Labels 4
    "I-PER",
    # Labels 5
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 6
    "O",
    # Labels 7
    "O",
    "O",
    "O",
    "O",
    "O",
    # Labels 8
    "O",
    # Labels 9
    "O",
    "O",
    # Labels 10
    "O",
    # Labels 11
    "***",
    "***",
    "***",
    "***",
    "***",
    # Labels 12
    "O",
    # Labels 13
    "O",
    "O",
    # Labels 14
    "O",
    # Labels 15
    "B-DAT",
    "I-DAT",
    "I-DAT",
    "I-DAT",
    # Labels 16
    "O",
    # Labels 17
    "O",
    "O",
]

expected_annot_tags_aligned = [
    # Labels 1
    "B-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 2
    "I-PER",
    # Labels 3
    "I-PER",
    "I-PER",
    # Labels 4
    "I-PER",
    # Labels 5
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 6
    "O",
    # Labels 7
    "O",
    "O",
    "O",
    # Labels 8
    "O",
    # Labels 9
    "O",
    "O",
    "O",
    "O",
    "O",
    # Labels 10
    "O",
    # Labels 11
    "O",
    "O",
    # Labels 12
    "O",
    # Labels 13
    "B-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    # Labels 14
    "O",
    # Labels 15
    "O",
    "O",
    # Labels 16
    "O",
    # Labels 17
    "B-DAT",
    "I-DAT",
    "I-DAT",
    "I-DAT",
    # Labels 18
    "O",
    # Labels 19
    "O",
    "O",
]

expected_predict_tags_aligned = [
    # Labels 1
    "B-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 2
    "I-PER",
    # Labels 3
    "I-PER",
    "I-PER",
    # Labels 4
    "I-PER",
    # Labels 5
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 6
    "O",
    # Labels 7
    "O",
    "O",
    "O",
    "O",
    # Labels 8
    "O",
    "O",
    "O",
    "O",
    "O",
    # Labels 9
    "O",
    # Labels 10
    "O",
    "O",
    # Labels 11
    "O",
    # Labels 12
    "***",
    "***",
    "***",
    "***",
    "***",
    # Labels 13
    "O",
    # Labels 14
    "O",
    "O",
    # Labels 15
    "O",
    # Labels 16
    "B-DAT",
    "I-DAT",
    "I-DAT",
    "I-DAT",
    # Labels 17
    "O",
    # Labels 18
    "O",
    "O",
]


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        (
            (fake_annot_original, fake_annot_aligned, fake_annot_tags_original),
            expected_annot_tags_aligned,
        ),
        (
            (fake_predict_original, fake_predict_aligned, fake_predict_tags_original),
            expected_predict_tags_aligned,
        ),
    ],
)
def test_get_labels_aligned(test_input, expected):
    assert evaluate.get_labels_aligned(*test_input) == expected


def test_get_labels_aligned_empty_entry():
    with pytest.raises(AssertionError):
        evaluate.get_labels_aligned(None, None, None)
