# Models

This folder contains three models trained on the [drake](https://imgflip.com/meme/Drake-Hotline-Bling) dataset.

- `drake_imgflip`: model based on [this](https://github.com/dylanwenzlau/ml-scripts/tree/master/meme_text_gen_convnet) architecture. Use with `predict.py`
- `drake_textgenrnn`: textgenrnn model, trained from scratch. Use with `textgenrnn_predict.py`
- `drake_textgenrnn`: textgenrnn model, pretrained with Reddit submissions. Use `textgenrnn_predict.py` for prediction