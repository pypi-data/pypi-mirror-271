import re
from typing import List

NOT_ENTITY_TAG = "O"
BEGINNING_POS = ["B", "S", "U"]

REGEX_IOB_LINE = re.compile(r"^(\S*) ((?:[BIESLU]-|O).*)$")
REGEX_LABEL = re.compile(r"[BIESLU]-(.*)$")


def get_type_label(label: str) -> str:
    """Return the type (tag) of a label

    Input format: "[BIESLU]-type"
    """
    try:
        tag = NOT_ENTITY_TAG if label == NOT_ENTITY_TAG else REGEX_LABEL.match(label)[1]
    except TypeError:
        raise (Exception(f"The label {label} is not valid in BIOES/BIOLU format."))

    return tag


def get_position_label(label: str) -> str:
    """Return the position of a label

    Input format: "[BIESLU]-type"
    """
    try:
        pos = (
            NOT_ENTITY_TAG
            if label == NOT_ENTITY_TAG
            else re.match(r"([BIESLU])-(.*)$", label)[1]
        )
    except TypeError:
        raise Exception(f"The label {label} is not valid in BIOES/BIOLU format.")

    return pos


def parse_line(index: int, line: str):
    try:
        match_iob = REGEX_IOB_LINE.search(line)

        assert match_iob, f"Line {line} does not match IOB regex"

        return match_iob.group(1, 2)
    except AssertionError:
        raise Exception(f"The file is not in BIO format: check line {index} ({line})")


def parse_bio(lines: List[str]) -> dict:
    """Parse a BIO file to get text content, character-level NE labels and entity types count.

    Input: lines of a valid BIO file
    Output format: { "words": str, "labels": list, "entity_count": { tag: int } }
    """
    words = []
    labels = []
    entity_count = {"All": 0}
    last_tag = None

    if "§" in " ".join(lines):
        raise (
            Exception(
                "§ found in input file. Since this character is used in a specific way during evaluation, please remove it from files."
            )
        )

    # Track nested entities infos
    in_nested_entity = False
    containing_tag = None

    for index, line in enumerate(lines):
        if not line:
            continue

        word, label = parse_line(index, line)

        # Preserve hyphens to avoid confusion with the hyphens added later during alignment
        word = word.replace("-", "§")
        words.append(word)

        tag = get_type_label(label)

        # Spaces will be added between words and have to get a label
        if index != 0:
            # If new word has same tag as previous, not new entity and in entity, continue entity
            if (
                last_tag == tag
                and get_position_label(label) not in BEGINNING_POS
                and tag != NOT_ENTITY_TAG
            ):
                labels.append(f"I-{last_tag}")

            # If new word begins a new entity of different type, check for nested entity to correctly tag the space
            elif (
                last_tag != tag
                and get_position_label(label) in BEGINNING_POS
                and tag != NOT_ENTITY_TAG
                and last_tag != NOT_ENTITY_TAG
            ):
                # Advance to next word with different label as current
                future_label = label
                while (
                    index < len(lines)
                    and future_label != NOT_ENTITY_TAG
                    and get_type_label(future_label) != last_tag
                ):
                    index += 1
                    if index < len(lines) and lines[index]:
                        future_label = lines[index].split()[1]

                # Check for continuation of the original entity
                if (
                    index < len(lines)
                    and get_position_label(future_label) not in BEGINNING_POS
                    and get_type_label(future_label) == last_tag
                ):
                    labels.append(f"I-{last_tag}")
                    in_nested_entity = True
                    containing_tag = last_tag
                else:
                    labels.append(NOT_ENTITY_TAG)
                    in_nested_entity = False

            elif in_nested_entity:
                labels.append(f"I-{containing_tag}")

            else:
                labels.append(NOT_ENTITY_TAG)
                in_nested_entity = False

        # Add a tag for each letter in the word
        if get_position_label(label) in BEGINNING_POS:
            labels += [f"B-{tag}"] + [f"I-{tag}"] * (len(word) - 1)
        else:
            labels += [label] * len(word)

        # Count nb entity for each type
        if get_position_label(label) in BEGINNING_POS:
            entity_count[tag] = entity_count.get(tag, 0) + 1
            entity_count["All"] += 1

        last_tag = tag

    result = None

    if words:
        result = {}
        result["words"] = " ".join(words)
        result["labels"] = labels
        result["entity_count"] = entity_count

        assert len(result["words"]) == len(
            result["labels"]
        ), f'Found {len(result["words"])} word(s) for {len(result["labels"])} label(s)'
        for tag in result["entity_count"]:
            if tag != "All":
                assert (
                    result["labels"].count(f"B-{tag}") == result["entity_count"][tag]
                ), f'Found {result["entity_count"][tag]} entities for {result["labels"].count(f"B-{tag}")} label(s) for entity {tag}'

    return result


def look_for_further_entity_part(index, tag, characters, labels):
    """Get further entities parts for long entities with nested entities.

    Input:
        index: the starting index to look for rest of entity (one after last character included)
        tag: the type of the entity investigated
        characters: the string of the annotation or prediction
        the labels associated with characters
    Output :
        complete string of the rest of the entity found
        visited: indexes of the characters used for this last entity part OF THE DESIGNATED TAG. Do not process again later
    """
    original_index = index
    last_loop_index = index
    research = True
    visited = []
    while research:
        while (
            index < len(characters)
            and labels[index] != NOT_ENTITY_TAG
            and get_type_label(labels[index]) != tag
        ):
            index += 1
        while (
            index < len(characters)
            and get_position_label(labels[index]) not in BEGINNING_POS
            and get_type_label(labels[index]) == tag
        ):
            visited.append(index)
            index += 1

        research = index != last_loop_index and get_type_label(labels[index - 1]) == tag
        last_loop_index = index

    characters_to_add = (
        characters[original_index:index]
        if get_type_label(labels[index - 1]) == tag
        else []
    )

    return characters_to_add, visited
