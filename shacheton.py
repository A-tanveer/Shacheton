import Shacheton.categorizer_trainer.train_naive_bayes_classyfier as nv
import os

corpus_dir = os.getcwd() + "\data"
a = 0
cates = ['robbery', 'mugging', 'murder', 'sexual harrasment', 'theft', 'road accident', 'drugs']

for file in os.listdir(corpus_dir):
    # print(file)
    text = ''
    x = 0

    f = open(os.path.join(corpus_dir, file), encoding='utf8')
    data = f.readlines()
    # print(len(data))
    for val in range(len(data)):
        if val % 9 == 7:
            classes = []
            news = data[val].replace('--', '').replace('*', '').replace('\n', '')
            classification = nv.newsClassifier.classify(news)

            for cat in classification:
                if cat[1] > 0:
                    classes.append(cat[0])

            lines = news.split('।')

            print(classes)
            DEL = []
            for x in range(len(classes)):
                if classes[x] in cates:
                    continue
                else:
                    DEL.append(classes[x])
            for x in DEL:
                classes.remove(x)
            print(classes)
            print()

            a += 1

