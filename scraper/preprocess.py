import os
import sys
import json
import argparse
import fasttext


parser = argparse.ArgumentParser(description="Merge scraper memes into a single document")

parser.add_argument("--out", required=True, help="Output filename", type=str)
parser.add_argument("--folder", default=None, help="Folder containing the scraped JSON files", type=str)
parser.add_argument("--filename", default=None, help="JSON file to be processed", type=str)
parser.add_argument("--lang_detect_threshold", default=0.35, help="Identification threshold for the English language", type=float)
parser.add_argument("--min_length", default=15, help="Minimum meme text length", type=str)
parser.add_argument("--max_length", default=80, help="Maximum meme text length", type=str)
parser.add_argument("--fasttext_model", default="lid.176.bin", help="fasttext model file", type=str)

args = parser.parse_args()

scan_folder = args.folder is not None
scan_file = args.filename is not None
lang_detection_model = fasttext.load_model(args.fasttext_model)

if (scan_folder and scan_file) or (not scan_folder and not scan_file):
    print("Specify either --folder or --filename, not both")
    sys.exit(0)

memes = []
memes_length = []
non_eng_memes_count = 0
memes_set = set()

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

if scan_folder:
    filenames = os.listdir(args.folder)
else:
    filenames = [args.filename]

for filename in filenames:
    file_path = f"{args.folder}/{filename}" if scan_folder else filename

    with open(file_path) as json_file:
        json_data = json.loads(json_file.read())

    for meme in json_data["memes"]:
        meme_text = meme['text'].lower().strip()

        if meme_text[-1] != ";":
            meme_text = f"{meme_text};"

        meme_text = meme_text.replace("\n", " ").strip()
        meme_length = len(meme_text)

        if meme_text in memes_set:
            # Skip memes that are already in the data set
            continue

        if not is_ascii(meme_text):
            # Skip non-ascii memes
            continue
        try:
            # Predict the top 3 languages
            lang_preds = lang_detection_model.predict(meme_text, k=3)
            lang_preds = list(zip(lang_preds[0], lang_preds[1]))

            # Convert predictions to a (lang, score) tuple and select
            # only the english score
            eng = list(filter(lambda x: "en" in x[0], lang_preds))

            # Discard non-english memes or memes below the accuracy
            # threshold
            if len(eng) == 0 or eng[0][1] < args.lang_detect_threshold:
                # Skip non-english memes ()
                non_eng_memes_count += 1
                continue
        except LangDetectException as _:
            # Skip memes whose language cannot be detected
            non_eng_memes_count += 1
            continue

        if meme_length < args.min_length or meme_length > args.max_length:
            # Skip memes which are either too short or too long
            continue

        memes.append({"text": meme_text})
        memes_set.add(meme_text)
        memes_length.append(meme_length)


with open(args.out, "w") as out_file:
    out_file.write(json.dumps({
        "memes": memes
    }))

print(f"Average meme length: {sum(memes_length) / len(memes_length)}")
print(f"Processed {len(memes)} memes")
print(f"Removed {non_eng_memes_count} non-english memes")
