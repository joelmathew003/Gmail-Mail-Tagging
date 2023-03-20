# -*- coding: utf-8 -*-
"""LDA_eval.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UvJJVTWxswmKTjZ2MQqXN6Z-ua3_Eytp
"""

from google.colab import drive
drive.mount('/content/drive')

test = []
for i in range(1, 101):
  filename = "/content/drive/MyDrive/BTP stuff/BTP_TestSet_Mails/test" + str(i) + ".txt"
  with open(filename, "r") as f:
    text = f.read().strip().lower().replace('\n', '')
    test.append(text)

import pandas as pd

test_data_path = "/content/drive/MyDrive/BTP stuff/GoldSet_BTP - Sheet1.csv"
data = pd.read_csv(test_data_path)
data['Tags'] = data['Tags'].str.replace(" ", "")

data

import urllib.request
urllib.request.urlretrieve('https://nlp.stanford.edu/data/glove.6B.zip','glove.6B.zip')

!unzip "/content/glove.6B.zip" -d "/content/"

import numpy as np
from scipy.spatial.distance import cosine
from gensim.models import KeyedVectors
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from numpy.linalg import norm
import tensorflow as tf
import torch
import torchtext

#@title Evaluation Class
class MailTester:
  def __init__(self, test_mails, test_data, model):
    self.test_mails = test_mails
    self.model = model
    self.test_data = test_data
  
  def test(self):
    correct_predictions = 0
    total_predictions = 0

    for index, row in self.test_data.iterrows():
        mail_body = self.test_mails[index]
        expected_tags = set(row['Tags'].split(','))
        predicted_tags = set(model_prediction(mail_body))#set(self.model.predict(mail_body))
        common_tags = set(expected_tags).intersection(predicted_tags)
        if len(common_tags) > 0:
          correct_predictions += 1
        total_predictions += 1

    accuracy = correct_predictions / total_predictions
    print(f"Accuracy: {accuracy}")
  
  def find_similar(self, list1, list2):
    glove_model = torchtext.vocab.GloVe(name="6B", dim=200)
    threshold = 0.9
    similar_words = []
    for word1 in list1:
        for word2 in list2:
            distance = cosine(glove_model[word1], glove_model[word2])
            if distance > threshold:
                similar_words.append((word1, word2))
    return similar_words

  def test_sim(self):
    correct_predictions = 0
    total_predictions = 0
    for index, row in self.test_data.iterrows():
        mail_body = self.test_mails[index]
        expected_tags = set(row['Tags'].split(','))
        predicted_tags = set(model_prediction(mail_body))
        common_tags = self.find_similar(expected_tags, predicted_tags)
        if len(common_tags) > 0:
          correct_predictions += 1
        total_predictions += 1

    accuracy = correct_predictions / total_predictions
    print(f"Accuracy: {accuracy}")

