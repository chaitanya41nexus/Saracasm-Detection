import nltk
from nltk.collocations import *
import re
import random

# This function parses tweets in a file.  This function expects that tweets have been
# preprocessed so that there is only one tweet per line.
# This function also filters some data out of tweets:
# - Mentions (@Username)
# - Hashtags (#Hashtag)
# - Links (Links of the form https://t.co/...)
# - All ampersand escape sequences are unescaped to reproduce the & character.
# - Filter all text that is not alphanumeric or punctuation.
def parseTweets(filename, category):
	file = open(filename, mode="r", encoding="utf-8")
	result = []
	for line in file:
		# Remove mentions
		line = re.sub("@.+?[ \t\r\n]", "", line)
		# Remove hashtags
		line = re.sub("#.+?[ \t\r\n]", "", line)
		# Remove links
		line = re.sub("https://t.co/[A-Za-z0-9]*", "", line)
		# Replace ampersand escapes
		line = re.sub("&amp;", "&", line)
		# Filter text, define acceptable characters below
		line = re.sub("[^A-Za-z0-9 ,.!?]", "", line)
		result.append((nltk.word_tokenize(line.strip()), category))
	return result

# This function defines a unigram list of features based on if the tweet contains
# the associated word.    
def tweet_features(tweet, word_features):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['V_{}'.format(word)] = (word in tweet_words)
    return features

sarcastic_tweets = parseTweets("preprocessing/sarcasm_pos2.txt", "sar")
not_sarcastic_tweets = parseTweets("preprocessing/sarcasm_neg2.txt", "not")
#print(sarcastic_tweets[:10])
#print(not_sarcastic_tweets[:10])

# Combine the sarcastic and non-sarcastic tweets (which have already been tagged).
all_tweets = sarcastic_tweets + not_sarcastic_tweets
# Shuffle the dataset.
random.shuffle(all_tweets)

# Get a list of all words contained in the dataset.
all_words_list = [word for (sent,cat) in all_tweets for word in sent]
# Filter words of length 1 to remove single-character words from the dataset.
all_words_list = list(filter(lambda x: len(x) > 1, all_words_list))
all_words = nltk.FreqDist(all_words_list)

# Get a list of the most common words to use as word features.
word_items = all_words.most_common(1000)
word_features = [word for (word, count) in word_items]
#print(word_features)

featuresets = [(tweet_features(tweet, word_features), category) for (tweet, category) in all_tweets]

# Define a training set and test set.  The training set is approximately 80% of the data while test is the other 20%.
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print("Accuracy: " + str(nltk.classify.accuracy(classifier, test_set)))

#classifier.show_most_informative_features(30)

# This function classifies a tweet as sarcastic or not.
# tweet - The tweet to classify.
# classifier - The classifier to use.
# word_features - The word features used during classification.
# This function returns a tuple where the first item is the tweet that was classified
# and the second is the classification result.
def classify_unigrams(tweet, classifier, word_features):
    tweet_tokens = nltk.word_tokenize(tweet)
    result = classifier.classify(tweet_features(tweet_tokens, word_features))
    return (tweet, result)

sample_tweet = "I love seeing the snow covering the trees around the university."
result = classify_unigrams(sample_tweet, classifier, word_features)
print(result[0] + ": " + result[1])

sample_tweet = "Walking to class in the snow is really great. I hope it snows some more."
result = classify_unigrams(sample_tweet, classifier, word_features)
print(result[0] + ": " + result[1])
