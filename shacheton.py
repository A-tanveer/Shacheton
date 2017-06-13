import os

from mitielib.mitie import *
import Shacheton.categorizer_trainer.train_naive_bayes_classyfier as nv


def clean_news(raw_news):
    """clean raw text"""
    return raw_news.replace('--', '').replace('*', '').replace('\n', '').replace('(', '').replace(')', '')


def categorize(cleaned_news):
    """returns categories of Bangla news"""
    _ret = ''
    relative_categories = ['robbery', 'mugging', 'murder', 'sexual harrasment', 'theft', 'road accident', 'drugs']
    classification = nv.newsClassifier.classify(cleaned_news)
    for cat in classification:
        if cat[1] > 0 and cat[0] in relative_categories:
            _ret += cat[0] + ', '
    return _ret


def extract_location(cleaned_news):
    """returns Entities found in first three lines of bangla news"""
    _ret = {}
    lines_in_news = cleaned_news.split('।')[0:2]  # using only the first 3 lines of the news
    for line in lines_in_news:
        tokens = line.split()
        entities_in_line = NER_MODEL.extract_entities(tokens)
        for entity in entities_in_line:
            range = entity[0]
            tag = entity[1]
            entity_text = ' '.join(tokens[word] for word in range)
            _ret.setdefault(tag, []).append(entity_text)

    return _ret


# create output file
out_dir = 'final output/output.txt'
if not os.path.exists(out_dir):
    try:
        os.makedirs(out_dir.split('/')[0])
    except OSError:
        print('something went wrong with creating file.')

# load Trained Model
print('Loading NER Model....')
NER_MODEL = named_entity_extractor('Bangla_ner_trained_model.dat')

_result = []

corpus_dir = os.getcwd() + "\data"

print('Processing Your Data.........\n[This may take some time.]')

# process every news of every file in data folder
for file in os.listdir(corpus_dir):
    # print(file)
    text = ''
    x = 0

    # f = open(os.path.join(corpus_dir, file), encoding='utf8')
    # f.close()
    with open(os.path.join(corpus_dir, file), encoding='utf8') as f:
        data = f.readlines()
    # print(len(data))

    for val in range(len(data)):
        if val % 9 == 7:

            _out = {}

            news = clean_news(data[val])

            classes = categorize(news)

            if len(classes) > 0:
                _out['news'] = news
                _out['class'] = classes
                _out['locations'] = extract_location(news)
                # print(extract_location(news))
                _result.append(_out)

# writing output to file
print("""Writing output to 'final output/output.txt'""")
with open(out_dir, 'w', encoding='utf8') as out_file:
    for dic in _result:
        # print(dic)
        out_file.write('news: ' + dic['news'] + '\n')
        out_file.write('categories:' + dic['class'] + '\n')
        loc = dic['locations']
        for key in loc:
            # ' '.join(tokens[word] for word in range)
            out_file.write(key + ': ' + ', '.join(token for token in loc[key]) + '\n')
        out_file.write('\n')

out_file.close()
print("All done!")
