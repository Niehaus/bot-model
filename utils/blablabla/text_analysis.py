"""

	Generate Topic Models


"""

import re
import os
import unicodedata
import time

import nltk

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import TfidfVectorizer

from gensim.parsing import preprocessing as pp
from scipy.stats import entropy

import scipy.stats as ss


def strip_accentuation(report):

	report = unicodedata.normalize('NFKD', report.lower().strip())

	return ('').join([w for w in report if not unicodedata.combining(w)])

def read_file(file_name):

	with open(file_name, 'r') as file:

		data = file.read().split('\n')

	return data

def select_step_words_set(language, path='aux'):

	if language == 'english':

		return nltk.corpus.stopwords.words('english')

	elif language == 'portuguese':

		stop_words = read_file(path + '/stop_words_pt_br.txt')

		stop_words = list(map(strip_accentuation, stop_words))
		
		return stop_words

	elif language == 'spanish':

		return read_file(path + '/stop_words_spanish.txt')

	assert "Error ! Language " + language + " was not found !"

def pre_process_data(df, column, language='portuguese'):

	stop_words = select_step_words_set(language)
	
	# all reports to lower
	df[column] = df[column].str.lower()
	
	"""
	for tweet in df.itertuples():
		print("===\n",tweet.full_text)
	"""
	# removal of html tags
	df[column] = list(map(pp.strip_tags, df[column]))

	# strip numeric values
	#df[column] = list(map(pp.strip_numeric, df[column].tolist()))
	df[column] = list(map(pp.strip_numeric, df[column]))

	# punctuation strip
	#df[column] = list(map(pp.strip_punctuation, df[column].tolist()))
	df[column] = list(map(pp.strip_punctuation, df[column]))

	# accentuation strip
	#df[column] = list(map(strip_accentuation, df[column].tolist()))
	df[column] = list(map(strip_accentuation, df[column]))

	"""
	print("ANTES")
	for tweet in df.itertuples():
		print("===\n",tweet.full_text)
	"""
	
	# Tokenização
	#df[column] = list(map(lambda dr: nltk.tokenize.word_tokenize(dr, language=language), df[column]))
	
	# stopwords
	#df[column] = list(map(lambda dr: (' ').join([w for w in dr if w not in stop_words]), df[column].tolist()))
	#df[column] = list(map(lambda dr: (' ').join([w for w in dr if w not in stop_words]), df[column]))
	
	"""
	print("DEPOIS:")
	for tweet in df.itertuples():
		print("===\n",tweet.full_text)
	"""

	# removal of small words, with less then 3 characteres
	#df[column] = list(map(pp.strip_short, df[column].tolist()))
	#df[column] = list(map(pp.strip_short, df[column]))
	
	return df

def generate_textual_representation(df, column, language='portuguese'):

	stop_words = select_step_words_set(language)

	tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words=stop_words, ngram_range=(1,2))

	documents = df[column]#.unique()
	
	#print(documents)

	tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

	tfidf_feature_names = tfidf_vectorizer.get_feature_names()
	
	#print(tfidf_matrix.shape)
	#print(len(tfidf_feature_names))
	
	#exit()

	return tfidf_matrix, tfidf_feature_names

def generate_topics(subject, color, tfidf_matrix, amount_topics, algorithm, amount_words=10, plot=False, title=None, tfidf_feature_names=None):

	if algorithm == 'nmf':

		model_topics = NMF(n_components=amount_topics, random_state=1, alpha=.1, l1_ratio=.5).fit(tfidf_matrix)

	elif algorithm == 'lda':

		params = {'n_components': amount_topics, 'max_iter': 5, 'learning_method': 'online',
				  'learning_offset': 50., 'random_state': 0}

		model_topics = LatentDirichletAllocation(**params).fit(tfidf_matrix)

	if plot:

		if title is None:

			title = algorithm

		plot_top_words(model_topics, tfidf_feature_names, amount_words, amount_topics, title, subject, color)

	return model_topics.components_

def plot_top_words(model, feature_names, n_top_words, amount_topics, title, subject, color):

	out_folder = "figs_nmf_%s" % subject

	figure_distribution = {1: (1, 1), 2: (1, 2), 3: (1, 3), 4: (1, 4), 5: (1, 5),
						   6: (2, 3), 7: (2, 4), 8: (2, 4), 9: (2, 5), 10: (2, 5)}

	rows, columns = figure_distribution[amount_topics]

	fig, axes = plt.subplots(rows, columns, figsize=(20, 4), sharex=True)

	axes = axes.flatten()

	for topic_idx, topic in enumerate(model.components_):
		top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
		top_features = [feature_names[i] for i in top_features_ind]
		weights = topic[top_features_ind]

		ax = axes[topic_idx]
		ax.barh(top_features, weights, height=0.5, color=color)
		ax.set_title(f'Tópico {topic_idx + 1}',
					 fontdict={'fontsize': 28})
		ax.invert_yaxis()
		ax.tick_params(axis='both', which='major', labelsize=28)
		for i in 'top right left'.split():
			ax.spines[i].set_visible(False)
		fig.suptitle(title, fontsize=30)

	plt.tight_layout()
	#plt.subplots_adjust(top=0.95, bottom=0.05, wspace=0.6, hspace=0.3)
	#plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.6)

	if out_folder not in os.listdir():

		os.mkdir(out_folder)

	plt.savefig(out_folder + "/" + title.replace(' ', '_') + '.svg')

