# ImgFlip scraper

This package contains tools for scraping, augmenting and pre-processing memes from [imgflip](imgflip.com)

The code was developed and tested with Python 3.6

## Setup

1. Run `sh setup.sh` to retrieve the fasttext model (only needed for pre-processing)
2. Run `pip install -r requirements.txt`

## Usage

### Scraper

Use `scraper.py` to retrieve a dataset

```sh
scraper.py --source SOURCE [--from_page FROM_PAGE] --pages PAGES \
           --boxes BOXES [--delay DELAY] [--sort SORT]
```

The command line arguments are the following:

- `--source`: the page memes should be scraped from. You can see all imgflip meme templates [here](https://imgflip.com/memetemplates), pick one and copy the URL
- `--pages`: how many pages should be scraped?
- `--from_page`: initial page offset
- `--boxes`: the number of text boxes used for this meme template (click "Caption this meme") in the meme template's feed to see how many text boxes are used for it
- `--delay`: delay in seconds between scraping one page and the next
- `--sort`: if specified will append `&sort=SORT` to each scraped page

### Data augmentation

To run the data augmentation pipeline run

```sh
# For more options check augment.py
python augment.py --filename source.json --out destination.json
```

Only the augmented memes will be saved to `destination.json`

The input JSON file must be in the following format:

```json
{
    "memes": [
        {
            "text": "top; bottom;"
        }, ...
    ]
}
```

### Data pre-processing

To run the data pre-processing pipeline run

```sh
# For more options check preprocess.py
python preprocess.py --filename source.json --out destination.json
```

The pre-processing pipeline, inspired by [this repo](https://github.com/dylanwenzlau/ml-scripts/tree/master/meme_text_gen_convnet) does the following:

- Remove short and long memes, control the cutoffs with the following flags
  - `--min_length`: min meme length (default: 15)
  - `--max_length`: max meme length (default: 80)
- Removes memes not in English, using `fasttext`
  - `--fasttext_model`: path to fasttext model for language identification (default: `lid.176.bin`)
  - `--lang_detect_threshold`: treshold under which memes are considered not to be in English

This script accepts either a `--filename` argument or a `--folder`. In the latter case all files in the given folder will be preprocessed and consolidated in a single dataset.

The input JSON file must be in the following format:

```json
{
    "memes": [
        {
            "text": "top; bottom"
        }, ...
    ]
}
```

## Extras

### Convert JSON dataset to text

`json_to_txt.py` converts a JSON dataset to a a text file with one meme per line (useful for training `textgenrnn` models)

### Data analysis

`analyze.py` prints the number of instances in a dataset, the average length and displays an histogram of meme lengths

### Merge datasets

`merge.py` consolidates all datasets in a given folder to a single file