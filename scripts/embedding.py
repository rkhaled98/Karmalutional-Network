# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FMS9XC6sJynUkubhJWUIMdAd2ZpegcvJ
"""

import numpy as np
import os
import pickle
from pathlib import Path
from tensorflow import keras
# from google.colab import files

# note: this causes the environment to crash and restart with such a huge file. for now, we are just using wget instead of Google Drive.
# wget is surprisingly fast for this task, possibly moreso than Google Drive would be.

# from documentation at https://colab.research.google.com/notebook#fileId=/v2/external/notebooks/io.ipynb&scrollTo=vz-jH8T_Uk2c:
# authenticate to access Google Drive using the REST API
# from google.colab import auth
# auth.authenticate_user()

# create a drive client:
# from googleapiclient.discovery import build
# drive_service = build('drive', 'v3')

# getting the glove file

import io
# from googleapiclient.http import MediaIoBaseDownload

# file_id = '18DZMqkgq5_nXgDEk9zc1HT7twmLuMEBk'
# request = drive_service.files().get_media(fileId = file_id)
# glove_downloaded = io.BytesIO()
# downloader = MediaIoBaseDownload(glove_downloaded, request)
#
# done = False
# while done is False:
#   _, done = downloader.next_chunk()
# glove_downloaded.seek(0)
#
# #download the glove word embedding from Stanford NLP:
# !wget http://nlp.stanford.edu/data/glove.42B.300d.zip
#
# !unzip glove.42B.300d.zip

# files = files.upload()
# Inspired by https://github.com/keras-team/keras/blob/master/examples/pretrained_word_embeddings.py
# and the Emojify exercise from Andrew Ng's course on sequence models
# word_to_index = {}
# word_to_vector = {}  # not to be confused with word2vec
word_to_idx = {}


def gen_embedding_matrix(file, input_shape, output_shape):
    embedding_matrix = np.zeros((input_shape, output_shape))
    with open(file) as f:
        print("gen embedding matrix\n")
        i = 0
        for line in f:
            split_line = line.split()
            word = split_line[0]
            weights = np.asarray(split_line[1:])
            word_to_idx[word] = i
            embedding_matrix[i, :] = weights
            i += 1
        word_to_idx["unk"] = i
        return embedding_matrix


def comment_to_index(comments, max_len):
    m = comments.shape[0]

    indices = np.zeros((m, max_len))

    for i in range(m):
        comment_words = comments['comment'][i].lower().split()
        j = 0
        for word in comment_words:
            try:
                indices[i, j] = word_to_idx[word]
            except (KeyError, IndexError):
                try:
                    indices[i, j] = word_to_idx["unk"]
                except IndexError:
                    continue
            j += 1

    return indices


# generates a Keras embedding layer, inspired by Emojify in Andrew Ng's Sequence Models Coursera course
def gen_embedding_layer():
    path = Path.cwd() / "data/glove.42B.300d.txt"
    # path = "/content/Karmalutional-Network/data/glove.42B.300d.txt" - for the notebook
    input_size = 1917496
    output_size = 300
    embedding_matrix = gen_embedding_matrix(path, input_size, output_size)
    print("gen embedding layer\n")
    layer = keras.layers.Embedding(input_size, output_size, trainable=False)
    layer.build((None,))
    layer.set_weights([embedding_matrix])
    return layer


