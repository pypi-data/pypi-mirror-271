from prettytable import MARKDOWN, PrettyTable


def print_markdown_table(header: list[str], rows: list[list]) -> None:
    """Prints a Markdown table filled with the provided header and rows."""
    table = PrettyTable()
    table.field_names = header
    table.set_style(MARKDOWN)
    table.add_rows(rows)
    print(table)


def print_results(scores: dict) -> None:
    """Display final results.

    None values are kept to indicate the absence of a certain tag in either annotation or prediction.
    """
    results = []
    for tag in sorted(scores, reverse=True):
        prec = None if scores[tag]["P"] is None else round(scores[tag]["P"], 3)
        rec = None if scores[tag]["R"] is None else round(scores[tag]["R"], 3)
        f1 = None if scores[tag]["F1"] is None else round(scores[tag]["F1"], 3)

        results.append(
            [
                tag,
                scores[tag]["predicted"],
                scores[tag]["matched"],
                prec,
                rec,
                f1,
                scores[tag]["Support"],
            ],
        )

    print_markdown_table(
        ["tag", "predicted", "matched", "Precision", "Recall", "F1", "Support"],
        results,
    )


def print_result_compact(scores: dict) -> None:
    result = [
        "All",
        scores["All"]["predicted"],
        scores["All"]["matched"],
        round(scores["All"]["P"], 3),
        round(scores["All"]["R"], 3),
        round(scores["All"]["F1"], 3),
        scores["All"]["Support"],
    ]
    print_markdown_table(
        ["tag", "predicted", "matched", "Precision", "Recall", "F1", "Support"],
        [result],
    )
