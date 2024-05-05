import spacy
from spacy.tokens import Span
from spacy.matcher import Matcher
from pathlib import Path
import re


def LocationMatcher():
    # Exclude all but essencial pipelines to improve performance.
    exclude = [
        # 'ner',
        # 'morphologizer',
        # 'tok2vec',
        'tagger',
        'parser',
        'entity_linker',
        'entity_ruler',
        'textcat',
        'textcat_multilabel',
        'lemmatizer',
        'trainable_lemmatizer',
        'attribute_ruler',
        'senter',
        'sentencizer',
        'transformer',
    ]

    nlp = spacy.load('nl_core_news_lg', exclude=exclude)
    ruler = nlp.add_pipe('entity_ruler', before='ner')
    ruler.from_disk((Path(__file__).parent / "./rules").resolve())

    patterns = [
        ([
            {"TEXT": "oversteekplaats"},
            {"TEXT": "tussen"},
            {"TEXT": "de"},
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC", "ORG"]}, "OP": "+"},
            {"POS": {"IN": ["ADP", "DET", "NOUN", "CCONJ"]},
                "TEXT": {"NOT_IN": ["naar"]}, "OP": "+"},
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC"]}}
        ], 'LONGEST'),
        ([
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC", "ORG"]}, "OP": "+"},
            {"TEXT": "in"},
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC"]}}
        ], 'LONGEST'),
        ([
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC", "ORG"]}, "OP": "+"},
            {"TEXT": "wijk"},
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC"]}}
        ], 'LONGEST'),
        ([
            {"TEXT": "in"},
            {"TEXT": "de"},
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC", "ORG"]}, "OP": "+"},
        ], 'LONGEST'),
        ([
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC", "ORG"]}, "OP": "+"},
            {"POS": {"IN": ["ADP", "DET", "NOUN"]},
                "TEXT": {"NOT_IN": ["naar"]}, "OP": "+"},
            {"ENT_TYPE": {"IN": ["GPE", "FAC", "LOC"]}}
        ], 'LONGEST'),
        ([
            {"ENT_TYPE": "PERSON", "OP": "+"},
            {"POS": {"IN": ['ADP', "DET"]},  "OP": "+"},
            {"ENT_TYPE": "NORP"},
            {"POS": "NOUN"},
            {"POS": "PROPN"},
        ], 'LONGEST'),
        ([{"ENT_TYPE": "LOC", "OP": "+"}], 'FIRST'),
        ([{"ENT_TYPE": "GPE", "OP": "+"}], 'FIRST'),
    ]

    matcher = Matcher(nlp.vocab)

    for index, (pattern, greedy) in enumerate(patterns):
        matcher.add(f"pattern_{index}", [pattern], greedy=greedy)

    def location_matcher(text: str) -> list[Span]:
        doc = nlp(text)
        matches = matcher(doc, as_spans=True)
        matches.sort(key=lambda span: span.label_)
        matches = filter(lambda span: not re.match(
            ', [A-Z]', span.doc[span.end:span.end + 2].text), matches)
        matches = filter(lambda span: not span.text.startswith('-'), matches)
        matches = filter(lambda span: 'Comité' not in span.text, matches)
        matches = list(matches)

        return matches

    return location_matcher
