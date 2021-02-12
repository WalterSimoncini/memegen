import os
import json
import argparse


parser = argparse.ArgumentParser(description="Merge JSON files in folder")
parser.add_argument("--folder", required=True, help="Folder with the memes dataset to be merged", type=str)
parser.add_argument("--out", required=True, help="Output filename", type=str)

args = parser.parse_args()

merged_memes = set()

for file in os.listdir(args.folder):
    with open(f"{args.folder}/{file}") as dataset_file:
        memes = [m['text'] for m in json.loads(dataset_file.read())['memes']]

    merged_memes.update(memes)

with open(args.out, "w") as out_file:
    out_memes = [{"text": m} for m in list(merged_memes)]

    out_file.write(json.dumps({
        "memes": out_memes
    }))
