# from symbol import term
import matplotlib.pyplot as plt
import numpy as np
import os
import operator
from nltk.corpus import stopwords
import gensim
from gensim import corpora, models
# from textblob import TextBlob
from bs4 import BeautifulSoup
import pyLDAvis.gensim_models as gensimvis
import pickle 
import pyLDAvis

def main():
    word_freq("mail_bodies_small.txt")

def filter_nouns(wordlist):
    text=' '.join(wordlist).lower()
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    nouns = [word for word,pos in tags if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    return nouns

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
            doc_words[-1] = filter_nouns(doc_words[-1])
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
            msg_line_count+=1
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

    dictionary = corpora.Dictionary(doc_words)
    corpus = [dictionary.doc2bow(text) for text in doc_words]
    num_topics = 20
    passes = 20
    lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topics, id2word = dictionary, passes = passes)
    print(lda_model.print_topics(num_topics = 10, num_words = 10))
    # Visualize the topics
    # pyLDAvis.enable_notebook()
    LDAvis_data_filepath = os.path.join('./results/ldavis_prepared_'+str(num_topics))
    # # this is a bit time consuming - make the if statement True
    # # if you want to execute visualization prep yourself
    if 1 == 1:
        LDAvis_prepared = gensimvis.prepare(lda_model, corpus, dictionary)
        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)
    # load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)
    pyLDAvis.save_html(LDAvis_prepared, './results/ldavis_prepared_'+ str(num_topics) +'.html')
    pyLDAvis.display(LDAvis_prepared)
    

if __name__ == "__main__":
    main()