def identify_topic_document_links(df, column, topics, n_top_words, tfidf_feature_names):

	selected_topics = [-1] * len(df[column].values)

	# measure the amount of words of that topic that is in that document
	amount_words = [0] * len(df[column].values)

	for topic_idx, topic in enumerate(topics):

		top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
		top_features = np.array([tfidf_feature_names[i] for i in top_features_ind])

		for index_document, document in enumerate(df[column].values):

			# the size of the insersection between two topic
			topic_max = len(np.intersect1d(top_features, np.array(document.split(' '))))

			if topic_max > amount_words[index_document]:

				amount_words[index_document] = topic_max

				selected_topics[index_document] = topic_idx

	df['topic'] = selected_topics

	return df

def generate_topic_probability(topics, tfidf_features_names, n_top_words):

	topic_probabilities = []

	for document_row in topics:

		index_top_features = document_row.argsort()[:-n_top_words - 1:-1]

		# getting the feature and it's importance
		top_features = {tfidf_features_names[i]: document_row[i] for i in index_top_features}

		topic_probabilities.append(top_features)


	topic_df = pd.DataFrame(topic_probabilities)

	# writing topic probabilities
	topic_df.to_csv("topic_probabilities.csv", sep=';', index=False)
	
	
def topic_modeling(subject,color,df,column,title_plot,params_ta = {}):

	df = pre_process_data(df, column)
	tfidf_matrix, tfidf_features_names = generate_textual_representation(df, column)
	
	tfidf_matrix, tfidf_features_names = generate_textual_representation(df, column)
	
	title = None

	params = {'amount_topics': 3, 'algorithm': 'nmf', 'amount_words': 5,
			  'plot': True, 'title': title_plot, 'tfidf_feature_names': tfidf_features_names}

	topics = generate_topics(subject, color, tfidf_matrix, **params)

	df = identify_topic_document_links(df, column, topics, params['amount_words'], tfidf_features_names)


	generate_topic_probability(topics, tfidf_features_names, params['amount_words'])
	


#end

def calculate_entropy(df,column):
	
	df = pre_process_data(df, column, language='portuguese')
	
	tweets = []
	st = nltk.RSLPStemmer()
	
	tweet_list_tokenized = list(map(lambda dr: nltk.tokenize.word_tokenize(dr, 'portuguese'), df[column]))
	#print(tweet_list_tokenized)
	
	tweet_list = []
	for tweet in tweet_list_tokenized:
		tweet = list(map(lambda dr: st.stem(dr), tweet))
		tweet_list = tweet_list + tweet
	#print("\n\n\n\n\n")

	#print(tweet_list)
	#exit()
	
	total_terms = len(tweet_list)
	
	
	count_termos = dict()
	for term in set(tweet_list):
		count_termos[term] = tweet_list.count(term)
	
	#print(count_termos)
	
	probabilities = []
	for term in set(tweet_list):
		probabilities.append(count_termos[term]/total_terms)
	
	entropy_df = ss.entropy(probabilities, base=2)
		
	return entropy_df
#end def

def get_tweets_info(df_tweets_community):
	all_tweets = len(df_tweets_community.index)
	print("Number of tweets (all):",all_tweets)
	
	
	
	num_retweets = df_tweets_community['retweet'].value_counts()['True']
		
	print("Number of retweets:",num_retweets)
	print("Proportion of retweets:",(num_retweets/all_tweets))

if __name__ == '__main__':


	# input dataset
	input_name = 'stf/timeline/top/stf_retweet_top_community0/top_community0_full_text.csv'

	df = pd.read_csv(input_name, sep=',')
	
	df = df.head(250)

	df = pre_process_data(df, 'full_text')

	#print(df['full_text'])
	after_stop_word = []
	before_stop_word = []

	stop_words = select_step_words_set(language='portuguese')
	last_i = -1
	print(len(df['full_text']))
	for	tweet in df['full_text']:
		words = tweet.split()	
		for i, word in enumerate(words):
			if(word in stop_words):
				phrase = ' '.join(words[last_i + 1:i + 1])
				if(not phrase in before_stop_word): before_stop_word.append(phrase)
				last_i = i
				
				half_tweet = round(len(words) / 2)
				end_tweet = len(words)

				end_phrase = ' '.join(words[half_tweet:end_tweet])
				begin_phrase = ' '.join(words[:half_tweet])

				if(not end_phrase in after_stop_word): after_stop_word.append(end_phrase)
				if(not begin_phrase in after_stop_word): after_stop_word.append(begin_phrase)
			
	
	#print('antes', before_stop_word)
	#print()
	print('depois', after_stop_word)

	print(before_stop_word[14] + after_stop_word[32])



	#tfidf_matrix, tfidf_features_names = generate_textual_representation(df, 'full_text')
	
	
	#print(tfidf_matrix)
	#print(tfidf_features_names)


	#title = None

	#params = {'amount_topics': 10, 'algorithm': 'lda', 'amount_words': 10,
	#		  'plot': True, 'title': title, 'tfidf_feature_names': tfidf_features_names}

	#topics = generate_topics(color='red', tfidf_matrix=tfidf_matrix, **params)

	#df = identify_topic_document_links(df, 'full_text', topics, params['amount_words'], tfidf_features_names)


	#generate_topic_probability(topics, tfidf_features_names, params['amount_words'])

