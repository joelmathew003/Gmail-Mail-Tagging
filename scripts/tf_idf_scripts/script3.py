import json
import operator
import nltk
import matplotlib.pyplot as plt
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
with open('tf_idf_data.json') as json_file:
    data = json.load(json_file)
wordlist = [str(word) for word in data.keys()]

print(data.type())
text=' '.join(wordlist).lower()
tokens = nltk.word_tokenize(text)
tags = nltk.pos_tag(tokens)
nouns = [word for word,pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
sorted_doc = (sorted(data.items(), key=operator.itemgetter(1)))[::-1]
with open("tf_idf_data","w") as f:
        for doc in sorted_doc:
            if not doc[0][0].isnumeric() and str(doc[0]) in nouns:
                f.write('\"'+str(doc[0])+"\":"+str(doc[1])+',\n')

