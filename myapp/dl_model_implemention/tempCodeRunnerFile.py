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
    questions = [question.lower() for question in entry['question']]
    questionList.append(questions)

    # Convert each answer to lowercase
    answers = [answer.lower() for answer in entry['answer']]
    answerList.append(answers)

print(questionList, answerList)
