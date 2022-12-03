import json
import matplotlib.pyplot as plt

with open('../tf_idf_data.json') as json_file:
    data = json.load(json_file)
wordlist = [str(word) for word in data.keys()]
top_words = wordlist[:20]
top_words.reverse()
scores = [data[word] for word in top_words]

plt.barh(top_words, scores)
plt.xlabel("TF-IDF Score")
plt.ylabel("Word")
plt.show()