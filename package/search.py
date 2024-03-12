import csv
import string
from rank_bm25 import BM25Okapi
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from package.preprocess import readCSV

data = None


def prepareSearchData():
    global data

    path = '/Users/supachokjirarojkul/Desktop/SE481-Project-Backend/resource/archive/recipes.csv'
    data = readCSV(path)


# string.punctuation use to remove symbol (e.g. !"#$%&'()*+, -./:;<=>?@[\]^_`{|}~)
def remove_puncts(input_string, string):
    return str(input_string).translate(str.maketrans('', '', string.punctuation)).lower()


def searchByName(query):
    title = data['Name']
    # with open('resource/name.txt', 'w') as f:
    #     f.writelines(title)
    corpus = title.to_numpy().tolist()
    cleaned_corpus = []
    for doc in corpus:
        cleaned_doc = remove_puncts(doc, string)
        cleaned_corpus.append(cleaned_doc)
    tokenized_clean_corpus = []
    # Ex. {[dragon ball]} -> {[dragon], [ball]}
    for doc in cleaned_corpus:
        doc = doc.split()
        tokenized_clean_corpus.append(doc)
    # print(tokenized_clean_corpus)
    bm25 = BM25Okapi(tokenized_clean_corpus)
    # Create txt file
    # ac.trainTitleTextFile(ac.get_text(tokenized_clean_corpus))
    relevent_document = 0
    tokenized_query = remove_puncts(query, string).split(" ")
    doc_scores = bm25.get_scores(tokenized_query).tolist()
    for score in doc_scores:
        if score != 0.0:
            relevent_document += 1
    rank = np.argsort(doc_scores)[::-1]
    if relevent_document > 10:
        return data.iloc[rank[:10]]
    elif 10 >= relevent_document > 0:
        return data.iloc[rank[:relevent_document]]
    else:
        return "No result"


def searchByIngredient(query):
    title = data['RecipeIngredientParts']
    # with open('resource/ingredient.txt', 'w') as f:
    #     f.writelines(title)
    corpus = title.to_numpy().tolist()
    cleaned_corpus = []
    for doc in corpus:
        cleaned_doc = remove_puncts(doc, string)
        cleaned_corpus.append(cleaned_doc)
    tokenized_clean_corpus = []
    for doc in cleaned_corpus:
        doc = doc.split()
        tokenized_clean_corpus.append(doc)
    bm25 = BM25Okapi(tokenized_clean_corpus)
    # Create txt file
    # remove_dupe_stop_word = ac.get_text(tokenized_clean_corpus)
    # remove_dupe_stop_word = [word for word in remove_dupe_stop_word if not word in stopwords.words('english')]
    # ac.trainDescriptionTextFile(ac.get_text(remove_dupe_stop_word))
    relevent_document = 0
    tokenized_query = remove_puncts(query, string).split(" ")
    doc_scores = bm25.get_scores(tokenized_query).tolist()
    for score in doc_scores:
        if score != 0.0:
            relevent_document += 1
    rank = np.argsort(doc_scores)[::-1]
    if relevent_document > 10:
        return data.iloc[rank[:10]]
    elif 10 >= relevent_document > 0:
        return data.iloc[rank[:relevent_document]]
    else:
        return "No result"


def searchByCookingProcess(query):
    title = data['RecipeInstructions']
    # with open('resource/process.txt', 'w') as f:
    #     f.writelines(title)
    corpus = title.to_numpy().tolist()
    cleaned_corpus = []
    for doc in corpus:
        cleaned_doc = remove_puncts(doc, string)
        cleaned_corpus.append(cleaned_doc)
    tokenized_clean_corpus = []
    for doc in cleaned_corpus:
        doc = doc.split()
        tokenized_clean_corpus.append(doc)
    bm25 = BM25Okapi(tokenized_clean_corpus)
    # Create txt file
    # remove_dupe_stop_word = ac.get_text(tokenized_clean_corpus)
    # remove_dupe_stop_word = [word for word in remove_dupe_stop_word if not word in stopwords.words('english')]
    # ac.trainDescriptionTextFile(ac.get_text(remove_dupe_stop_word))
    relevent_document = 0
    tokenized_query = remove_puncts(query, string).split(" ")
    doc_scores = bm25.get_scores(tokenized_query).tolist()
    for score in doc_scores:
        if score != 0.0:
            relevent_document += 1
    rank = np.argsort(doc_scores)[::-1]
    if relevent_document > 10:
        return data.iloc[rank[:10]]
    elif 10 >= relevent_document > 0:
        return data.iloc[rank[:relevent_document]]
    else:
        return "No result"


def findById(idnumber):
    return data.loc[data['RecipeId'] == int(idnumber)]
