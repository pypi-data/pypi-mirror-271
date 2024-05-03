# Nerval, a python package for NER evaluation on noisy text

> Je suis l'autre
>
>  -- <cite>Gérard de Nerval</cite>

Nerval is an evaluation library written in python implementing a metric for named-entity recognition evaluation on noisy text, typically to measure NER performances on OCR or Handwritten text recognition predictions.

Expected inputs are a ground truth and a prediction BIOES/BILOU files without any  ''§'' occurrences, this character having a special meaning during evaluation.
It also works by designating a csv file with file matches (one pair per row with the annotation file in the first column and the prediction file in the second column)

## Usage

### Installation

After cloning the repository, install the package with:

```
$ cd nerval
$ pip3 install .
```

To run the tests and check that everything is fine:
```
$ pip3 install tox
$ tox
```

### Usage

You can now use Nerval in command line :

```
$ nerval -a/--annot <annot_file.bio> -p/--predict <predict-file.bio> \
		 [-t/--threshold <threshold_value>] [-c/--csv <correspondence_file.csv>]
```

The threshold value should be between 0 and 1. It designates the acceptable number of characters differing between an annotated and a predicted entity - over the number of characters in the annotated entity - to consider it as a match. Default value is 0.30. 0 would impose perfect matches, 1 would allow completely different strings to be considered as a match.

For instance, if we consider the following case:

| Annotation        | Prediction        |
| ----------------- | ----------------- |
| Hugone B-PERS     | Hugone B-PERS     |
| Montiniaci I-PERS | Montiniaci I-PERS |
| domino I-PERS     | domino O          |

Counting the spaces, 7 characters differ over 24 characters in the reference entity: a threshold of 0.30 would accept the match but a lower one would not.

### Demo

```
$ nerval -a demo/demo_annot.bio -p demo/demo_predict.bio
```

We also provide two annotation and prediction toy files, which are identical for now and produce perfect scores. Feel free to play with the the text and entity tags in the prediction file to see the impact on the score.

```
$ nerval -a demo/toy_test_annot.bio -p demo/toy_test_predict.bio
```

You can also indicate a folder and a csv file to have multiple evaluation at once.

```
$ nerval -c demo/mapping_file.csv -f demo
```

And with the verbose option that's triggered by -v

```
$ nerval -a demo/demo_annot.bio -p demo/demo_predict.bio -v
```

## Metric

This metric uses string alignment at character level.

The automatic transcription is first aligned with the ground truth at character level, by minimising the Levenshtein distance between them. Each entity in the ground truth is then matched with a corresponding entity in the aligned transcription, with the same entity label, or an empty character string if no match is found. If the edit distance between the two entities is less than 30% of the ground truth entity length, the predicted entity is considered as recognised. For the purpose of matching detected entities to existing databases, we estimated that a 70% match between the entity texts was a fair threshold.

**Nested entities -** Nerval makes an approximate evaluation of nested entities: containing entities and  nested entities will be evaluated separately. But note that in the BIOES/BILOU format, a nested entity at the end of a containing entity cannot be properly distinguished from a simple end and beginning of entity, hence the approximate evaluation. Therefore, in the following example, the detected and evaluated entities will be "Louis par la grâce de Dieu roy de France et de" (PER), "France" (LOC), "Navarre" (LOC).

```
Louis B-PER
par I-PER
la I-PER
grâce I-PER
de I-PER
Dieu I-PER
roy I-PER
de I-PER
France B-LOC
et I-PER
de I-PER
Navarre B-LOC
. O
```

#### Details

- From the bio files in input, retrieval of the text content and extension of a word-level tagging to a character-level tagging
    - spaces added between each word
    - spaces between two words with the same tag get the same tag, else O
    - information about beginning of entity is dropped

For instance, the following annotation file:

```
Tolkien B-PER
was O
a O
writer B-OCC
. O
```
produces the following list of tags, one per character plus spaces:

```
['B-PER','I-PER','I-PER','I-PER','I-PER','I-PER','I-PER',
 'O',
 'O', 'O', 'O',
 'O',
 'O',
 'O',
 'B-OCC','I-OCC','I-OCC','I-OCC','I-OCC','I-OCC',
 'O',
 'O']
```

And the prediction file could be:

```
Tolkieene B-PER
xas O
writear B-OCC
,. O
```

producing:

