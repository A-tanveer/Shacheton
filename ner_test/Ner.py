from mitielib.mitie import *
from collections import defaultdict


print("loading NER model...")
ner = named_entity_extractor(os.path.dirname(__file__) + '/../Bangla_ner_trained_model.dat')
print('\nTags output by this NER model:', ner.get_possible_ner_tags())

print('Tags: ', ner.get_possible_ner_tags())

for line in open('testText.txt', encoding='utf8'):
    print('\n', line.replace('\n', ''))
    tokens = line.replace('\n', '').split()
    entities = ner.extract_entities(tokens)

    for eachEntitie in entities:
        range = eachEntitie[0]
        # print(range)
        tag = eachEntitie[1]
        entity_text = " ".join(tokens[i] for i in range)
        print(tag + ": " + entity_text)

