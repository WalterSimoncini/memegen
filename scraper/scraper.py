"""
imgflip.com scraper

This script scrapes memes from a category on imgflip.com
(e.g. https://imgflip.com/meme/Bird-Box). As an example,
to scrape the first 10 pages of Drake memes run:

python scraper.py --source https://imgflip.com/meme/Drake-Hotline-Bling --pages 10 --boxes 2

--boxes is set to 2 based on the imgflip template available at:

https://imgflip.com/memegenerator/Drake-Hotline-Bling
"""

import time
import json
import argparse
import requests

from tqdm import tqdm
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description="Scrape memes from imgflip.com")
parser.add_argument("--source", required=True, help="Memes list url (e.g. https://imgflip.com/meme/Bird-Box)", type=str)
parser.add_argument("--from_page", default=1, help="Initial page", type=int)
parser.add_argument("--pages", required=True, help="Maximum page number to be scraped", type=int)
parser.add_argument("--boxes", required=True, help="The standard number of text boxes for this meme", type=int)
parser.add_argument("--delay", default=2, help="Delay between page loads (seconds)", type=int)
parser.add_argument("--sort", default=None, help="Optional page sorting key", type=str)

args = parser.parse_args()

fetched_memes = []

meme_name = args.source.split("/")[-1].replace("-", " ")
output_filename = args.source.split("/")[-1].replace("-", "_").lower() + ".json"

for i in tqdm(range(args.from_page, args.pages + 1)):
    # Append the sort key if needed
    if args.sort is not None:
        page_url = f"{args.source}?page={i}&sort={args.sort}"
    else:
        page_url = f"{args.source}?page={i}"

    response = requests.get(page_url)
    body = BeautifulSoup(response.text, 'html.parser')

    if response.status_code != 200:
        # Something went wrong (e.g. page limit)
        print(f"Something went wrong: {response.text} (status: {response.status_code})")
        break

    # Retrieve all meme divs in the page
    memes = body.findAll("div", {"class": "base-unit clearfix"})

    if len(memes) == 0:
        # We reached the last page with data
        print("End of results reached")
        break

    for meme in memes:
        # Extract each meme in the page
        if "not-safe-for-work images" in str(meme):
            # NSFW memes are available only to logged in users, skip them
            continue

        meme_text = meme.find("img", {"class": "base-img"})["alt"]
        meme_text = meme_text.split("|")[1].strip()

        rows = meme_text.split(";")

        if (len(rows) != args.boxes):
            # Skip memes with more boxes than expected, images, etc
            continue

        meme_data = {
            "url": meme.find("img", {"class": "base-img"})["src"][2:],
            "text": meme_text
        }

        fetched_memes.append(meme_data)

    time.sleep(args.delay)

print(f"Fetched: {len(fetched_memes)} memes")

with open(output_filename, "w") as out_file:
    data = {
        "name": meme_name,
        "memes": fetched_memes
    }

    out_file.write(json.dumps(data))
