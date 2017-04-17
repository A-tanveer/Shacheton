import os, random

from mitielib.mitie import *


print("loading NER model...")
ner = named_entity_extractor(os.path.dirname(__file__) + '/../Bangla_ner_trained_model.dat')
print('\nTags output by this NER model:', ner.get_possible_ner_tags())

corpus_dir = os.getcwd() + "\..\data"

for file in os.listdir(corpus_dir):
    print(file)
    f = open(os.path.join(corpus_dir, file), encoding='utf8')
    data = f.readlines()
    n = 0

    while n < 10:
        n += 1
        x = random.randint(0,10)
        try:
            news = data[x * 9 + 7].split('।')
            y = random.randint(0, 3)

            tokens = news[y].replace('\n', '').split()
            entities = ner.extract_entities(tokens)
            print(news[x])
            for eachEntitie in entities:
                range = eachEntitie[0]
                # print(range)
                tag = eachEntitie[1]
                entity_text = " ".join(tokens[i] for i in range)
                print(tag + ": " + entity_text)
        except IndexError:
            continue

