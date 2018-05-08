import unittest
from scripts import datasets
import os
import pathlib
import pickle

# made this to test (i.e print out) random things without messing with the code

class Tests(unittest.TestCase):

    def test_datasets(self):
        path = "/Users/Colby/Code/Machine-Learning/Karmalutional-Network/data/news_first50.csv"
        train_test = datasets.get_sets(path)
        # print("{}\n".format(train_test['X_train']))
        # print("{}\n".format(train_test['X_test']))
        # print("{}\n".format(train_test['Y_train']))
        # print("{}\n".format(train_test['Y_test']))
        print(train_test['X_train']['comment'][2])
        assert True



