import pandas as pd
import numpy as np
from tensorflow import keras
from scripts import datasets
import os

def get_input_df_with_labels(file):
    # file is a file which has already been parsed by datasets.py to contain a csv
    # with the format ,comment,id,score.
    # the output return of this function is a DataFrame which represents the
    # same csv as the input, but with additional column at the end representing
    # the classified representation of the score using function get_single_classifier_for_score
    df = pd.read_csv(file)
    df = df.iloc[:, [1,3,2]] # order by comment,score,id (1,3,2)
    df['rank'] = df.score.apply(lambda score: get_single_classifier_for_score(score, df.score))
    print(df)
    return df


def get_single_classifier_for_score(score, all_scores, TOP = 90, GOOD = 75, NEUTRAL = 50, BAD = 35, TERRIBLE = 20):
    # scores is one score, all_scores is a series of all_scores
    # this function will return either 'top','good','neutral','bad', or 'terrible'
    # representation as a one-hot vector with a 1 in the place of the appropriate
    # classification from top...terrible,
    # dependent on whether or not the score is above the percentile threshold
    # specified by the input parameters TOP, GOOD, NEUTRAL, BAD, AND TERRIBLE.
    # there are placeholder values provided, however these parameters should be changed
    # to lower arbitrariness of the chosen values.
    #global iteration
    #iteration += 1
    if score > np.percentile(all_scores, TOP):
        print('top') #+ str(iteration))
        return [1,0,0,0,0]
    elif score > np.percentile(all_scores, GOOD):
        print('good')# + str(iteration))
        return [0,1,0,0,0]
    elif score > np.percentile(all_scores, NEUTRAL):
        print('neutral')# + str(iteration))
        return [0,0,1,0,0]
    elif score > np.percentile(all_scores, BAD):
        print('bad')# + str(iteration))
        return [0,0,0,1,0]
    else:
        print('terrible')# + str(iteration))
        return [0,0,0,0,1]

#iteration = 1

def train_test_sets(df, pct):
    train_index = df.shape[0] * pct

    train = df[:train_index]
    test = df[train_index:]

    X_train = train.iloc[:, [0]]
    X_test = test.iloc[:, [0]]

    Y_train = train.iloc[:, [1]]
    Y_test = test.iloc[:,[1]]

    x_y_train_test = {'X_train:': X_train, 'X_test': X_test, 'Y_train': Y_train, 'Y_test': Y_test}

    return x_y_train_test


def read_file_in_cwd_and_pass_to_get_input_df_with_labels():
    # to be used in conjunction with get_input_df_with_labels in the case when the
    # user wishes to specify a file in their cwd to read in for the file param
    # in get_input_df_with_labels
    file_name = input("enter name of file to read: ")
    df = get_input_df_with_labels(os.getcwd() + '/' + file_name)
    inputs = train_test_sets(df, 0.9)
    train_model(inputs, epocs=, batchsize=, lstm_dim=, test=True)


def create_model(input_shape, lstm_dim, embeddings):
    # Input pretrained Keras embeddings, builds Keras model
    inputs = keras.Input(shape=input_shape, dtype='int32')
    inputs = embeddings(inputs)
    X = keras.layers.LSTM(lstm_dim, return_sequences=False)(inputs)
    X = keras.layers.Activation('softmax')(X)

    model = keras.Model(inputs=inputs, outputs=X)
    return model


def train_model(inputs, epocs, batch_size, lstm_dim, test):
    # Trains model and evaluates on test set if 'test' is true
    embeddings = # FUNCTION TO GENERATE EMBEDDINGS

    model = create_model((longest,), lstm_dim, embeddings) # Longest =  longest word in vocabulary
    model.compile(loss='categoricalcrossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(inputs['X_train'], inputs['Y_train'], epocs=epocs, batch_size=batch_size, shuffle=True) # NEED TO SET UP TRAINING SETS
    if test:
        loss,acc = model.evaluate(inputs['X_test'], inputs['Y_test'])# NEED TO SET UP TEST SETS
        print(acc)

def main():
    read_file_in_cwd_and_pass_to_get_input_df_with_labels()

if __name__  == "__main__":
    main()
