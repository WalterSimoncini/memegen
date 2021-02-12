# Memegen

This repository contains code to train text generation models and use them to generate memes. The architectures used are `textgenrnn` and [this](https://github.com/dylanwenzlau/ml-scripts/tree/master/meme_text_gen_convnet)

The training code is in the jupyter notebooks meanwhile prediction is done with `textgenrnn_predict.py` (for textgenrnn) and `predict.py` (for the convolutional network).

Note that textgenrnn is trained via txt files and not via JSON files like the convolutional networks. The `json_to_txt.py` script in the `scraper` folder can be used to perform the conversion.

> **Disclaimer:** the generated memes will often have a poor quality and you may have to generate a large number of them to find "good" ones.

Sample outputs for the two models are in the `samples` folder

### Setup

Run `pip install -r requirements.txt`

## Meme generation (prediction)

The prediction scripts load a trained model, use it to generate text and create a meme using a template from [memegen.link](http://memegen.link). The template is specified via the `--template` flag for both prediction scripts. Check the link for the available templates!

The prediction scripts output `--count` images, to be saved in the folder specified by the `--out_folder` flag.

### Convolutional model

To generate new memes using one of the convolutional models run the following command:

```sh
python predict.py --model model.h5 --params params.json --count 2 --template drake --out_folder memes
```

The `--boxes` flag determines how many text boxes need to be generated for this template.

![](samples/convolutional/1.png)

### textgenrnn

To generate new memes using one of the textgenrnn models run the following command

```sh
python textgenrnn_predict.py --model model_folder --count 2 --template drake --out_folder memes --boxes 2
```

If you want to use one of the transfer learning models you need to add the flag `--load_only_weights y` to the command.

![](samples/textgenrnn/2.png)

### Miscellaneous

- The code was developed and tested with Python 3.6