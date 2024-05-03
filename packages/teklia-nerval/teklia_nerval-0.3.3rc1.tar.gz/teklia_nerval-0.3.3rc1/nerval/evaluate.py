import csv
import logging
from pathlib import Path
from typing import List

import editdistance
import edlib

from nerval.parse import (
    BEGINNING_POS,
    NOT_ENTITY_TAG,
    get_position_label,
    get_type_label,
    look_for_further_entity_part,
    parse_bio,
)
from nerval.utils import print_markdown_table, print_result_compact, print_results

logger = logging.getLogger(__name__)

ANNO_COLUMN = "Annotation"
PRED_COLUMN = "Prediction"
CSV_HEADER = [ANNO_COLUMN, PRED_COLUMN]


def compute_matches(
    annotation: str,
    prediction: str,
    labels_annot: list,
    labels_predict: list,
    threshold: int,
) -> dict:
    """Compute prediction score from annotation string to prediction string.

    Annotation and prediction strings should be the same length.

    For each entity in the annotation string, a match is found in the prediction.
    This is done in looking for a sub-string roughly at the same position in the prediction, and with the right entity-tag.
    Here is an example to illustrate the method used :

                     *-------*       *----*
    labels_annot   : PPPPPPPPPOOOOOOOCCCCCCOO
    annotation     : Tolkie-n- was a writer .
    prediction     : Tolkieene xas --writer .
    labels_predict : PPPPPPPPPOCCCCCCCCCCCCCC
                     *-------* <-----*----*->

    Each entity in the annotation string gets a prediction score based on the number
    of characters well predicted and labeled in the prediction string.
    The score of a label is the addition of entity scores divided by the number
    of entities.

    Inputs :
    annotation : str, example : "Tolkie-n- was a writer- -."
    prediction : str, example : "Tolkieene xas --writear ,."
    labels_annot : list of strings,   example : ['B-P','I-P','I-P','I-P','I-P','I-P','I-P','I-P','I-P','O', ...]
    labels_predict : list of string , example : ['B-P','I-P','I-P','I-P','I-P','I-P','I-P','I-P','I-P','O', ...]

    Output : {TAG1 : nb_entity_matched, ...}, example : {'All': 1, 'OCC': 0, 'PER': 1}
    """
    assert annotation, "Annotation is empty"
    assert prediction, "Prediction is empty"
    assert labels_annot, "Annotation labels are empty"
    assert labels_predict, "Prediction labels are empty"

    entity_count = {"All": 0}
    last_tag = NOT_ENTITY_TAG

    # Track indexes of characters found for continuation of nested entities
    visited_annot = []
    visited_predict = []

    # Iterating on reference string
    for i, char_annot in enumerate(annotation):
        if i in visited_annot:
            continue

        label_ref = labels_annot[i]
        tag_ref = get_type_label(label_ref)
        label_predict = labels_predict[i]
        tag_predict = get_type_label(label_predict)

        # If character not in entity
        if tag_ref == NOT_ENTITY_TAG:
            last_tag = NOT_ENTITY_TAG

        else:
            # If beginning new entity
            if get_position_label(label_ref) in BEGINNING_POS:
                current_ref, current_compar = [], []
                last_tag = tag_ref
                found_aligned_beginning = False
                found_aligned_end = False

            current_ref.append(char_annot)

            # Searching character string corresponding with tag
            if not found_aligned_end and tag_predict == tag_ref:
                if i in visited_predict:
                    continue

                # If just beginning new entity, backtrack tags on prediction string
                if (
                    len(current_ref) == 1
                    and get_position_label(labels_predict[i]) not in BEGINNING_POS
                ):
                    j = i - 1
                    while (
                        j >= 0
                        and get_type_label(labels_predict[j]) == tag_ref
                        and get_position_label(labels_predict[j]) not in BEGINNING_POS
                        and j not in visited_predict
                    ):
                        j -= 1

                    if (
                        get_position_label(labels_predict[j]) in BEGINNING_POS
                        and get_type_label(labels_predict[j]) == tag_ref
                        and j not in visited_predict
                    ):
                        start = j
                    else:
                        start = j + 1

                    current_compar += prediction[start:i]

                found_aligned_beginning = True
                current_compar.append(prediction[i])

            # If tags don't match and beginning was found : end of predicted entity
            elif found_aligned_beginning:
                found_aligned_end = True

            # If detect end of (1st part) entity in annotation: check for nested entity and compare
            if (i + 1 == len(annotation)) or (
                i + 1 < len(annotation)
                and get_type_label(labels_annot[i + 1]) != last_tag
            ):
                if not found_aligned_end:
                    rest_predict, visited = look_for_further_entity_part(
                        i + 1,
                        tag_ref,
                        prediction,
                        labels_predict,
                    )
                    current_compar += rest_predict
                    visited_predict += visited

                rest_annot, visited = look_for_further_entity_part(
                    i + 1,
                    tag_ref,
                    annotation,
                    labels_annot,
                )
                current_ref += rest_annot
                visited_annot += visited

                # Normalize collected strings
                entity_ref = "".join(current_ref)
                entity_ref = entity_ref.replace("-", "")
                len_entity = len(entity_ref)
                entity_compar = "".join(current_compar)
                entity_compar = entity_compar.replace("-", "")

                # One entity is counted as recognized (score of 1) if the Levenhstein distance between the expected and predicted entities
                # represents less than 30% (THRESHOLD) of the length of the expected entity.
                # Precision and recall will be computed for each category in comparing the numbers of recognized entities and expected entities
                score = (
                    1
                    if editdistance.eval(entity_ref, entity_compar) / len_entity
                    <= threshold
                    else 0
                )
                entity_count[last_tag] = entity_count.get(last_tag, 0) + score
                entity_count["All"] += score
                current_ref = []
                current_compar = []

    return entity_count