#@title LDA WordCloud 
d = {0: {'group': 0.062,
  'peer': 0.016,
  'computer': 0.016,
  'information': 0.0155,
  'service': 0.015,
  'visit': 0.015,
  'inconvenience': 0.013,
  'application': 0.011000000000000001,
  'movie': 0.011,
  'discussion': 0.009333333333333334,
  'view': 0.009333333333333334,
  'nptel': 0.009,
  'connectivity': 0.009,
  'letter': 0.008,
  'connection': 0.008,
  'duty': 0.008,
  'join': 0.0075,
  'message': 0.007,
  'profile': 0.007,
  'internet': 0.007,
  'auction': 0.007,
  'deadline': 0.006666666666666667,
  'contact': 0.0065,
  'test': 0.006,
  'trip': 0.006,
  'water': 0.006,
  'list': 0.005666666666666667,
  'lab': 0.005333333333333333,
  'parent': 0.005,
  'income': 0.005,
  'scholarship': 0.005,
  'scheme': 0.005,
  'verb': 0.005,
  'repeat': 0.005,
  'arm': 0.005,
  'process': 0.0045,
  'campus': 0.0045,
  'thanks': 0.004333333333333333,
  'circuit': 0.004,
  'interview': 0.004,
  'seat': 0.004,
  'document': 0.004,
  'failure': 0.004,
  'issue': 0.003,
  'use': 0.0026,
  'internship': 0.002,
  'coordinator': 0.002,
  'form': 0.00175,
  'series': 0.0016666666666666668,
  'today': 0.0015},
 1: {'team': 0.021,
  'post': 0.019,
  'form': 0.015,
  'club': 0.015,
  'competition': 0.0145,
  'event': 0.0145,
  'assignment': 0.012,
  'google': 0.01,
  'candidate': 0.01,
  'selection': 0.01,
  'game': 0.009,
  'sport': 0.009,
  'fill': 0.0085,
  'submission': 0.0075,
  'member': 0.007,
  'batch': 0.007,
  'player': 0.007,
  'election': 0.007,
  'response': 0.006,
  'secretary': 0.006,
  'status': 0.006,
  'winner': 0.006,
  'student': 0.005,
  'contact': 0.005,
  'activity': 0.005,
  'affair': 0.005,
  'position': 0.005,
  'feel': 0.005,
  'participant': 0.005,
  'nomination': 0.005,
  'vote': 0.005,
  'people': 0.0045,
  'participation': 0.0045,
  'tomorrow': 0.004,
  'query': 0.004,
  'deadline': 0.0036666666666666666,
  'section': 0.0035,
  'entry': 0.0035,
  'mail': 0.003,
  'point': 0.0026666666666666666,
  'date': 0.0025,
  'note': 0.0023333333333333335,
  'thanks': 0.0023333333333333335,
  'time': 0.00225,
  'year': 0.00225,
  'detail': 0.0021999999999999997,
  'case': 0.002,
  'number': 0.0013333333333333333,
  'help': 0.0012000000000000001,
  'request': 0.0012000000000000001},
 2: {'session': 0.068,
  'student': 0.0178,
  'inform': 0.016,
  'information': 0.0135,
  'event': 0.0115,
  'workshop': 0.011,
  'college': 0.009,
  'kind': 0.0085,
  'message': 0.008,
  'opportunity': 0.008,
  'behalf': 0.008,
  'program': 0.0075,
  'join': 0.007,
  'registration': 0.006,
  'poster': 0.006,
  'link': 0.00575,
  'edition': 0.005,
  'register': 0.0045,
  'institution': 0.004,
  'contest': 0.004,
  'conduct': 0.004,
  'chance': 0.004,
  'university': 0.004,
  'hour': 0.004,
  'year': 0.0035,
  'participation': 0.0035,
  'competition': 0.003,
  'talk': 0.003,
  'detail': 0.0028,
  'share': 0.0025,
  'application': 0.0023333333333333335,
  'series': 0.002,
  'platform': 0.002,
  'industry': 0.002,
  'regard': 0.002,
  'speaker': 0.002,
  'research': 0.0016666666666666668,
  'day': 0.0016666666666666668,
  'institute': 0.0016666666666666668,
  'mail': 0.0016,
  'date': 0.0015,
  'request': 0.0014,
  'meeting': 0.0013333333333333333,
  'discussion': 0.0013333333333333333,
  'contact': 0.00125,
  'faculty': 0.00125,
  'case': 0.00125,
  'help': 0.0012000000000000001,
  'email': 0.001,
  'time': 0.0005},
 3: {'project': 0.024,
  'innovation': 0.018,
  'technology': 0.018,
  'team': 0.013,
  'min': 0.01,
  'idea': 0.009,
  'data': 0.009,
  'product': 0.009,
  'support': 0.009,
  'network': 0.008,
  'business': 0.008,
  'solution': 0.007,
  'problem': 0.006333333333333333,
  'communication': 0.006,
  'area': 0.006,
  'machine': 0.006,
  'challenge': 0.005,
  'science': 0.005,
  'skill': 0.005,
  'role': 0.005,
  'interest': 0.005,
  'leader': 0.005,
  'statement': 0.005,
  'career': 0.005,
  'job': 0.005,
  'opportunity': 0.0045,
  'member': 0.004,
  'community': 0.004,
  'knowledge': 0.004,
  'development': 0.0035,
  'field': 0.0035,
  'work': 0.00325,
  'service': 0.003,
  'industry': 0.003,
  'experience': 0.003,
  'world': 0.0025,
  'access': 0.0025,
  'platform': 0.0025,
  'design': 0.002,
  'system': 0.002,
  'program': 0.002,
  'model': 0.002,
  'visit': 0.002,
  'share': 0.00175,
  'message': 0.00175,
  'help': 0.0016,
  'use': 0.0014,
  'research': 0.0013333333333333333,
  'faculty': 0.001,
  'change': 0.0008},
 4: {'talk': 0.021,
  'research': 0.016666666666666666,
  'proposal': 0.013,
  'analysis': 0.011,
  'presentation': 0.011,
  'technique': 0.009,
  'material': 0.009,
  'seminar': 0.009,
  'paper': 0.008,
  'method': 0.008,
  'study': 0.0075,
  'performance': 0.007,
  'structure': 0.007,
  'patient': 0.006,
  'health': 0.006,
  'stress': 0.006,
  'effect': 0.006,
  'discus': 0.006,
  'state': 0.005,
  'result': 0.005,
  'power': 0.005,
  'condition': 0.005,
  'trial': 0.005,
  'system': 0.004666666666666667,
  'model': 0.0045,
  'reminder': 0.004,
  'control': 0.004,
  'space': 0.004,
  'cover': 0.004,
  'focus': 0.004,
  'conference': 0.004,
  'interaction': 0.004,
  'factor': 0.004,
  'colleague': 0.004,
  'graph': 0.004,
  'work': 0.00375,
  'meeting': 0.0036666666666666666,
  'detail': 0.003,
  'problem': 0.0029999999999999996,
  'series': 0.0029999999999999996,
  'field': 0.0025,
  'process': 0.0025,
  'property': 0.0025,
  'speaker': 0.0025,
  'application': 0.002,
  'design': 0.002,
  'development': 0.002,
  'number': 0.0018333333333333333,
  'link': 0.00125,
  'time': 0.0005},
 5: {'forum': 0.072,
  'digest': 0.043,
  'lecture': 0.037,
  'class': 0.0365,
  'announcement': 0.029,
  'topic': 0.019,
  'question': 0.011333333333333334,
  'quiz': 0.01,
  'zoom': 0.01,
  'tomorrow': 0.009,
  'doubt': 0.009,
  'copy': 0.009,
  'regard': 0.0085,
  'let': 0.008,
  'submit': 0.008,
  'answer': 0.008,
  'meeting': 0.007666666666666666,
  'submission': 0.0075,
  'slide': 0.007,
  'sheet': 0.007,
  'paper': 0.0065,
  'today': 0.006,
  'client': 0.006,
  'watch': 0.006,
  'link': 0.00575,
  'note': 0.005333333333333333,
  'motor': 0.005,
  'video': 0.004,
  'solution': 0.004,
  'chemistry': 0.004,
  'roll': 0.004,
  'review': 0.004,
  'kind': 0.0035,
  'concern': 0.0035,
  'reminder': 0.003,
  'view': 0.0026666666666666666,
  'problem': 0.0023333333333333335,
  'thanks': 0.0023333333333333335,
  'student': 0.0021999999999999997,
  'discussion': 0.002,
  'word': 0.002,
  'time': 0.00175,
  'message': 0.00175,
  'contact': 0.0015,
  'number': 0.001,
  'change': 0.001,
  'use': 0.001,
  'request': 0.001,
  'date': 0.001,
  'email': 0.0008},
 6: {'campus': 0.02,
  'hostel': 0.02,
  'staff': 0.016,
  'situation': 0.013,
  'office': 0.012,
  'student': 0.011,
  'mess': 0.01,
  'company': 0.01,
  'room': 0.009,
  'survey': 0.008,
  'day': 0.007,
  'permission': 0.007,
  'cycle': 0.007,
  'person': 0.0065,
  'return': 0.006,
  'plan': 0.006,
  'month': 0.006,
  'measure': 0.006,
  'order': 0.006,
  'facility': 0.006,
  'security': 0.005,
  'attendance': 0.005,
  'bus': 0.005,
  'suggestion': 0.005,
  'safety': 0.005,
  'report': 0.005,
  'rule': 0.005,
  'period': 0.005,
  'employee': 0.005,
  'work': 0.00475,
  'home': 0.004,
  'activity': 0.0035,
  'lab': 0.0033333333333333335,
  'instruction': 0.003,
  'coordinator': 0.003,
  'internship': 0.003,
  'case': 0.00275,
  'schedule': 0.0025,
  'lot': 0.0025,
  'time': 0.002375,
  'institute': 0.0023333333333333335,
  'year': 0.00225,
  'member': 0.002,
  'help': 0.0018,
  'week': 0.0015,
  'faculty': 0.0015,
  'mail': 0.0012000000000000001,
  'number': 0.0011666666666666668,
  'request': 0.001,
  'change': 0.001},
 7: {'account': 0.034,
  'book': 0.032,
  'invitation': 0.025,
  'file': 0.022,
  'phone': 0.016,
  'drive': 0.015,
  'access': 0.013,
  'damage': 0.012,
  'video': 0.0115,
  'item': 0.011,
  'entry': 0.0095,
  'click': 0.009,
  'organizer': 0.009,
  'stop': 0.009,
  'page': 0.009,
  'address': 0.009,
  'meet': 0.008,
  'calendar': 0.008,
  'reply': 0.008,
  'article': 0.008,
  'line': 0.008,
  'source': 0.008,
  'logo': 0.008,
  'folder': 0.008,
  'receiving': 0.008,
  'comment': 0.008,
  'bee': 0.008,
  'response': 0.007,
  'image': 0.007,
  'detection': 0.006,
  'log': 0.006,
  'relief': 0.006,
  'theme': 0.006,
  'orientation': 0.006,
  'link': 0.005,
  'description': 0.005,
  'modify': 0.005,
  'verification': 0.005,
  'design': 0.004666666666666667,
  'notification': 0.0045,
  'week': 0.00425,
  'email': 0.004,
  'version': 0.003,
  'list': 0.0029999999999999996,
  'view': 0.0029999999999999996,
  'change': 0.0026,
  'share': 0.0025,
  'point': 0.0023333333333333335,
  'mail': 0.0016,
  'request': 0.0014},
 8: {'course': 0.178,
  'semester': 0.028,
  'fee': 0.019,
  'payment': 0.019,
  'registration': 0.014,
  'instructor': 0.013,
  'match': 0.013,
  'student': 0.0114,
  'preference': 0.01,
  'evaluation': 0.01,
  'phase': 0.009,
  'exam': 0.009,
  'slot': 0.007,
  'trademark': 0.007,
  'batch': 0.006,
  'module': 0.006,
  'recommendation': 0.006,
  'backlog': 0.006,
  'credit': 0.006,
  'approval': 0.006,
  'class': 0.0055,
  'note': 0.005,
  'drop': 0.005,
  'consent': 0.005,
  'catalog': 0.005,
  'faculty': 0.004,
  'manage': 0.004,
  'register': 0.0035,
  'schedule': 0.0035,
  'difficulty': 0.0035,
  'date': 0.003,
  'section': 0.003,
  'list': 0.0029999999999999996,
  'form': 0.00275,
  'query': 0.0025,
  'end': 0.0025,
  'property': 0.0025,
  'notification': 0.0025,
  'fill': 0.0025,
  'institute': 0.002,
  'deadline': 0.002,
  'concern': 0.002,
  'number': 0.0016666666666666668,
  'change': 0.0016,
  'detail': 0.0016,
  'week': 0.0015,
  'time': 0.00125,
  'email': 0.001,
  'mail': 0.001,
  'today': 0.001},
 9: {'mark': 0.026,
  'code': 0.018,
  'term': 0.016,
  'score': 0.015,
  'test': 0.013,
  'examination': 0.01,
  'case': 0.0095,
  'end': 0.008,
  'road': 0.008,
  'block': 0.008,
  'trouble': 0.007,
  'need': 0.007,
  'location': 0.007,
  'criterion': 0.006,
  'size': 0.006,
  'input': 0.006,
  'ability': 0.006,
  'unsubscribe': 0.006,
  'try': 0.006,
  'issue': 0.005,
  'approach': 0.005,
  'prepare': 0.005,
  'vehicle': 0.005,
  'rest': 0.005,
  'flood': 0.005,
  'soil': 0.005,
  'question': 0.004,
  'estimate': 0.004,
  'experiment': 0.004,
  'poverty': 0.004,
  'flight': 0.004,
  'decision': 0.004,
  'auto': 0.004,
  'dimension': 0.004,
  'component': 0.004,
  'distance': 0.004,
  'data': 0.0035,
  'practice': 0.003,
  'time': 0.002875,
  'version': 0.0025,
  'instruction': 0.0025,
  'difficulty': 0.0025,
  'lab': 0.0023333333333333335,
  'study': 0.002,
  'form': 0.00175,
  'email': 0.0016,
  'use': 0.0014,
  'detail': 0.0014,
  'number': 0.001,
  'week': 0.001},
 10: {'thing': 0.027,
  'way': 0.023,
  'type': 0.018,
  'life': 0.017,
  'people': 0.0145,
  'body': 0.013,
  'story': 0.013,
  'year': 0.009,
  'exercise': 0.009,
  'moment': 0.009,
  'mentor': 0.009,
  'hand': 0.009,
  'word': 0.008,
  'eye': 0.008,
  'mind': 0.008,
  'experience': 0.0075,
  'movement': 0.007,
  'joy': 0.007,
  'place': 0.007,
  'control': 0.006,
  'congratulation': 0.006,
  'woman': 0.006,
  'sentence': 0.006,
  'language': 0.006,
  'world': 0.005,
  'fact': 0.005,
  'school': 0.005,
  'night': 0.005,
  'challenge': 0.0045,
  'idea': 0.004,
  'lot': 0.004,
  'money': 0.004,
  'sense': 0.004,
  'step': 0.004,
  'medium': 0.004,
  'matter': 0.004,
  'head': 0.004,
  'day': 0.0036666666666666666,
  'person': 0.0035,
  'question': 0.0033333333333333335,
  'time': 0.003125,
  'help': 0.003,
  'practice': 0.003,
  'home': 0.003,
  'point': 0.0029999999999999996,
  'share': 0.00225,
  'work': 0.002,
  'today': 0.00175,
  'system': 0.0013333333333333333,
  'use': 0.0012000000000000001}}

