from tensorflow import keras
from scripts import datasets
from scripts.embedding_layer import embedding
import os


# def run_model_from_file_input():
#     # to be used in conjunction with get_input_df_with_labels in the case when the
#     # user wishes to specify a file in their cwd to read in for the file param
#     # in get_input_df_with_labels
#     file_name = input("enter name of file to read: ")
#     inputs = datasets.get_sets(os.getcwd() + '/' + file_name)
#     train_model(inputs, epocs=None, batch_size=None, lstm_dim=None, test=True)

def run_model_from_file(file):
    inputs = datasets.get_sets(file)
    train_model(inputs, epocs=32, batch_size=50, lstm_dim=128, test=True)


def create_model(input_shape, lstm_dim, embeddings):
    # Input pretrained Keras embeddings, builds Keras model
    inputs = keras.Input(shape=input_shape, dtype='int32')
    inputs = embeddings(inputs)
    X = keras.layers.LSTM(lstm_dim, return_sequences=False)(inputs)
    X = keras.layers.Activation('sigmoid')(X)

    model = keras.Model(inputs=inputs, outputs=X)
    print("model made\n")
    return model


def train_model(inputs, epocs, batch_size, lstm_dim, test):
    # Trains model and evaluates on test set if 'test' is true
    embeddings, longest = embedding.gen_embedding_layer()
    model = create_model((longest,), lstm_dim, embeddings)

    print("compiling and fitting\n")
    model.compile(loss='categoricalcrossentropy', optimizer='adam', metrics=['accuracy'])

    x_train_indices = embedding.comment_to_index(inputs['X_train'], max_len=100)
    model.fit(x_train_indices, inputs['Y_train'], epocs=epocs, batch_size=batch_size, shuffle=True)
    if test:
        x_test_indices = embedding.comment_to_index(inputs['X_test'], max_len=100)
        loss, acc = model.evaluate(inputs['X_test'], inputs['Y_test'])
        print(acc)


def main():
    run_model_from_file("/Users/Colby/Code/Machine-Learning/Karmalutional-Network/data/news_first50.csv")


if __name__ == "__main__":
    main()
