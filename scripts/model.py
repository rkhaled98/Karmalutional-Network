from tensorflow import keras
import datasets
import embedding
import os
import pathlib


# def run_model_from_file_input():
#     # to be used in conjunction with get_input_df_with_labels in the case when the
#     # user wishes to specify a file in their cwd to read in for the file param
#     # in get_input_df_with_labels
#     file_name = input("enter name of file to read: ")
#     inputs = datasets.get_sets(os.getcwd() + '/' + file_name)
#     train_model(inputs, epocs=None, batch_size=None, lstm_dim=None, test=True)

def run_model_from_file(file):
    inputs = datasets.get_sets_from_out(file)
    train_model(inputs, epocs=32, batch_size=50, lstm_dim=128, test=True)


def create_model(lstm_dim, embeddings):
    # Input pretrained Keras embeddings, builds Keras model
    print("Model Starting\n")
    inputs = keras.Input(shape=(50,), dtype='int32')
    embeddings = embeddings(inputs)
    X = keras.layers.LSTM(lstm_dim, return_sequences=False)(embeddings)
    X = keras.layers.Activation('sigmoid')(X)

    model = keras.Model(inputs=inputs, outputs=X)
    model.summary()
    return model


def train_model(inputs, epocs, batch_size, lstm_dim, test):
    # Trains model and evaluates on test set if 'test' is true
    print("trian model starting\n")
    embeddings = embedding.gen_embedding_layer()
    model = create_model(lstm_dim, embeddings)

    print("compiling and fitting\n")
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    x_train_indices = embedding.comment_to_index(inputs['X_train'], max_len=100)
    model.fit(x_train_indices, inputs['Y_train'], epocs=epocs, batch_size=batch_size, shuffle=True)
    if test:
        x_test_indices = embedding.comment_to_index(inputs['X_test'], max_len=100)
        loss, acc = model.evaluate(x_test_indices, inputs['Y_test'])
        print(acc)


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    path = str(pathlib.PurePath(path).parent)
    path += "/data/news_news.out"
    run_model_from_file(path)


if __name__ == "__main__":
    main()
