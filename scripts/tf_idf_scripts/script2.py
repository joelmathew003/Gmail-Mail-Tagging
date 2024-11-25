# from symbol import term
import matplotlib.pyplot as plt
import numpy as np
import sys
import operator
import argparse
from nltk.corpus import stopwords
import gensim
from gensim import corpora, models
# from textblob import TextBlob
from bs4 import BeautifulSoup
import pickle 

def main():
    word_freq("mail_bodies_small.txt")


def word_freq(filename):
    doc = {}
    doc_words = [[]]
    termdf = {}
    msg_doc = {}
    no_of_docs = 0
    msg_line_count = 0
    for line in open(filename, encoding="utf-8"):
        line = line.strip()
        if(line == "*****************************************************"):
            # if(msg_line_count<3):
            #     msg_doc.clear()
            #     msg_line_count = 0
            #     continue
            doc_words.append([])
            msg_line_count = 0
            no_of_docs += 1
            for term in msg_doc:
                if (doc.__contains__(term)):
                    doc[term] = int(doc.get(term)) + msg_doc[term]
                else:
                    doc[term] = 1
            msg_doc.clear()
        else:
            # if(line[0] != '>'):
            msg_line_count+=1
            # line = BeautifulSoup(line).get_text()
            split = line.split(' ')
            for entry in split:
                entry = entry.lower()
                if(entry in stopwords.words('english') or (not entry.isalnum()) or len(entry)<=2):
                    continue
                doc_words[-1].append(entry)
                if (msg_doc.__contains__(entry)):
                    msg_doc[entry] = int(msg_doc.get(entry)) + 1
                else:
                    msg_doc[entry] = 1
                    if(termdf.__contains__(entry)):
                        termdf[entry] = int(termdf.get(entry)) + 1
                    else:
                        termdf[entry] = 1

    tfidf = {}
    for term in doc:
        tfidf[term] = doc[term] * np.log(no_of_docs/termdf[term])

    sorted_doc = (sorted(tfidf.items(), key=operator.itemgetter(1)))[::-1]
    print("num docs", no_of_docs)
    # print(sorted_doc)
    top = []
    topfreq = []
    for i in range(min(len(sorted_doc), 40)):
        entry = sorted_doc[i]
        top.append(entry[0])
        topfreq.append(entry[1])

    # with open("tf_idf_data.json","w",encoding="utf-8") as f:
    #     for doc in sorted_doc:
    #         if not doc[0][0].isnumeric():
    #             print(str(doc[0])+":"+str(doc[1])+',\n', file = f)

    # words = [doc[0] for doc in sorted_doc]
    # print(doc_words)
    # dictionary = corpora.Dictionary(doc_words)
    # corpus = [dictionary.doc2bow(text) for text in doc_words]
    # ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 20, id2word = dictionary, passes = 20)
    # print(ldamodel.print_topics(num_topics = 10, num_words = 10))

    # with open("words","w") as f:
    #     f.write(sorted_doc.keys())
    # plt.barh(y, x)
    plt.barh(top, topfreq)
    plt.xlabel("Frequency")
    plt.ylabel("Word")
    plt.show()

    

if __name__ == "__main__":
    main()