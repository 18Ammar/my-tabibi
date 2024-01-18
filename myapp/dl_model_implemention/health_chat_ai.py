import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import json
import os
#prepare the dataset

filePath = "D:\\health_AI\\myapp\\dl_model_implemention\\dataset.json"

with open(filePath) as f:
    dataset = json.load(f)    

# set the question and answer lists
questionList = []
answerList = []
for entry in dataset:
    questionList.append(entry['question'])
    answerList.append(entry['answer'])

tokenizer = Tokenizer()
tokenizer.fit_on_texts(questionList+answerList)
question_seq = tokenizer.texts_to_sequences(questionList)
answer_seq = tokenizer.texts_to_sequences(answerList)
max_length = max(max(map(len,questionList)),max(map(len,answerList)))
question_padded = pad_sequences(question_seq,maxlen = max_length,padding = 'post')
answer_padded = pad_sequences(answer_seq,maxlen=max_length,padding = 'post')

print(question_padded)
