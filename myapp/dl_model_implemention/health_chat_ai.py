import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, LSTM, Embedding, Input, Flatten
import numpy as np
import json
import string
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import random

# Prepare the dataset
filePath = "content.josn"

# Load dataset from JSON file
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

# Create a DataFrame from Data set
data = pd.DataFrame({"question": questionList, "tags": tags})

# Preprocess the text data
data['question'] = data['question'].apply(lambda wrd: [itrs.lower() for itrs in wrd if itrs not in string.punctuation])
data['question'] = data['question'].apply(lambda wrd: ''.join(wrd))

# Tokenize the text 
tokenizer = Tokenizer(num_words=1000)
tokenizer.fit_on_texts(data['question'])
train = tokenizer.texts_to_sequences(data['question'])
x_train = pad_sequences(train)

#use LabelEncoder to Encode the tags
le = LabelEncoder()
y_train = le.fit_transform(data['tags'])
 
model = Sequential()

vocab = len(tokenizer.word_index) + 1
embed_dim = 10
model.add(Embedding(input_dim=vocab, output_dim=embed_dim, input_length=x_train.shape[1]))

units = 10
model.add(LSTM(units, return_sequences=True))

model.add(Flatten())

output_len = le.classes_.shape[0]
model.add(Dense(output_len, activation="softmax"))

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.summary()

# strat Train the model
model.fit(x_train, y_train, epochs=200)

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
    
    answer_tag = le.inverse_transform([output])[0]
    
    respons = random.choice(answerList[answer_tag])
    
    print("Bot:", respons)
