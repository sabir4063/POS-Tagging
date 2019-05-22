#!/bin/python
import string
#import inflect

def preprocess_corpus(train_sents):
	"""Use the sentences to do whatever preprocessing you think is suitable,
	such as counts, keeping track of rare features/words to remove, matches to lexicons,
	loading files, and so on. Avoid doing any of this in token2features, since
	that will be called on every token of every sentence.

	Of course, this is an optional function.

	Note that you can also call token2features here to aggregate feature counts, etc.
	"""
	global brown_map, w2v
	brown_map = {}
	w2v = {}
	
	PATH_CLUSTER = './Data/brown_cluster.txt'
	PATH_W2V = './Data/w2v_cluster_words.txt'
	#PATH_W2V = './Data/w2v_cluster_words_twitter.txt' 
	
	file = open(PATH_CLUSTER, 'r')
	lines = file.readlines()
	
	for line in lines:
		brown_map[line.split()[0]] = line.split()[1]
		
	file = open(PATH_W2V, 'r')
	lines = file.readlines()
	
	for line in lines:
		line = line.replace('\n','')
		#print(line.split(':')[0])
		n_list = line.split(':')[1].split(',')
		del n_list[0]
		n_list = sorted(n_list)
		#print(n_list)
		w2v[line.split(':')[0]] = n_list

def token2features(sent, i, add_neighs = True):
	"""Compute the features of a token.

	All the features are boolean, i.e. they appear or they do not. For the token,
	you have to return a set of strings that represent the features that *fire*
	for the token. See the code below.

	The token is at position i, and the rest of the sentence is provided as well.
	Try to make this efficient, since it is called on every token.

	One thing to note is that it is only called once per token, i.e. we do not call
	this function in the inner loops of training. So if your training is slow, it's
	not because of how long it's taking to run this code. That said, if your number
	of features is quite large, that will cause slowdowns for sure.

	add_neighs is a parameter that allows us to use this function itself in order to
	recursively add the same features, as computed for the neighbors. Of course, we do
	not want to recurse on the neighbors again, and then it is set to False (see code).
	"""
	ftrs = []
	# bias
	ftrs.append("BIAS")
	# position features
	if i == 0:
		ftrs.append("SENT_BEGIN")
	if i == len(sent)-1:
		ftrs.append("SENT_END")

	# the word itself
	word = unicode(sent[i])
	ftrs.append("WORD=" + word)
	ftrs.append("LCASE=" + word.lower())
	# some features of the word
	if word.isalnum():
		ftrs.append("IS_ALNUM")
	if word.isnumeric():
		ftrs.append("IS_NUMERIC")
	if word.isdigit():
		ftrs.append("IS_DIGIT")
	if word.isupper():
		ftrs.append("IS_UPPER")
	if word.islower():
		ftrs.append("IS_LOWER")
	
	ftrs.append("WORD_LENGTH" + str(len(word)))
	ftrs.append("FIRST_ONE_LETTERS" + word[:1])
	ftrs.append("FIRST_TWO_LETTERS" + word[:2])
	ftrs.append("FIRST_THREE_LETTERS" + word[:3])
	ftrs.append("LAST_ONE_LETTERS" + word[-1:])
	ftrs.append("LAST_TWO_LETTERS" + word[-2:])
	ftrs.append("LAST_THREE_LETTERS" + word[-3:])
	
	puncts = set(string.punctuation)
	punct_cnt = 0
	digit_cnt = 0
	caps_cnt = 0
	for c in word:
		if c in puncts:
			punct_cnt += 1
		if c.isdigit():
			digit_cnt += 1
		if not c.islower():
			caps_cnt += 1

	ftrs.append("WORD_LOCATION" + str(i))
	ftrs.append("PUNCT_CNT" + str(punct_cnt))
	ftrs.append("DIGIT_CNT" + str(digit_cnt))
	ftrs.append("CAPS_CNT" + str(caps_cnt))
	
	global brown_map, w2v
	if word in brown_map:
		ftrs.append("BROWN_" + brown_map[word][:30])
	
	if word in w2v:
		for n in w2v[word]:
			ftrs.append("W2V_"+n)
			
	relative_pos = int(i/len(sent)*10)

	bi_word = ''
	tri_word = ''
    
	if i < len(sent)-1:
		bi_word = unicode(sent[i]) + ' ' +unicode(sent[i+1])
	if i < len(sent)-2:
		tri_word = unicode(sent[i]) + ' ' +unicode(sent[i+1]) + ' ' + unicode(sent[i+2])

	ftrs.append("BI_" + bi_word)
	ftrs.append("TRI_" + tri_word)
	ftrs.append("WORD_POS" + str(relative_pos))
	
	# previous/next word feats
	if add_neighs:
		if i > 0:
			for pf in token2features(sent, i-1, add_neighs = False):
				ftrs.append("PREV_" + pf)
		if i < len(sent)-1:
			for pf in token2features(sent, i+1, add_neighs = False):
				ftrs.append("NEXT_" + pf)

	# return it!
	return ftrs

if __name__ == "__main__":
	sents = [
	[ "I", "love", "food" ]
	]
	preprocess_corpus(sents)
	for sent in sents:
		for i in xrange(len(sent)):
			print sent[i], ":", token2features(sent, i)
