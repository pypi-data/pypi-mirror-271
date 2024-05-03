import edlib
import pytest


@pytest.mark.parametrize(
    ("query", "target"),
    [
        (
            "Gérard de Nerval was born in Paris in 1808 .",
            "G*rard de *N*erval bo*rn in Paris in 1833 *.",
        ),
    ],
)
def test_align(query, target):
    a = edlib.align(query, target, task="path")
    result_alignment = edlib.getNiceAlignment(a, query, target)
    assert result_alignment == {
        "query_aligned": "Gérard de -N-erval was bo-rn in Paris in 1808 -.",
        "matched_aligned": "|.||||||||-|-||||||----||-|||||||||||||||||..|-|",
        "target_aligned": "G*rard de *N*erval ----bo*rn in Paris in 1833 *.",
    }
