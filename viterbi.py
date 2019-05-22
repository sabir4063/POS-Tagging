import numpy as np
	
def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
	"""Run the Viterbi algorithm.
	
	N - number of tokens (length of sentence)
	L - number of labels

	As an input, you are given:
	- Emission scores, as an NxL array
	- Transition scores (Yp -> Yc), as an LxL array
	- Start transition scores (S -> Y), as an Lx1 array
	- End transition scores (Y -> E), as an Lx1 array

	You have to return a tuple (s,y), where:
	- s is the score of the best sequence
	- y is the size N array/seq of integers representing the best sequence.
	"""
	L = start_scores.shape[0]
	assert end_scores.shape[0] == L
	assert trans_scores.shape[0] == L
	assert trans_scores.shape[1] == L
	assert emission_scores.shape[1] == L
	N = emission_scores.shape[0]

	y = []
	#for i in xrange(N):
	#	 # stupid sequence
	#	 y.append(i % L)
	# score set to 0
	#return (0.0, y)
	
	Q = np.arange(L)
	T = N
	p = np.zeros(emission_scores.shape)
	back = np.zeros(emission_scores.shape, dtype=np.int)
	z_pred = np.zeros(shape=(T, ), dtype=np.int)
	
	for q in Q:
		p[0,q] = start_scores[q] + emission_scores[0,q]
		back[0,q] = 0
	
	for t in np.arange(T-1):
		for q in Q:
			p[t+1,q] = np.max([emission_scores[t+1, q] + p[t, qp] + trans_scores[qp, q] for qp in Q])
			back[t+1,q] = np.argmax([emission_scores[t+1, q] + p[t, qp] + trans_scores[qp, q] for qp in Q])

			
	max_score = np.max([p[T-1, qp] + end_scores[qp] for qp in Q])
	last_index = np.argmax([p[T-1, qp] + end_scores[qp] for qp in Q])
	
	tag_list = []
	tag_list.append(last_index)
	back_tag = last_index
	
	for t in np.arange(T-1,0,-1):
		tag_list.append(back[t][back_tag])
		back_tag = back[t][back_tag]
	
	tag_list = tag_list[::-1]
	return max_score, tag_list