def get_labels_aligned(original: str, aligned: str, labels_original: list) -> list:
    """Takes original string, original string labels and aligned string given by edlib.align.
    Returns a list of labels corresponding to the aligned string.

    Input formats:
        original: str
        aligned: str with hyphens
        labels_original: list of labels ["O", "B-LOC", "I-LOC", ...]
    Output format :
        list of strings
    """
    assert original, "Original is empty"
    assert aligned, "Aligned is empty"
    assert labels_original, "Original labels are empty"

    labels_aligned = []
    index_original = 0
    last_label = NOT_ENTITY_TAG

    # Inspecting aligned string
    for i, char in enumerate(aligned):
        # new_label = ""

        # If original string has been fully processed, rest of labels are "O" ('-' characters at aligned end)
        if index_original >= len(original):
            new_label = NOT_ENTITY_TAG

        # If current aligned char does not match current original char ('-' characters in aligned)
        # Keep last_label and don't increment index_original
        elif not char == original[index_original]:
            new_label = (
                last_label
                if get_position_label(last_label) not in BEGINNING_POS
                else f"I-{get_type_label(last_label)}"
            )

        # Until matching of characters)
        else:
            new_label = labels_original[index_original]
            last_label = new_label
            index_original += 1

        labels_aligned.append(new_label)

    return labels_aligned


def compute_scores(
    annot_tags_count: dict,
    predict_tags_count: dict,
    matches: dict,
) -> dict:
    """Compute Precision, Recall and F1 score for all entity types found in annotation and prediction.

    Each measure is given at document level, global score is a micro-average over tag types.

    Inputs :
    annot :   { TAG1(str) : nb_entity(int), ...}
    predict : { TAG1(str) : nb_entity(int), ...}
    matches : { TAG1(str) : nb_entity_matched(int), ...}

    Output :
    scores : { TAG1(str) : {"P" : float, "R" : float, "F1" : float}, ... }
    """

    annot_tags = set(annot_tags_count.keys())
    predict_tags = set(predict_tags_count.keys())
    tags = annot_tags | predict_tags

    scores = {tag: {"P": None, "R": None, "F1": None} for tag in tags}

    for tag in sorted(tags)[::-1]:
        nb_predict = predict_tags_count.get(tag)
        nb_annot = annot_tags_count.get(tag)
        nb_match = matches.get(tag, 0)
        prec = None if not nb_predict else nb_match / nb_predict
        rec = None if not nb_annot else nb_match / nb_annot
        f1 = (
            None
            if (prec is None) or (rec is None)
            else 0
            if (prec + rec == 0)
            else 2 * (prec * rec) / (prec + rec)
        )

        scores[tag]["predicted"] = nb_predict
        scores[tag]["matched"] = nb_match
        scores[tag]["P"] = prec
        scores[tag]["R"] = rec
        scores[tag]["F1"] = f1
        scores[tag]["Support"] = nb_annot

    return scores


