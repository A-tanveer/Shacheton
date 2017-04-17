
import Shacheton.categorizer_trainer.train_naive_bayes_classyfier as nv
from pymongo import MongoClient
from Shacheton.cleaner import getDate
from mitielib.mitie import *


count = 0
client = MongoClient()
client.drop_database('shacheton')
db = client['shacheton']

print("loading NER model...")
ner = named_entity_extractor(os.path.dirname(__file__) + '/../Bangla_ner_trained_model.dat')

cates = ['robbery', 'mugging', 'murder', 'sexual harrasment', 'theft', 'road accedent', 'drugs']
corpus_dir = os.getcwd() + "\..\data"

for file in os.listdir(corpus_dir):
    print(file)
    f = open(os.path.join(corpus_dir, file), encoding='utf8')
    data = f.readlines()
    n = 0

    for lineNo in range(len(data)):
        print(n)
        n += 1
        if lineNo % 9 == 3:
            url = data[lineNo].replace('--', '').replace('*', '').replace('\n', '')
        elif lineNo % 9 == 5:
            title = data[lineNo].replace('--', '').replace('*', '').replace('\n', '')
        elif lineNo % 9 == 6:
            dateStr = data[lineNo].replace('--', '').replace('*', '').replace('\n', '')
        elif lineNo % 9 == 7:
            content = data[lineNo].replace('--', '').replace('*', '').replace('\n', '')
        if lineNo > 0 and lineNo % 9 == 0:
            newsdate = getDate.find_date(url, dateStr)
            # b = newsdate + datetime.timedelta(0,1,10)
            # print(newsdate)
            categories = []
            classification = nv.newsClassifier.classify(content)
            for cat in classification:
                if cat[1] > 0:
                    categories.append(cat[0])

            rem = []
            for cls in categories:
                if cls not in cates:
                    rem.append(cls)
            for x in rem:
                categories.remove(x)

            NER = {}
            if len(categories) > 0:
                lines = content.split('।')
                for line in lines:
                    tokens = line.replace('\n', '').replace('--', '').split()
                    entities = ner.extract_entities(tokens)
                    for eachEntitie in entities:
                        words = eachEntitie[0]
                        tag = eachEntitie[1]
                        entity_text = " ".join(tokens[i] for i in words)
                        NER[tag] = entity_text

                if newsdate:
                    news = {
                        "url": url,
                        "title": title,
                        'content': content,
                        'date': newsdate,
                        'categories': categories,
                        'namedEntitie': NER
                    }
                else:
                    news = {
                        "url": url,
                        "title": title,
                        'content': content,
                        'categories': categories,
                        'namedEntitie': NER
                    }
                news_db = db['news']
                news_id = news_db.insert_one(news)
                count += 1

            url = ''
            title = ''
            content = ''
            date = None
            categories = []
            NER = {}

print('\n\n\n', count)