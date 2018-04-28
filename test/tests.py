import unittest
from scripts import datasets
from scripts.embedding_layer import embedding
from unittest import mock


class Tests(unittest.TestCase):

    def test_datasets(self):
        path = "/Users/Colby/Code/Machine-Learning/Karmalutional-Network/data/news_first50.csv"
        train_test = datasets.get_sets(path)
        print("{}\n".format(train_test['X_train']))
        print("{}\n".format(train_test['X_test']))
        print("{}\n".format(train_test['Y_train']))
        print("{}".format(train_test['Y_test']))
        assert True

    def test_embeddings(self):
        embedding.gen_embedding_layer()
