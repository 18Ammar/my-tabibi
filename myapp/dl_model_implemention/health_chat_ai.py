import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
import numpy as np
import json
import string

# Prepare the dataset
filePath = "D:\\health_AI\\myapp\\dl_model_implemention\\dataset.json"

with open(filePath) as f:
    dataset = json.load(f)

questionList = []
answerList = []
for entry in dataset:
    # Convert each question to lowercase
    questions = [question.lower() for question in entry['question']]
    questionList.append(questions)

    # Convert each answer to lowercase
    answers = [answer.lower() for answer in entry['answer']]
    answerList.append(answers)

# Tokenize the text
tokenizer = Tokenizer()
tokenizer.fit_on_texts([item for sublist in questionList + answerList for item in sublist])  # Flatten the lists
question_seq = tokenizer.texts_to_sequences(questionList)
answer_seq = tokenizer.texts_to_sequences(answerList)

# Here we need a fixed length, so we will use pad_sequences function to make it fixed length
max_length = max(max(map(len, question_seq)), max(map(len, answer_seq)))
question_padded = pad_sequences(question_seq, maxlen=max_length, padding='post')
answer_padded = pad_sequences(answer_seq, maxlen=max_length, padding='post')

X = question_padded
Y = answer_padded

# Define the model
model = Sequential()
vocab = len(tokenizer.word_index) + 1
embed_dim = 50  
model.add(Embedding(input_dim=vocab, output_dim=embed_dim, input_length=max_length, mask_zero=True))

units = 50  
model.add(LSTM(units, return_sequences=True))

model.add(Dense(vocab, activation="softmax"))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.summary()

# Start training the model
model.fit(X, Y, epochs=100)  

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
    predicate_input = pad_sequences([predicate_input], maxlen=max_length, padding='post')

       
    output = model.predict(predicate_input)

    print("output shape:", output.shape)
    print("output sum:", np.sum(output))
    output_flat = output.flatten()
    output_prob = output_flat / np.sum(output_flat)
    print("output_flat:", output_flat)
    print("output_prob:", output_prob)

    predicted_index = np.random.choice(len(output_flat), p=output_prob)
    predicted_word = tokenizer.index_word.get(predicted_index, 'unknown_word')

    print("Bot:", predicted_word)


