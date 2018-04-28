import unittest
from scripts import datasets
import os
import pathlib
from scripts.embedding_layer import embedding
from unittest import mock

# made this to test (i.e print out) random things without messing with the code

class Tests(unittest.TestCase):

    def test_datasets(self):
        path = "/Users/Colby/Code/Machine-Learning/Karmalutional-Network/data/news_first50.csv"
        train_test, max_len = datasets.get_sets(path)
        print("{}\n".format(train_test['X_train']))
        print("{}\n".format(train_test['X_test']))
        print("{}\n".format(train_test['Y_train']))
        print("{}\n".format(train_test['Y_test']))
        print("Max_len {}\n".format(max_len))
        assert True


    def test_embeddings(self):
        path = os.path.dirname(os.path.abspath(__file__))
        path = str(pathlib.PurePath(path).parent)
        path += "/data/glove.42B.300d.txt"
        print(path)
