import nltk
import re
import random
import nltk
from nltk.tokenize import *

TESTCOUNT = 200

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

print(sarcastic_tweets[:10])
print(not_sarcastic_tweets[:10])

 #add stopword
stopwords = nltk.corpus.stopwords.words('english')
stopwords.append('!');
stopwords.append('.');
stopwords.append('?');
stopwords.append('...');
stopwords.append(',');
for i in range(97, 123):
		stopwords.append(chr(i)); # a-z

all_tweets = sarcastic_tweets + not_sarcastic_tweets
random.shuffle(all_tweets)

all_words_list = [word for (sent,cat) in all_tweets for word in sent if word not in stopwords] # filter by stopword
all_words = nltk.FreqDist(all_words_list)

word_items = all_words.most_common(100)
word_features = [word for (word, count) in word_items]
#print(word_features)

print("len", len(all_tweets))
train_featuresets = all_tweets[500:]
test_featuresets =  all_tweets[:TESTCOUNT]

def cross_validation_accuracy(num_folds, featuresets):
    subset_size = int(len(featuresets)/num_folds)
    print('Each fold size:', subset_size)
    accuracy_list = []
    # iterate over the folds
    for i in range(num_folds):
        test_this_round = featuresets[(i*subset_size):][:subset_size]
        train_this_round = featuresets[:(i*subset_size)] + featuresets[((i+1)*subset_size):]
        # train using train_this_round
        classifier = nltk.NaiveBayesClassifier.train(train_this_round)
        # evaluate against test_this_round and save accuracy
        accuracy_this_round = nltk.classify.accuracy(classifier, test_this_round)
        print (i, accuracy_this_round)
        accuracy_list.append(accuracy_this_round)
    # find mean accuracy over all rounds
    print ('mean accuracy', sum(accuracy_list) / num_folds)

print("######################################  unigram ##########################################")
def tweet_features(tweet, word_features):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['V_{}'.format(word)] = (word in tweet_words)
    return features

train_set =  [(tweet_features(tweet, word_features), category) for (tweet, category) in train_featuresets]
test_set = [(tweet_features(tweet, word_features), category) for (tweet, category) in test_featuresets]

classifier = nltk.NaiveBayesClassifier.train(train_set)
print("Unigram Classifier accuracy ", nltk.classify.accuracy(classifier, test_set))

##################### validation #####################
# get features sets for a document, including keyword features and category feature

classifier.show_most_informative_features(30)
featuresets = [(tweet_features(d, word_features), c) for (d, c) in all_tweets]
print("\nCross-validation:")
num_folds = 5
cross_validation_accuracy(num_folds, featuresets)

print("######################################  unigram ##########################################")


print("######################################  bigram ###########################################")
####  Task 1: adding Bigram features   ####
# set up for using bigrams
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()

# create the bigram finder on all the words in sequence
#print(all_words_list[:50])
finder = BigramCollocationFinder.from_words(all_words_list)

# define the top 500 bigrams using the chi squared measure
bigram_features = finder.nbest(bigram_measures.chi_sq, 500)
#print(bigram_features[:50])

# examples to demonstrate the bigram feature function definition
sent = ['So', 'glad', 'our', 'secret', 'of', 'having', 'a', 'problem', 'down', 'the', 'left', 'didn\'t', 'get', 'exposed']
sentbigrams = list(nltk.bigrams(sent))
print(sentbigrams)

# for a single bigram, test if it's in the sentence bigrams and format the feature name
bigram = ('our','secret')
#print(bigram in sentbigrams)
print('B_{}_{}'.format(bigram[0], bigram[1]))

# define features that include words as before 
# add the most frequent significant bigrams
# this function takes the list of words in a document as an argument and returns a feature dictionary
# it depends on the variables word_features and bigram_features
def bigram_document_features(document, word_features, bigram_features):
    document_words = set(document)
    document_bigrams = nltk.bigrams(document)
    features = {}
    for word in word_features:
        features['V_{}'.format(word)] = (word in document_words)
    for bigram in bigram_features:
        features['B_{}_{}'.format(bigram[0], bigram[1])] = (bigram in document_bigrams)    
    return features

# use this function to create feature sets for all sentences
train_set =  [(bigram_document_features(tweet, word_features, bigram_features), category) for (tweet, category) in train_featuresets]
test_set = [(bigram_document_features(tweet, word_features, bigram_features), category) for (tweet, category) in test_featuresets]

# features in document 0
# print(bigram_featuresets[0][0])