```
['B-PER','I-PER,'I-PER','I-PER','I-PER','I-PER','I-PER','I-PER','I-PER',
 'O',
 'O', 'O', 'O',
 'O',
 'B-OCC','I-OCC','I-OCC','I-OCC','I-OCC','I-OCC','I-OCC',
 'O',
 'O','O']
```

- Character level alignment between annotation and prediction adds '-' characters to both strings so they are the same length

With the following input texts :

```
annotation : Tolkien was a writer .
prediction : Tolkieen xas writear ,.
```

the alignment result is:

```
annotation : Tolkie-n- was a writer- -.
prediction : Tolkieene xas --writear ,.
```

- Adapt character-level tag to aligned strings
  - '-' characters in aligned strings get the same tag as the previous proper character in the string

```
             PPPPPPPPPOOOOOOOCCCCCCCOOO
annotation : Tolkie-n- was a writer- -.
prediction : Tolkieene xas --writear ,.
             PPPPPPPPPOOOOOOOCCCCCCCOOO
```
- Search for matching entity for each entity in the annotation
  - Inspecting the annotation character by character, when a new "B-" label is encountered, the character is the beginning of an entity to be matched.
  - Considering the opposite character in the prediction string, if the entity tags match on these two characters, tags are back-tracked in the prediction string to detect the beginning of the entity; that is, the first occurrence of said entity tag.
  - Else, if the entity tags don't match on the first character, beginning of matching entity in prediction is looked for until the end of the entity in the annotation.
  - Both for the annotation and the prediction, detected entities end with the last occurrence of the tag of their first character. At this point, the rest of the annotation and prediction are inspected to check for nested entities and collect the end of potential containing entity.

Here are examples of several situations with the delimitation of the matched entities in each case.

```
Matches delimitations are represented by ||

annotation : OOOOOOO|PPPPPPPPPPPPPPPPP|OOOOOO
prediction : OOOO|PPPPPPPPPPP|OOOOOOOOOOOOOOO

annotation : OOOOOOO|PPPPPPPPPPPPPPPPP|OOOOOO
prediction : OOOOOOOOOOOOOO|PPPPPPPPPPPPPP|OO

annotation : OOOOOOO|PPPPPPPPPPPPPPPPP|OOOOOO
prediction : OOOO|PPPPPPPPPPP|OOOOPPPPOOOOOOO

annotation : OOOOOOO|PPPPPPPPPPPPPPPPP|OOOOOO
prediction : OOOOOOO|P|OPPPPPPPPPPPPPPOOOOOOO

annotation : OOOOOOO|PPPPPP|LLL|PPPPPP|OOOOOO
prediction : OOOOOOO|PPPPPP|LLL|PPPPPP|OOOOOO

For this last example, "PPPPPPLLLPPPPPP" and "LLL" are evaluated separately.
```
- Get a score on the two matched strings :
  - Compute the Levenshtein distance between the two strings, ignoring the "-" characters
  - If edit_distance / length(annotation_entity) < 0.3, the entity is considered as recognised

```
edit_distance("Tolkien", "Tolkieene") = 2
len("Tolkien") = 7
2/7 = 0.29 < 0.3
OK

edit_distance("writer", "writear") = 1
len("writer") = 6
1/6 = 0.17 < 0.3
OK
```

- Final scores, Precision, Recall and F1-score, are given for each entity types, on entity-level. The total ("ALL") is a micro-average across entity types

```
PER :
P = 1/1
R = 1/1
F1 = 2*1*1/(1+1)

OCC :
P = 1/1
R = 1/1
F1 = 2*1*1/(1+1)

ALL :
P = 2/2
R = 2/2
F1 = 2*1*1/(1+1)
```

## Linting

We use [pre-commit](https://pre-commit.com/) to check the Python source code syntax of this project.

To be efficient, you should run pre-commit before committing (hence the name...).

To do that, run once :

```
pip install pre-commit
pre-commit install
```

The linting workflow will now run on modified files before committing, and may fix issues for you.

If you want to run the full workflow on all the files: `pre-commit run -a`.

## Citation

If you use this work, please cite us using this Bibtex citation:

```
@misc{nerval2021,
	title        = {Nerval: a python library for named-entity recognition evaluation on noisy texts},
	author       = {Miret, Blanche and Kermorvant, Christopher},
	year         = 2021,
	journal      = {GitLab repository},
	publisher    = {GitLab},
	howpublished = {\url{https://gitlab.teklia.com/ner/nerval}}
}
```
