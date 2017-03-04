import os

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.trainer import Trainer
from naiveBayesClassifier.classifier import Classifier

newstrainer = Trainer(tokenizer.Tokenizer(stop_words=[], signs_to_remove=["?!#%&"]))
trainer_dir = os.getcwd() + "\\trainer_files"

for file in os.listdir(trainer_dir):
    print(file)
    f = open(os.path.join(trainer_dir, file), encoding='utf8')
    data = f.readlines()
    text = ''
