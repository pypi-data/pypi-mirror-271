# augmolino

|||
|-|-|
|`augmolino` is a small data-augmentation python module for data science and neural networks with focus on audio. Its methods are very file-based and user friendly for simple mass-augmentation.|<img src="GRAPHICS/augmolino_logo.png" alt="logo" width="300"/>|


---

## First things first!

- This module is for `wav`-files only
- Data augmentation needs huge amounts of memory
- Use this module to expand your datasets

## Based on:

- [librosa](https://librosa.org/)
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)

## Usage:

- Create as many `augmentation` objects as you like. Here you specify the exact parameters of every augmentation
- Run them by passing them a source and destination file path.
- OR group them together in an `augmenter` which is like a pipeline for augmentations. YOu can add augmentations to the augmenter and point it to different files or folders. It has automatic naming capabilities and saves the files to disk or returns you the signals directly depending on your project style.