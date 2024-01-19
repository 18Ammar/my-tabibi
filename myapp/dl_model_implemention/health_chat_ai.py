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
filePath = "D:\\health_AI\\myapp\\dl_model_implemention\\dataset.json"

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
tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['question']) 

train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

x_train = pad_sequences(tokenizer.texts_to_sequences(train_data['question']))
x_val = pad_sequences(tokenizer.texts_to_sequences(val_data['question']))

y_train = le.transform(train_data['tags'])
y_val = le.transform(val_data['tags'])

vocab_size = len(tokenizer.word_index) + 1
print("Number of unique words:", vocab_size)

output_len = len(np.unique(y_train))
print("Output length:", output_len)

train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

x_train = pad_sequences(tokenizer.texts_to_sequences(train_data['question']))
x_val = pad_sequences(tokenizer.texts_to_sequences(val_data['question']))

y_val = le.transform(val_data['tags'])

# Define the model
i = Input(shape=(x_train.shape[1],))
x = Embedding(vocab_size, 10)(i)
x = LSTM(10, return_sequences=True)(x)
x = Flatten()(x)
x = Dense(output_len, activation="softmax")(x)
model = Model(i, x)

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
history = model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=200)

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
