import os
import argparse

from textgenrnn import textgenrnn
from utils import generate_meme


parser = argparse.ArgumentParser(description="Meme generator (textgenrnn)")

parser.add_argument("--model", required=True, help="Path to the model folder (containing weights.hdf5, vocab.json and config.json)", type=str)
parser.add_argument("--count", default=1, help="Number of memes to generate", type=int)
parser.add_argument("--template", required=True, help="Meme template name", type=str)
parser.add_argument("--out_folder", default=".", help="Where the generated memes should be stored", type=str)
parser.add_argument("--boxes", required=True, help="Number of text boxes in the meme template", type=int)
parser.add_argument("--load_only_weights", default='n', help="Whether to use the default config and load only the weights or load vocabulary, weights and config [y/n]", type=str)

args = parser.parse_args()
args.load_only_weights = args.load_only_weights.lower() == "y"

if args.load_only_weights:
    textgen = textgenrnn(
        weights_path=f"{args.model}/weights.hdf5")
else:
    textgen = textgenrnn(
        weights_path=f"{args.model}/weights.hdf5",
        vocab_path=f"{args.model}/vocab.json",
        config_path=f"{args.model}/config.json")

# Make sure the output folder exists and if not create it
os.makedirs(args.out_folder, exist_ok=True)
generated_idx = 0

while generated_idx < args.count:
    sample = textgen.generate(
        n=1,
        return_as_list=True,
        temperature=0.5)[0]
    segments = [w.strip() for w in sample[:-1].split(";")]

    if len(segments) != args.boxes:
        continue

    top, bottom = segments
    meme_data = generate_meme(top, bottom, args.template)
    generated_idx += 1

    with open(f"{args.out_folder}/meme_{generated_idx}.png", "wb") as out_image:
        out_image.write(meme_data)
