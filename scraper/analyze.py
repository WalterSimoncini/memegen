import json
import argparse
import numpy as np
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description="Displays statistics for a given dataset")
parser.add_argument("--dataset", required=True, help="Memes dataset", type=str)

args = parser.parse_args()

with open(args.dataset) as dataset_file:
    dataset = json.loads(dataset_file.read())

memes = dataset['memes']
meme_lengths = np.array([len(m['text']) for m in memes])

print(f"Analyzing dataset: {args.dataset}\n")
print(f"Memes count: {len(memes)}")
print(f"Average meme length: {round(meme_lengths.mean(), 2)}")

fig, ax = plt.subplots()
n, bins, patches = ax.hist(meme_lengths, 10)

ax.set_xlabel("Counts")
ax.set_ylabel("Meme length")
ax.set_title("Meme length")

plt.show()
