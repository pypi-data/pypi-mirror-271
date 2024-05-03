import pytest

from nerval import ALL_ENTITIES, evaluate

THRESHOLD = 0.30


fake_tags_aligned_nested_perfect = [
    # Labels 1
    "B-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 2
    "I-PER",
    # Labels 3
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 4
    "I-PER",
    # Labels 5
    "I-PER",
    "I-PER",
    # Labels 6
    "I-PER",
    # Labels 7
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 8
    "I-PER",
    # Labels 9
    "I-PER",
    "I-PER",
    # Labels 10
    "I-PER",
    # Labels 11
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 12
    "I-PER",
    # Labels 13
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 14
    "I-PER",
    # Labels 15
    "I-PER",
    "I-PER",
    # Labels 16
    "I-PER",
    # Labels 17
    "B-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    # Labels 18
    "I-PER",
    # Labels 19
    "I-PER",
    "I-PER",
    # Labels 20
    "I-PER",
    # Labels 21
    "I-PER",
    "I-PER",
    # Labels 22
    "O",
    # Labels 23
    "B-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    # Labels 24
    "O",
    # Labels 25
    "O",
]


fake_tags_aligned_nested_false = [
    # Labels 1
    "B-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 2
    "I-PER",
    # Labels 3
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 4
    "I-PER",
    # Labels 5
    "I-PER",
    "I-PER",
    # Labels 6
    "I-PER",
    # Labels 7
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 8
    "I-PER",
    # Labels 9
    "I-PER",
    "I-PER",
    # Labels 10
    "I-PER",
    # Labels 11
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 12
    "I-PER",
    # Labels 13
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 14
    "I-PER",
    # Labels 15
    "I-PER",
    "I-PER",
    # Labels 16
    "I-PER",
    # Labels 17
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    "I-PER",
    # Labels 18
    "I-PER",
    # Labels 19
    "I-PER",
    "I-PER",
    # Labels 20
    "I-PER",
    # Labels 21
    "I-PER",
    "I-PER",
    # Labels 22
    "O",
    # Labels 23
    "B-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    "I-LOC",
    # Labels 24
    "O",
    # Labels 25
    "O",
]

fake_predict_tags_aligned = [
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
    "B-***",
    "I-***",
    "I-***",
    "I-***",
    "I-***",
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

fake_annot_tags_aligned = [
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
    "O",
]

fake_annot_tags_bk_boundary = [
    "O",
    "O",
    "O",
    "O",
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
]

fake_predict_tags_bk_boundary = [
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
]

fake_annot_tags_bk_boundary_2 = [
    "O",
    "O",
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
]

fake_predict_tags_bk_boundary_2 = [
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
]


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        (
            (
                "Gérard de -N-erval was bo-rn in Paris in 1808 -.",
                "G*rard de *N*erval ----bo*rn in Paris in 1833 *.",
                fake_annot_tags_aligned,
                fake_predict_tags_aligned,
                THRESHOLD,
            ),
            {ALL_ENTITIES: 1, "PER": 1, "LOC": 0, "DAT": 0},
        ),
        (
            (
                "Louis par la grâce de Dieu roy de France et de Navarre.",
                "Louis par la grâce de Dieu roy de France et de Navarre.",
                fake_tags_aligned_nested_perfect,
                fake_tags_aligned_nested_perfect,
                THRESHOLD,
            ),
            {ALL_ENTITIES: 3, "PER": 1, "LOC": 2},
        ),
        (
            (
                "Louis par la grâce de Dieu roy de France et de Navarre.",
                "Louis par la grâce de Dieu roy de France et de Navarre.",
                fake_tags_aligned_nested_perfect,
                fake_tags_aligned_nested_false,
                THRESHOLD,
            ),
            {ALL_ENTITIES: 2, "PER": 1, "LOC": 1},
        ),
        (
            (
                "The red dragon",
                "The red dragon",
                fake_annot_tags_bk_boundary,
                fake_predict_tags_bk_boundary,
                THRESHOLD,
            ),
            {ALL_ENTITIES: 0, "PER": 0},
        ),
        (
            (
                "A red dragon",
                "A red dragon",
                fake_annot_tags_bk_boundary_2,
                fake_predict_tags_bk_boundary_2,
                THRESHOLD,
            ),
            {ALL_ENTITIES: 1, "PER": 1},
        ),
    ],
)
def test_compute_matches(test_input, expected):
    assert evaluate.compute_matches(*test_input) == expected


def test_compute_matches_empty_entry():
    with pytest.raises(AssertionError):
        evaluate.compute_matches(None, None, None, None, None)
