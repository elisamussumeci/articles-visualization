# coding=utf-8
from collections import Counter
import nltk
from nltk.cluster import  cosine_distance
from nltk.stem import RSLPStemmer
from nltk.corpus import stopwords
from numpy import *
from pandas import *
from re import *

def create_words_vector(list_articles):
	list_aux = []
	stopw = stopwords.words('portuguese')
	for art in list_articles:
		article = art['link_content'].lower().decode('utf8')
		list_words = findall(r'\w+', article,flags = UNICODE)
		important_words = [RSLPStemmer().stem(word) for word in list_words if word not in stopw]
		list_aux += important_words
		art['count_words'] = dict(Counter(important_words))
		del art['link_content']
	vector = list(set(list_aux))
	return vector


def create_freq_vector(list_articles):
	vector = create_words_vector(list_articles)
	for art in list_articles:
		art['freq_vector'] = [art['count_words'].get(item,0) for item in vector ]
		del art['count_words']
	return list_articles


def similar_article(list_articles):
	for i, art in enumerate(list_articles[:-1]):
		list_aux=[]
		index = i+1
		art2 = list_articles[index]
		while (art['published']-art2['published']).days < 15:
			cos = cosine_distance(art['freq_vector'],art2['freq_vector'])
			list_aux.append(art2['_id']) if cos < 0.5 else None
			index += 1
			try:
				art2 = list_articles[index]
			except IndexError:
				break
		art['filhos'] = list_aux
		del art['freq_vector']
	return list_articles