# train a classifier and report accuracy
#train_set, test_set = bigram_featuresets[10:], bigram_featuresets[:10]
bi_classifier = nltk.NaiveBayesClassifier.train(train_set)
print("Bigram Classifier accuracy :",nltk.classify.accuracy(bi_classifier, test_set))

bi_classifier.show_most_informative_features(30)

BI_featuresets = [(bigram_document_features(d, word_features, bigram_features), c) for (d, c) in all_tweets]
print("\nCross-validation:")
num_folds = 5
cross_validation_accuracy(num_folds, BI_featuresets)
print("######################################  bigram ###########################################")

print("###################################  POS tag counts ######################################")
# using the default pos tagger in NLTK (the Stanford tagger)
#print(sent)
#print(nltk.pos_tag(sent))

# this function takes a document list of words and returns a feature dictionary
# it runs the default pos tagger (the Stanford tagger) on the document
#   and counts 4 types of pos tags to use as features
def POS_features(document, word_features):
    document_words = set(document)
    tagged_words = nltk.pos_tag(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    numNoun = 0
    numVerb = 0
    numAdj = 0
    numAdverb = 0
    for (word, tag) in tagged_words:
        if tag.startswith('N'): numNoun += 1
        if tag.startswith('V'): numVerb += 1
        if tag.startswith('J'): numAdj += 1
        if tag.startswith('R'): numAdverb += 1
    features['nouns'] = numNoun
    features['verbs'] = numVerb
    features['adjectives'] = numAdj
    features['adverbs'] = numAdverb
    return features

# define feature sets using this function
POS_featuresets = [(POS_features(d, word_features), c) for (d, c) in all_tweets]
# the first sentence
print(all_tweets[0])
# the pos tag features for this sentence
print('num nouns', POS_featuresets[0][0]['nouns'])
print('num verbs', POS_featuresets[0][0]['verbs'])
print('num adjectives', POS_featuresets[0][0]['adjectives'])
print('num adverbs', POS_featuresets[0][0]['adverbs'])

# train and test the classifier
train_set =  [(POS_features(tweet, word_features), category) for (tweet, category) in train_featuresets]
test_set = [(POS_features(tweet, word_features), category) for (tweet, category) in test_featuresets]
pos_classifier = nltk.NaiveBayesClassifier.train(train_set)
print("POS Classifier accuracy: ", nltk.classify.accuracy(pos_classifier, test_set))

pos_classifier.show_most_informative_features(30)

print("\nCross-validation:")
num_folds = 5
cross_validation_accuracy(num_folds, POS_featuresets)
print("###################################  POS tag counts #######################################")

############################## score the sentence ###############################
def classifySentence(tweet):
    guess = "not"
    sar_count = 0
    not_count = 0
    for word in tweet:
       # using bigram
        word_guess = bi_classifier.classify(bigram_document_features(word, word_features, bigram_features))
        if word_guess == "sar":
            sar_count = sar_count + 5
        #if word_guess == "not":
        #    not_count = not_count + 2
         
        # using unigram
        word_guess = classifier.classify(tweet_features(word, word_features))
        if word_guess == "sar":
            sar_count = sar_count + 1
        if word_guess == "not":
            not_count = not_count + 1
        # using pos tag
        word_guess = pos_classifier.classify(POS_features(word, word_features))
        if word_guess == "sar":
            sar_count = sar_count + 2
        if word_guess == "not":
            not_count = not_count + 2

    if sar_count > not_count:
        guess = "sar"
    else:
        guess = "not"
    return guess

print("#####################################  comparison ########################################")
# define a function that will compare the classifier labels with the gold standard labels
def geterrors(test):
    errors = []
    for (tweet, tag) in test:
        guess = classifySentence(tweet)
       # score result
        if guess != tag:
            tweet = ' '.join(tweet)
            errors.append( (tag, guess, tweet) )
    return errors

errors = geterrors(test_featuresets)
print("Accuracy on sentence level: ", (TESTCOUNT - len(errors))/TESTCOUNT)

# define a function to print the errors
def printerrors(errors):
    count = 0
    for (tag, guess, tweet) in sorted(errors):
        print('correct={:<8s} guess={:<8s} tweet={:<30s}'.format(tag, guess, tweet))
        count = count + 1
        if count == 10:
          break

printerrors(errors)
print("#####################################  comparison #######################################")
# classifier - unigram
# bi_classifier - bigram
# pos_classifier - pos tag
# more classider
sample_tweet = "I love creating sample sarcastic tweets..."
print(sample_tweet + ": " + classifier.classify(tweet_features(sample_tweet, word_features)))
sample_tweet = "I love creating sample sarcastic tweets!"
print(sample_tweet + ": " + classifier.classify(tweet_features(sample_tweet, word_features)))