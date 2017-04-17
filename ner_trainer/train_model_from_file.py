from mitielib.mitie import *

trainer_dir = os.getcwd() + "/trainer_files"

trainer_model = ner_trainer("../../MITIE-models/bangla/total_word_feature_extractor.dat")

for file in os.listdir(trainer_dir):
    print(file)
    f = open(os.path.join(trainer_dir, file), encoding='utf8')
    data = f.readlines()
    text = ''
    var = False
    lineNo = 0

    for line in data:
        lineNo += 1

        if line == '\n':
            var = False
            try:
                trainer_model.add(sample)
            except Exception:
                print('something gone wrong!')
            continue

        if not var:
            var = True
            text = line.split()
            sample = ner_training_instance(text)
        else:
            try:
                ner_data = line.split()
                start_range = int(ner_data[0])
                # print("Error in data. Filename: ", file, "line No:", lineNo, "List index out of range!")
                end_range = int(ner_data[1]) + 1
                ner_tag = ner_data[2]

                sample.add_entity(xrange(start_range, end_range), ner_tag)
            except IndexError:
                print("Error in data. Filename: ", file, "line No:", lineNo, "List index out of range!")
                continue

    f.close()

trainer_model.num_threads = 4
ner = trainer_model.train()
ner.save_to_disk('new_trained_model.dat')

print("tags:", ner.get_possible_ner_tags())
f = open('test', encoding='utf8')
tokens = f.readline().split()
entities = ner.extract_entities(tokens)

print("\nEntities found:", entities)
print("\nNumber of entities detected:", len(entities))

for e in entities:
    range = e[0]
    tag = e[1]
    entity_text = " ".join(tokens[i] for i in range)
    print("    " + tag + ": " + entity_text)
