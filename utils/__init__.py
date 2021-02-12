import requests

from spellchecker import SpellChecker


def escape_meme_text(text):
  replacements = {
      " ": "_",
      "?": "~q",
      "%": "~p",
      "#": "~h",
      "/": "~s",
      "''": "\"",
  }

  for r in replacements.keys():
    text = text.replace(r, replacements[r])

  return text


def generate_meme(top_text, bottom_text, meme_type):
  top_text = escape_meme_text(top_text)
  bottom_text = escape_meme_text(bottom_text)
  url = f"https://memegen.link/{meme_type}/{top_text}/{bottom_text}.jpg"
  res = requests.get(url)

  return res.content


def correct_spelling(text):
    spell_checker = SpellChecker()
    return " ".join([spell_checker.correction(w) for w in text.split(" ")])
