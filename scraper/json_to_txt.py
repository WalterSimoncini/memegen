import json
import argparse


parser = argparse.ArgumentParser(description="Converts a memes JSON dataset to a txt file")
parser.add_argument("--filename", required=True, help="JSON file to be processed", type=str)
parser.add_argument("--out", required=True, help="Output file path", type=str)

args = parser.parse_args()

with open(args.filename) as json_file:
    memes = json.loads(json_file.read())['memes']

output_text = ""

for meme in memes:
    output_text += f"{meme['text']}\n"

with open(args.out, "w") as out_file:
    out_file.write(output_text)
