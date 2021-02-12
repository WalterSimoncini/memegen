import os
import json
import random
import argparse

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from utils import generate_meme, correct_spelling

parser = argparse.ArgumentParser(description="Meme generator")

parser.add_argument("--model", required=True, help="Path to the model file", type=str)
parser.add_argument("--params", required=True, help="Path to the model params file", type=str)
parser.add_argument("--template", required=True, help="Meme template name", type=str)
parser.add_argument("--count", default=1, help="Number of memes to generate", type=int)
parser.add_argument("--out_folder", default=".", help="Where the generated memes should be stored", type=str)

args = parser.parse_args()

def prefix_meme_text(intermediate_meme, template_id):
    box_index = str(intermediate_meme['text'].count(';'))    
    return f"{template_id} {box_index} {intermediate_meme['text']}"


def predict_next_character(labels, current_memes, texts, tokenizer, sequence_length=128):
    input_sequences = pad_sequences(
        tokenizer.texts_to_sequences(texts),
        maxlen=sequence_length)

    predictions_list = model.predict(input_sequences)
    sorted_predictions = []

    for i in range(0, len(predictions_list)):
        for j in range(0, len(predictions_list[i])):
            sorted_predictions.append({
                'text': current_memes[i]['text'],
                'next_char': labels[j],
                'score': predictions_list[i][j] * current_memes[i]['score']
            })

    return sorted(
        sorted_predictions,
        key=lambda p: p['score'],
        reverse=True)


def predict_meme_text(model, config, init_text="", threshold=0.1, maxlen=128, beam_width=1):
    tokenizer = Tokenizer(num_words=0, char_level=True)
    tokenizer.word_index = config['vocabulary']

    labels = {v: k for k, v in params['labels_vocabulary'].items()}

    current_memes = [{'text': init_text, 'score': 1}]
    completed_memes = []

    for char_count in range(len(init_text), maxlen):
        texts = [prefix_meme_text(m, config['template_id']) for m in current_memes]
        sorted_predictions = predict_next_character(
            labels,
            current_memes,
            texts,
            tokenizer,
            sequence_length=config['sequence_length'])

        top_score = sorted_predictions[0]['score']

        # Introduce randomization in the prediction choice
        iteration_threshold = (threshold + (1 - threshold) * random.random()) * top_score
        top_predictions = [p for p in sorted_predictions if p['score'] >= iteration_threshold]

        random.shuffle(top_predictions)

        current_memes = []

        for i in range(0, min(beam_width, len(top_predictions)) - len(completed_memes)):
            prediction = top_predictions[i]

            current_memes.append({
                'text': prediction['text'] + prediction['next_char'],
                # Normalize scores
                'score': prediction['score'] / top_score
            })

            if prediction['next_char'] == ';' and prediction['text'].count(';') == config["num_boxes"] - 1:
                completed_memes.append(current_memes[len(current_memes) - 1])
                current_memes.pop()

        if char_count >= maxlen - 1 or len(current_memes) == 0:
            # Return the meme with the highest score
            return sorted(
                current_memes + completed_memes,
                key=lambda p: p['score'],
                reverse=True)[0]['text']


model = load_model(args.model)
params = json.load(open(args.params))

params["num_boxes"] = 2
params["template_id"] = "1".zfill(8)

# Make sure the output folder exists and if not create it
os.makedirs(args.out_folder, exist_ok=True)

for meme_idx in range(args.count):
    top, bottom = [correct_spelling(text.strip()) for text in predict_meme_text(model, params, '')[:-1].split(";")]
    meme_image_data = generate_meme(top, bottom, args.template)

    with open(f"{args.out_folder}/meme_{meme_idx}.png", "wb") as out_image:
        out_image.write(meme_image_data)