def evaluate(annotation: dict, prediction: dict, threshold: int) -> dict:
    # Align annotation and prediction
    align_result = edlib.align(annotation["words"], prediction["words"], task="path")
    nice_alignment = edlib.getNiceAlignment(
        align_result,
        annotation["words"],
        prediction["words"],
    )

    annot_aligned = nice_alignment["query_aligned"]
    predict_aligned = nice_alignment["target_aligned"]

    # Align labels from string alignment
    labels_annot_aligned = get_labels_aligned(
        annotation["words"],
        annot_aligned,
        annotation["labels"],
    )
    labels_predict_aligned = get_labels_aligned(
        prediction["words"],
        predict_aligned,
        prediction["labels"],
    )

    # Get nb match
    matches = compute_matches(
        annot_aligned,
        predict_aligned,
        labels_annot_aligned,
        labels_predict_aligned,
        threshold,
    )

    # Compute scores
    scores = compute_scores(
        annotation["entity_count"], prediction["entity_count"], matches
    )
    return scores


def run(annotation: Path, prediction: Path, threshold: int, verbose: bool) -> dict:
    """Compute recall and precision for each entity type found in annotation and/or prediction.

    Each measure is given at document level, global score is a micro-average across entity types.
    """

    # Get string and list of labels per character
    def read_file(path: Path) -> List[str]:
        assert path.exists(), f"Error: Input file {path} does not exist"
        return path.read_text().strip().splitlines()

    logger.info(f"Parsing file @ {annotation}")
    annot = parse_bio(read_file(annotation))

    logger.info(f"Parsing file @ {prediction}")
    predict = parse_bio(read_file(prediction))

    if not (annot and predict):
        raise Exception("No content found in annotation or prediction files.")

    scores = evaluate(annot, predict, threshold)

    # Print results
    if verbose:
        print_results(scores)
    else:
        print_result_compact(scores)

    return scores


def run_multiple(file_csv: Path, folder: Path, threshold: int, verbose: bool):
    """Run the program for multiple files (correlation indicated in the csv file)"""
    # Read the csv in a list
    with file_csv.open() as read_obj:
        csv_reader = csv.DictReader(read_obj)
        assert (
            csv_reader.fieldnames == CSV_HEADER
        ), f'Columns in the CSV mapping should be: {",".join(CSV_HEADER)}'
        list_cor = list(csv_reader)

    if not folder.is_dir():
        raise Exception("The path indicated does not lead to a folder.")

    list_bio_file = list(folder.rglob("*.bio"))

    count = 0
    precision = 0
    recall = 0
    f1 = 0
    for row in list_cor:
        annot = None
        predict = None

        for file in list_bio_file:
            if row[ANNO_COLUMN] == file.name:
                annot = file
        for file in list_bio_file:
            if row[PRED_COLUMN] == file.name:
                predict = file

        if not (annot and predict):
            raise Exception(
                f"No file found for files {row[ANNO_COLUMN]}, {row[PRED_COLUMN]}"
            )

        count += 1
        scores = run(annot, predict, threshold, verbose)
        precision += scores["All"]["P"]
        recall += scores["All"]["R"]
        f1 += scores["All"]["F1"]

    if not count:
        raise Exception("No file were counted")

    logger.info("Average score on all corpus")
    result = [
        round(precision / count, 3),
        round(recall / count, 3),
        round(f1 / count, 3),
    ]
    print_markdown_table(["Precision", "Recall", "F1"], [result])
