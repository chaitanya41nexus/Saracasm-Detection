import nltk
import re
import random

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
		result.append((nltk.word_tokenize(line.strip().lower()), category)) # lower case
	return result

sarcastic_tweets = parseTweets("preprocessing/sarcasm_pos.txt", "sar")
not_sarcastic_tweets = parseTweets("preprocessing/sarcasm_neg.txt", "not")
#print(sarcastic_tweets[:10])
#print(not_sarcastic_tweets[:10])

 #add stopword
stopwords = nltk.corpus.stopwords.words('english')
stopwords.append('!');
stopwords.append('.');
stopwords.append('?');
stopwords.append('...');

all_tweets = sarcastic_tweets + not_sarcastic_tweets
random.shuffle(all_tweets)

all_words_list = [word for (sent,cat) in all_tweets for word in sent if word not in stopwords] # filter by stopword
all_words = nltk.FreqDist(all_words_list)

word_items = all_words.most_common(100)
word_features = [word for (word, count) in word_items]
#print(word_features)

def tweet_features(tweet, word_features):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['V_{}'.format(word)] = (word in tweet_words)
    return features

featuresets = [(tweet_features(tweet, word_features), category) for (tweet, category) in all_tweets]

train_set, test_set = featuresets[20:], featuresets[:20]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)

classifier.show_most_informative_features(30)

sample_tweet = "I love creating sample sarcastic tweets..."
print(sample_tweet + ": " + classifier.classify(tweet_features(sample_tweet, word_features)))
sample_tweet = "I love creating sample sarcastic tweets!"
print(sample_tweet + ": " + classifier.classify(tweet_features(sample_tweet, word_features)))