import argparse
from pathlib import Path

from nerval.evaluate import run, run_multiple

THRESHOLD = 0.30


def threshold_float_type(arg):
    """Type function for argparse."""
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number.")
    if f < 0 or f > 1:
        raise argparse.ArgumentTypeError("Must be between 0 and 1.")
    return f


def parse_args():
    """Get arguments and run."""
    parser = argparse.ArgumentParser(description="Compute score of NER on predict.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-a",
        "--annot",
        help="Annotation in BIO format.",
        type=Path,
    )
    group.add_argument(
        "-c",
        "--csv",
        help="CSV with the correlation between the annotation bio files and the predict bio files",
        type=Path,
    )
    parser.add_argument(
        "-p",
        "--predict",
        help="Prediction in BIO format.",
        type=Path,
    )
    parser.add_argument(
        "-f",
        "--folder",
        help="Folder containing the bio files referred to in the csv file",
        type=Path,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Show a full recap on each NER label.",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        help="Set a distance threshold for the match between gold and predicted entity.",
        default=THRESHOLD,
        type=threshold_float_type,
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.annot:
        if not args.predict:
            raise argparse.ArgumentTypeError(
                "You need to specify the path to a predict file with -p",
            )
        run(args.annot, args.predict, args.threshold, args.verbose)
    elif args.csv:
        if not args.folder:
            raise argparse.ArgumentTypeError(
                "You need to specify the path to a folder of bio files with -f",
            )
        run_multiple(args.csv, args.folder, args.threshold, args.verbose)
    else:
        raise argparse.ArgumentTypeError(
            "You need to specify the argument of input file",
        )


if __name__ == "__main__":
    main()
