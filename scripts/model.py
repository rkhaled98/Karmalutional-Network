from tensorflow import keras
from scripts import datasets
import os


def run_model_from_file_input():
    # to be used in conjunction with get_input_df_with_labels in the case when the
    # user wishes to specify a file in their cwd to read in for the file param
    # in get_input_df_with_labels
    file_name = input("enter name of file to read: ")
    inputs = datasets.get_sets(os.getcwd() + '/' + file_name)
    train_model(inputs, epocs=None, batch_size=None, lstm_dim=None, test=True)


def create_model(input_shape, lstm_dim, embeddings):
    # Input pretrained Keras embeddings, builds Keras model
    inputs = keras.Input(shape=input_shape, dtype='int32')
    inputs = embeddings(inputs)
    X = keras.layers.LSTM(lstm_dim, return_sequences=False)(inputs)
    X = keras.layers.Activation('sigmoid')(X)

    model = keras.Model(inputs=inputs, outputs=X)
    return model


def train_model(inputs, epocs, batch_size, lstm_dim, test):
    # Trains model and evaluates on test set if 'test' is true
    embeddings = None# FUNCTION TO GENERATE EMBEDDINGS

    model = create_model((longest,), lstm_dim, embeddings) # Longest =  longest word in vocabulary
    model.compile(loss='categoricalcrossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(inputs['X_train'], inputs['Y_train'], epocs=epocs, batch_size=batch_size, shuffle=True) # NEED TO SET UP TRAINING SETS
    if test:
        loss,acc = model.evaluate(inputs['X_test'], inputs['Y_test'])# NEED TO SET UP TEST SETS
        print(acc)


def main():
    run_model_from_file_input()


if __name__  == "__main__":
    main()