"""###LDA Old WordCloud"""

d_old = {0: {'group': 0.062,
  'application': 0.033,
  'information': 0.031,
  'service': 0.03,
  'visit': 0.03,
  'message': 0.028,
  'discussion': 0.028,
  'view': 0.028,
  'contact': 0.026,
  'deadline': 0.02,
  'list': 0.017,
  'lab': 0.016,
  'peer': 0.016,
  'computer': 0.016,
  'join': 0.015,
  'inconvenience': 0.013,
  'use': 0.013,
  'thanks': 0.013,
  'test': 0.012,
  'movie': 0.011,
  'nptel': 0.009,
  'connectivity': 0.009,
  'process': 0.009,
  'campus': 0.009,
  'letter': 0.008,
  'connection': 0.008,
  'duty': 0.008,
  'profile': 0.007,
  'internet': 0.007,
  'auction': 0.007,
  'form': 0.007,
  'issue': 0.006,
  'trip': 0.006,
  'water': 0.006,
  'today': 0.006,
  'series': 0.005,
  'parent': 0.005,
  'income': 0.005,
  'scholarship': 0.005,
  'scheme': 0.005,
  'verb': 0.005,
  'repeat': 0.005,
  'arm': 0.005,
  'internship': 0.004,
  'circuit': 0.004,
  'interview': 0.004,
  'coordinator': 0.004,
  'seat': 0.004,
  'document': 0.004,
  'failure': 0.004},
 1: {'form': 0.06,
  'team': 0.042,
  'competition': 0.029,
  'event': 0.029,
  'student': 0.025,
  'member': 0.021,
  'contact': 0.02,
  'post': 0.019,
  'time': 0.018,
  'fill': 0.017,
  'submission': 0.015,
  'mail': 0.015,
  'club': 0.015,
  'batch': 0.014,
  'response': 0.012,
  'assignment': 0.012,
  'detail': 0.011,
  'deadline': 0.011,
  'google': 0.01,
  'candidate': 0.01,
  'activity': 0.01,
  'date': 0.01,
  'selection': 0.01,
  'game': 0.009,
  'year': 0.009,
  'people': 0.009,
  'participation': 0.009,
  'sport': 0.009,
  'case': 0.008,
  'number': 0.008,
  'tomorrow': 0.008,
  'point': 0.008,
  'query': 0.008,
  'note': 0.007,
  'section': 0.007,
  'player': 0.007,
  'entry': 0.007,
  'thanks': 0.007,
  'election': 0.007,
  'secretary': 0.006,
  'status': 0.006,
  'winner': 0.006,
  'help': 0.006,
  'request': 0.006,
  'affair': 0.005,
  'position': 0.005,
  'feel': 0.005,
  'participant': 0.005,
  'nomination': 0.005,
  'vote': 0.005},
 2: {'student': 0.089,
  'session': 0.068,
  'message': 0.032,
  'information': 0.027,
  'link': 0.023,
  'event': 0.023,
  'kind': 0.017,
  'inform': 0.016,
  'opportunity': 0.016,
  'program': 0.015,
  'year': 0.014,
  'detail': 0.014,
  'join': 0.014,
  'registration': 0.012,
  'workshop': 0.011,
  'share': 0.01,
  'register': 0.009,
  'college': 0.009,
  'behalf': 0.008,
  'mail': 0.008,
  'participation': 0.007,
  'application': 0.007,
  'request': 0.007,
  'date': 0.006,
  'poster': 0.006,
  'help': 0.006,
  'series': 0.006,
  'competition': 0.006,
  'talk': 0.006,
  'contact': 0.005,
  'research': 0.005,
  'faculty': 0.005,
  'day': 0.005,
  'edition': 0.005,
  'institute': 0.005,
  'case': 0.005,
  'email': 0.005,
  'institution': 0.004,
  'platform': 0.004,
  'contest': 0.004,
  'conduct': 0.004,
  'chance': 0.004,
  'meeting': 0.004,
  'industry': 0.004,
  'regard': 0.004,
  'discussion': 0.004,
  'university': 0.004,
  'hour': 0.004,
  'speaker': 0.004,
  'time': 0.004},
 3: {'team': 0.026,
  'project': 0.024,
  'problem': 0.019,
  'innovation': 0.018,
  'technology': 0.018,
  'idea': 0.018,
  'data': 0.018,
  'solution': 0.014,
  'work': 0.013,
  'member': 0.012,
  'min': 0.01,
  'challenge': 0.01,
  'product': 0.009,
  'opportunity': 0.009,
  'support': 0.009,
  'network': 0.008,
  'business': 0.008,
  'help': 0.008,
  'share': 0.007,
  'development': 0.007,
  'field': 0.007,
  'message': 0.007,
  'use': 0.007,
  'design': 0.006,
  'communication': 0.006,
  'area': 0.006,
  'service': 0.006,
  'industry': 0.006,
  'system': 0.006,
  'machine': 0.006,
  'experience': 0.006,
  'world': 0.005,
  'science': 0.005,
  'skill': 0.005,
  'role': 0.005,
  'interest': 0.005,
  'leader': 0.005,
  'statement': 0.005,
  'career': 0.005,
  'access': 0.005,
  'platform': 0.005,
  'job': 0.005,
  'community': 0.004,
  'research': 0.004,
  'change': 0.004,
  'program': 0.004,
  'model': 0.004,
  'knowledge': 0.004,
  'faculty': 0.004,
  'visit': 0.004},
 4: {'research': 0.05,
  'talk': 0.042,
  'paper': 0.016,
  'detail': 0.015,
  'study': 0.015,
  'work': 0.015,
  'system': 0.014,
  'proposal': 0.013,
  'number': 0.011,
  'analysis': 0.011,
  'presentation': 0.011,
  'meeting': 0.011,
  'model': 0.009,
  'problem': 0.009,
  'series': 0.009,
  'technique': 0.009,
  'material': 0.009,
  'seminar': 0.009,
  'reminder': 0.008,
  'method': 0.008,
  'control': 0.008,
  'performance': 0.007,
  'structure': 0.007,
  'application': 0.006,
  'design': 0.006,
  'patient': 0.006,
  'health': 0.006,
  'stress': 0.006,
  'effect': 0.006,
  'discus': 0.006,
  'field': 0.005,
  'link': 0.005,
  'state': 0.005,
  'process': 0.005,
  'result': 0.005,
  'power': 0.005,
  'property': 0.005,
  'speaker': 0.005,
  'condition': 0.005,
  'trial': 0.005,
  'space': 0.004,
  'cover': 0.004,
  'time': 0.004,
  'focus': 0.004,
  'conference': 0.004,
  'development': 0.004,
  'interaction': 0.004,
  'factor': 0.004,
  'colleague': 0.004,
  'graph': 0.004},
 5: {'class': 0.073,
  'forum': 0.072,
  'digest': 0.043,
  'lecture': 0.037,
  'question': 0.034,
  'announcement': 0.029,
  'today': 0.024,
  'link': 0.023,
  'meeting': 0.023,
  'topic': 0.019,
  'tomorrow': 0.018,
  'regard': 0.017,
  'note': 0.016,
  'submission': 0.015,
  'time': 0.014,
  'paper': 0.013,
  'student': 0.011,
  'quiz': 0.01,
  'zoom': 0.01,
  'doubt': 0.009,
  'copy': 0.009,
  'video': 0.008,
  'let': 0.008,
  'submit': 0.008,
  'view': 0.008,
  'answer': 0.008,
  'solution': 0.008,
  'message': 0.007,
  'slide': 0.007,
  'sheet': 0.007,
  'problem': 0.007,
  'kind': 0.007,
  'thanks': 0.007,
  'concern': 0.007,
  'reminder': 0.006,
  'contact': 0.006,
  'client': 0.006,
  'discussion': 0.006,
  'number': 0.006,
  'watch': 0.006,
  'change': 0.005,
  'use': 0.005,
  'request': 0.005,
  'motor': 0.005,
  'chemistry': 0.004,
  'word': 0.004,
  'email': 0.004,
  'roll': 0.004,
  'review': 0.004,
  'date': 0.004},
 6: {'student': 0.055,
  'campus': 0.04,
  'day': 0.021,
  'hostel': 0.02,
  'work': 0.019,
  'time': 0.019,
  'staff': 0.016,
  'situation': 0.013,
  'person': 0.013,
  'office': 0.012,
  'case': 0.011,
  'mess': 0.01,
  'lab': 0.01,
  'company': 0.01,
  'room': 0.009,
  'help': 0.009,
  'year': 0.009,
  'survey': 0.008,
  'home': 0.008,
  'number': 0.007,
  'permission': 0.007,
  'activity': 0.007,
  'institute': 0.007,
  'cycle': 0.007,
  'mail': 0.006,
  'return': 0.006,
  'instruction': 0.006,
  'coordinator': 0.006,
  'plan': 0.006,
  'week': 0.006,
  'month': 0.006,
  'measure': 0.006,
  'order': 0.006,
  'facility': 0.006,
  'faculty': 0.006,
  'member': 0.006,
  'internship': 0.006,
  'request': 0.005,
  'security': 0.005,
  'attendance': 0.005,
  'bus': 0.005,
  'suggestion': 0.005,
  'safety': 0.005,
  'schedule': 0.005,
  'report': 0.005,
  'rule': 0.005,
  'lot': 0.005,
  'change': 0.005,
  'period': 0.005,
  'employee': 0.005},
 7: {'account': 0.034,
  'book': 0.032,
  'access': 0.026,
  'invitation': 0.025,
  'video': 0.023,
  'file': 0.022,
  'link': 0.02,
  'email': 0.02,
  'entry': 0.019,
  'week': 0.017,
  'phone': 0.016,
  'drive': 0.015,
  'response': 0.014,
  'design': 0.014,
  'change': 0.013,
  'damage': 0.012,
  'item': 0.011,
  'share': 0.01,
  'click': 0.009,
  'organizer': 0.009,
  'list': 0.009,
  'stop': 0.009,
  'notification': 0.009,
  'view': 0.009,
  'page': 0.009,
  'address': 0.009,
  'meet': 0.008,
  'calendar': 0.008,
  'mail': 0.008,
  'reply': 0.008,
  'article': 0.008,
  'line': 0.008,
  'source': 0.008,
  'logo': 0.008,
  'folder': 0.008,
  'receiving': 0.008,
  'comment': 0.008,
  'bee': 0.008,
  'request': 0.007,
  'image': 0.007,
  'point': 0.007,
  'detection': 0.006,
  'log': 0.006,
  'version': 0.006,
  'relief': 0.006,
  'theme': 0.006,
  'orientation': 0.006,
  'description': 0.005,
  'modify': 0.005,
  'verification': 0.005},
 8: {'course': 0.178,
  'student': 0.057,
  'semester': 0.028,
  'registration': 0.028,
  'fee': 0.019,
  'payment': 0.019,
  'faculty': 0.016,
  'note': 0.015,
  'instructor': 0.013,
  'match': 0.013,
  'date': 0.012,
  'batch': 0.012,
  'form': 0.011,
  'class': 0.011,
  'preference': 0.01,
  'time': 0.01,
  'number': 0.01,
  'evaluation': 0.01,
  'phase': 0.009,
  'exam': 0.009,
  'list': 0.009,
  'change': 0.008,
  'detail': 0.008,
  'slot': 0.007,
  'trademark': 0.007,
  'register': 0.007,
  'schedule': 0.007,
  'difficulty': 0.007,
  'module': 0.006,
  'recommendation': 0.006,
  'institute': 0.006,
  'section': 0.006,
  'week': 0.006,
  'backlog': 0.006,
  'deadline': 0.006,
  'credit': 0.006,
  'approval': 0.006,
  'email': 0.005,
  'query': 0.005,
  'end': 0.005,
  'property': 0.005,
  'drop': 0.005,
  'notification': 0.005,
  'consent': 0.005,
  'catalog': 0.005,
  'fill': 0.005,
  'mail': 0.005,
  'concern': 0.004,
  'manage': 0.004,
  'today': 0.004},
 9: {'case': 0.038,
  'test': 0.026,
  'mark': 0.026,
  'time': 0.023,
  'code': 0.018,
  'end': 0.016,
  'term': 0.016,
  'score': 0.015,
  'question': 0.012,
  'examination': 0.01,
  'issue': 0.01,
  'email': 0.008,
  'road': 0.008,
  'block': 0.008,
  'use': 0.007,
  'lab': 0.007,
  'data': 0.007,
  'trouble': 0.007,
  'need': 0.007,
  'location': 0.007,
  'form': 0.007,
  'detail': 0.007,
  'criterion': 0.006,
  'size': 0.006,
  'input': 0.006,
  'practice': 0.006,
  'number': 0.006,
  'ability': 0.006,
  'unsubscribe': 0.006,
  'try': 0.006,
  'approach': 0.005,
  'version': 0.005,
  'instruction': 0.005,
  'difficulty': 0.005,
  'prepare': 0.005,
  'vehicle': 0.005,
  'rest': 0.005,
  'flood': 0.005,
  'soil': 0.005,
  'estimate': 0.004,
  'study': 0.004,
  'experiment': 0.004,
  'poverty': 0.004,
  'flight': 0.004,
  'week': 0.004,
  'decision': 0.004,
  'auto': 0.004,
  'dimension': 0.004,
  'component': 0.004,
  'distance': 0.004},
 10: {'year': 0.036,
  'people': 0.029,
  'thing': 0.027,
  'time': 0.025,
  'way': 0.023,
  'type': 0.018,
  'life': 0.017,
  'word': 0.016,
  'experience': 0.015,
  'help': 0.015,
  'body': 0.013,
  'story': 0.013,
  'control': 0.012,
  'day': 0.011,
  'world': 0.01,
  'question': 0.01,
  'exercise': 0.009,
  'point': 0.009,
  'moment': 0.009,
  'challenge': 0.009,
  'mentor': 0.009,
  'share': 0.009,
  'hand': 0.009,
  'work': 0.008,
  'idea': 0.008,
  'eye': 0.008,
  'lot': 0.008,
  'mind': 0.008,
  'movement': 0.007,
  'today': 0.007,
  'person': 0.007,
  'joy': 0.007,
  'place': 0.007,
  'practice': 0.006,
  'congratulation': 0.006,
  'home': 0.006,
  'use': 0.006,
  'woman': 0.006,
  'sentence': 0.006,
  'language': 0.006,
  'fact': 0.005,
  'school': 0.005,
  'night': 0.005,
  'system': 0.004,
  'money': 0.004,
  'sense': 0.004,
  'step': 0.004,
  'medium': 0.004,
  'matter': 0.004,
  'head': 0.004}}

