import Shacheton.categorizer_trainer.train_naive_bayes_classyfier as nv
import os

corpus_dir = os.getcwd() + "\data"
a = 0
for file in os.listdir(corpus_dir):
    # print(file)
    text = ''
    x = 0

    f = open(os.path.join(corpus_dir, file), encoding='utf8')
    data = f.readlines()
    # print(len(data))
    for val in range(len(data)):
        if val % 9 == 7:
            news = data[val].replace('--', '').replace('*', '').replace('\n', '')
            classification = nv.newsClassifier.classify(news)
            print('\n', news)
            for cat in classification:
                if cat[1] > 0:
                    print(cat[0], end='\t')

            lines = news.split('।')


            a += 1

print(a)