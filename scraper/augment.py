import json
import argparse
import functools

import nlpaug.augmenter.word as naw
from spellchecker import SpellChecker

parser = argparse.ArgumentParser(description="RoBERTa based memes augmentation tool")

parser.add_argument("--out", required=True, help="Output filename", type=str)
parser.add_argument("--filename", required=True, help="JSON file to be processed", type=str)
parser.add_argument("--min_length", default=20, help="The minimum length of to be augmented texts", type=int)

args = parser.parse_args()

roberta = naw.ContextualWordEmbsAug(
    model_path="roberta-base",
    action="substitute")

with open(args.filename) as memes_file:
    memes = json.loads(memes_file.read())["memes"]

def is_augmentation_valid(augmented_text, boxes):
    """
        Verify that all boxes for a meme's text have length > 0
    """
    valid_boxes = functools.reduce(
            lambda x, y: x and y,
            [len(t) > 0 for t in augmented_text.split(";")[:2]])

    return augmented_text.count(";") == boxes and augmented_text[-1] == ";" and valid_boxes

def augment_meme_text(model, meme_text, attempts=2, boxes=2):
    """
        Attempt to augment a meme's text _attempts_ times.
        Returns the augmented text if successful, otherwise None
    """
    for _ in range(attempts):
        # Try augmenting the text three times if it does
        # not conform to the format we need
        augmented_text = model.augment(meme_text).lower().replace(" ;", ";").strip()

        # Sometimes the data augmentation forgets to add the last
        # trailing ";", so we appent it if that's the case
        if augmented_text[-1] != ";":
            augmented_text = f"{augmented_text};"

        if is_augmentation_valid(augmented_text, boxes):
            return augmented_text
    
    return None

def correct_spelling(text, spell_checker):
    """
        Corrects spelling errors in a given text
    """
    return " ".join([spell_checker.correction(w) if len(w) > 5 else w for w in text.split(" ")])

augmented_memes = []
spell_checker = SpellChecker()

for meme in memes:
    if len(meme['text']) < args.min_length:
        # Skip short memes
        continue

    augmented_text = augment_meme_text(
        roberta,
        meme["text"])

    if augmented_text is not None:
        augmented_memes.append({
            "text": augmented_text
        })

with open(args.out, "w") as out_file:
    out_file.write(json.dumps({
        "memes": augmented_memes
    }))