clusters = []
for i in range(11):
  cluster = []
  # print(d[i])
  for word in d[i]:
    cluster.append(word)
  clusters.append(cluster)

clusters = []
for i in range(11):
  cluster = []
  # print(d[i])
  for word in d_old[i]:
    cluster.append(word)
  clusters.append(cluster)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

cluster_text = [' '.join(cluster) for cluster in clusters]

fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(20, 8))
axs = axs.flatten()

for i, text in enumerate(cluster_text): # replace ... with the rest of the word clouds
    wc = WordCloud(background_color="white").generate(cluster_text[i])
    axs[i].imshow(wc, interpolation='bilinear')
    axs[i].axis('off')

fig.delaxes(axs[-1])
plt.tight_layout()
plt.show()

from wordcloud import WordCloud
import matplotlib.pyplot as plt

cluster_text = [' '.join(cluster) for cluster in clusters]

fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(20, 8))
axs = axs.flatten()

for i, text in enumerate(cluster_text): # replace ... with the rest of the word clouds
    wc = WordCloud(background_color="white").generate(cluster_text[i])
    axs[i].imshow(wc, interpolation='bilinear')
    axs[i].axis('off')

fig.delaxes(axs[-1])
plt.tight_layout()
plt.show()

"""# Evaluation"""

from gensim import corpora, models
from gensim.test.utils import datapath

model_path = datapath("/content/drive/MyDrive/BTP stuff/lda_model_11/Copy of lda_model_11_dummy")
lda_model = models.ldamodel.LdaModel.load(model_path)

dictionary = lda_model.id2word

def model_prediction(text):
  new_text_corpus =  dictionary.doc2bow(text.split())
  prob_topics = lda_model.get_document_topics(new_text_corpus)
  prob_topics.sort(key = lambda x: x[1],reverse=True)
  output_tags = []
  terms = text.split()
  output_tags = list(d[prob_topics[0][0]].keys())[:4]
  # print(output_tags)
  return output_tags

tester = MailTester(test, data, None)

tester.test()

tester.test_sim()

