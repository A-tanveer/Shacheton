
f = open('sample_trainer_.txt', encoding='utf8')

text = f.readlines()
f.close()
x = 0
f = open('testText.txt', 'w', encoding='utf8')
for line in text:
    if line == '\n':
        x = 1
        continue
    if x == 1:
        x = 0
        f.write(line)

f.close()

