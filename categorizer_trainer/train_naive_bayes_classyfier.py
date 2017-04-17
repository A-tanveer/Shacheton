import os

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier


newsTrainer = Trainer(tokenizer)
# change to relative location to the file which is importing
trainer_dir = os.getcwd() + "\..\categorizer_trainer\\trainer_files"
print(os.getcwd())

for file in os.listdir(trainer_dir):

    f = open(os.path.join(trainer_dir, file), encoding='utf8')
    data = f.readlines()
    text = ''
    lineNo = 0
    counter = 0
    category = ''

    for line in data:

        if line == '\n':
            counter = 0
            category = ''
            text = ''
        else:
            counter += 1
            if counter == 2:
                text = line.replace('\n', '')
            elif counter > 2:
                category = line.replace('\n', '')
                newsTrainer.train(text, category)

        lineNo += 1

    f.close()

newsClassifier = Classifier(newsTrainer.data, tokenizer)
