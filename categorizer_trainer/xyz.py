
f = open('trainer_files/categorizer_trainer.txt', encoding='utf8')

da = f.readlines()
count = 0
num_news_trained = 0

for line in da:

    try:
        x = da[count + 1]
    except IndexError:
        continue

    if x == '\n':
        num_news_trained += 1

    count += 1

print(num_news_trained)