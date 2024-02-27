import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Embedding, Input, Flatten,Bidirectional,Dropout
import numpy as np
import json
import string
import pandas as pd
import random

# Load dataset from JSON file
filePath = "D:\\health_AI\\myapp\\dl_model_implemention\\dataset.json"



def load_glove_embeddings(file_path, word_index, vocab_size, embedding_dim):
    embeddings_index = {}
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

    embedding_matrix = np.zeros((vocab_size, embedding_dim))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return embedding_matrix



with open(filePath) as f:
    dataset = json.load(f)

tags = []
questionList = []
answerList = {}

for intent in dataset["intents"]:
    answerList[intent['tag']] = intent['answer']
    for qu in intent['question']:
        questionList.append(qu)
        tags.append(intent['tag'])

# Create a DataFrame from the dataset
data = pd.DataFrame({"question": questionList, "tags": tags})

# Preprocess the text data
data['question'] = data['question'].apply(lambda wrd: [itrs.lower() for itrs in wrd if itrs not in string.punctuation])
data['question'] = data['question'].apply(lambda wrd: ''.join(wrd))

# Tokenize the text
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(data['question'])


x_train = pad_sequences(tokenizer.texts_to_sequences(data['question']))

# Use StringLookup to encode labels
tag_lookup = tf.keras.layers.StringLookup(vocabulary=np.unique(data['tags']), num_oov_indices=0, mask_token=None)

y_train = tag_lookup(data['tags'])

vocab_size = len(tokenizer.word_index) + 1
print("Number of unique words:", vocab_size)

output_len = len(np.unique(y_train))
print("Output length:", output_len)
embedding_matrix = load_glove_embeddings('D:\\health_AI\\myapp\\dl_model_implemention\\glove.6B.100d.txt', tokenizer.word_index, vocab_size, embedding_dim=100)

i = Input(shape=(x_train.shape[1],))
x = Embedding(vocab_size, 100, weights=[embedding_matrix], input_length=x_train.shape[1], trainable=False)(i)
x = Bidirectional(LSTM(20, return_sequences=True))(x)
x = Dropout(0.2)(x)
x = Flatten()(x)
x = Dense(output_len, activation="softmax")(x)
model = Model(i, x)
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])


history = model.fit(x_train, y_train,  epochs=10)
model.summary()

while True:
    text_p = []
    predicate_input = input("You: ")
    predicate_input = [letter.lower() for letter in predicate_input if letter not in string.punctuation]
    predicate_input = ''.join(predicate_input)
    text_p.append(predicate_input)

    # Tokenize the input
    predicate_input = tokenizer.texts_to_sequences(text_p)
    if not predicate_input:
        print("Bot: Please provide a valid input.")
        continue

    predicate_input = np.array(predicate_input).reshape(-1)
    predicate_input = pad_sequences([predicate_input], maxlen=x_train.shape[1])

    output = model.predict(predicate_input)
    output = np.argmax(output)

    # Convert the output to the corresponding string label
    answer_tag = tag_lookup.get_vocabulary()[output]
    
    respons = random.choice(answerList[answer_tag])

    print("Bot:", respons)
