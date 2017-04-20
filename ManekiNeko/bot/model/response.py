#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import threading
import os

import pandas as pd
import jieba
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.neural_network import MLPClassifier
import ManekiNeko.settings as sett
from bot.core.state import State
from bot.core.state_model import StateModel

module_dir = os.path.dirname(__file__)
jieba.load_userdict(sett.BASE_DIR + "/bot/data/dict.txt.big")


class Response(StateModel):
    THRESHOLD = 0.2
    MAX_RESPONSE_SENTENCE = 500
    BASE_ITER = 50

    RESPONSE_PATH = sett.BASE_DIR + '/bot/data/response_train.csv'
    RESPONSE_BACK_PATH = sett.BASE_DIR + '/bot/data/response_back.csv'

    df = pd.read_csv(RESPONSE_PATH)
    df_response = pd.read_csv(RESPONSE_BACK_PATH)
    response = np.array(df_response.values[:, :1]).ravel()
    # Jieba斷詞
    comma_tokenizer = lambda x: jieba.cut(x, cut_all=False, HMM=True)
    # 斷詞方式
    vect = HashingVectorizer(decode_error='ignore',
                             n_features=2 ** 21,
                             tokenizer=comma_tokenizer,
                             non_negative=True)

    # MLP
    clf = MLPClassifier(hidden_layer_sizes=(10, 5), max_iter=10, alpha=1e-4,
                        solver='adam', verbose=10, tol=1e-4, random_state=1,
                        learning_rate_init=.1)

    def init_model(self):

        if self.check_training():
            return False

        # state change
        self.NOW_STATE = State.TRAINING

        # all data
        X = np.array(self.df.values[:, :1]).ravel()
        # label
        y = np.array(self.df.values[:, 1:2]).ravel()
        y = y.astype(int)

        print("{}, {}".format(X.size, y.size))

        classes = [i for i in range(self.MAX_RESPONSE_SENTENCE)]
        for i in range(self.BASE_ITER):
            self.clf.partial_fit(self.vect.transform(X), y, classes=classes)
            if float(self.clf.loss_) < self.THRESHOLD:
                break

        # state change
        self.NOW_STATE = State.RUNNING

    def predict(self, sentence):

        if not self.check_running():
            return False

        data = self.vect.transform([sentence])
        result = self.clf.predict(data)
        return self.response[int(result[0])]

    def partial_fit(self, last_sentence, next_sentence):

        try:
            res_index = self.response.tolist().index(next_sentence)
        except Exception as e:
            res_index = self.response.size
            self.response = np.append(self.response, next_sentence)

        for i in range(self.BASE_ITER):
            text = self.remove_symbol(last_sentence)
            self.clf.partial_fit(self.vect.transform([text]), [res_index])
            if float(self.clf.loss_) < self.THRESHOLD:
                break

    def partial_fit_two_way(self, last_sentence, next_sentence):

        try:
            next_index = self.response.tolist().index(next_sentence)
        except Exception as e:
            next_index = self.response.size
            self.response = np.append(self.response, next_sentence)

        try:
            last_index = self.response.tolist().index(last_sentence)
        except Exception as e:
            last_index = self.response.size
            self.response = np.append(self.response, last_sentence)

        X = [self.remove_symbol(last_sentence), self.remove_symbol(next_sentence)]
        Y = [next_index, last_index]

        for i in range(self.BASE_ITER):
            self.clf.partial_fit(self.vect.transform(X), Y)
            if float(self.clf.loss_) < self.THRESHOLD:
                break

    def save_csv(self):
        self.df.to_csv(self.RESPONSE_PATH, index=False)
        self.df_response.to_csv(self.RESPONSE_BACK_PATH, index=False)
        print("輸出完成")

    def remove_symbol(self, sentence):
        return re.sub(r'[^\w]', ' ', sentence)


class ResponseModelFitting(threading.Thread):
    def run(self):
        res_model = Response()
        res_model.init_model()


class ResponseModelPartialFitting(threading.Thread):
    last_sentence = ""
    next_sentence = ""

    def __init__(self, last_sentence, next_sentence):
        threading.Thread.__init__(self)
        self.last_sentence = last_sentence
        self.next_sentence = next_sentence

    def run(self):
        res_model = Response()
        res_model.partial_fit_two_way(last_sentence=self.last_sentence,
                                      next_sentence=self.next_sentence)