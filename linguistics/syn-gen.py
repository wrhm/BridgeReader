#syn-gen.py
#Provides methods for generating synonyms and related terms with respect to a
#given set of keywords.

'''
HackCMU Notes / Plan

Project Name: ?
Project Goal: Find CMU clubs based on searching by intelligently synonym-augmented keyword queries.

Roles:
 - Jai: scraper for clubs and descriptions
 - Billy: synonym search (see below)
 - Ian: front end

Details:
 - Take in a set K of (at least one) keyword(s), create a set T which is the union over k in K of possible synonyms and related terms of k
    - Of course, K is a subset of T
    - EXTENSION: NLP on elaborated description [Is this equivalent to keyword combing?]
 - Let C be the set of all CMU clubs
 - For t in T, let c(t) be the set of clubs whose descriptions contain the term t.
 - Let the set S be the union over all c in C //Set of clubs with non-zero relevance
 - Let the list of results ("R") be the top 3/5/10/n? most relevant elements s in S
    - Subtask: Determine relevance heuristic rel()

To be developed:
 - T (for "Terms"): takes in a keyword/phrase, and returns a list of relevant words/phrases
 - S (derpily for "Set"): set of all possibly relevant clubs //subset of C
 - R (for relevance): takes in (S, T, n) and returns the n most relevant* clubs from S with respect to the terms in T
'''

'''
Ideal format per entry in club_descriptions.txt : 

[Club name] ::: [description] \n

Example:

AB Comedy ::: A permanent committee whose purpose is to provide the campus community with comedy shows during the school year.



TODOs

 - Fix Deep Scrape
 - Extend synonym branching from above and below

'''

from club_scraper import *
import string
import ast, re

alpha = string.ascii_lowercase+string.ascii_uppercase

#harvest_all_clubs()

'''
#This code was used to clean the json file into a line-by-line pairwise file. (Triple-colon delimited)
print 'Reading dict...'
f = open('json_dictionary.txt','r')
line = (f.readlines()[0])[:-1]
f.close()

d = ast.literal_eval(line)

f = open('cleaner_dict.txt','w')
print 'Dict read!'
for e in d:
	d[e] = string.lower(' '.join((' '.join(re.split(',|;|\.',d[e]))).split())
	d[e] = ''.join([x for x in d[e] if x in (alpha+' ')])
	#print e,d[e]
	f.write('%s ::: %s\n'%(e,d[e]))
f.close()
print 'All json dict entries cleaned and written to new file.'
'''

'''
#No longer needed; use dict parser now on punct_cleaned_j_dict
#omit extra spaces
print 'Removing extra spaces from json file...'
s = ''
i = 0
while i < (len(line)-1):
	s += line[i]
	if line[i] in ';,.' and line[i+1]==' ':
		i += 1
	i += 1
f = open('punct_cleaned_j_dict.txt','w')
f.write(s)
f.close()
print 'Extra spaces removed!'
'''

print 'Loading clubs...'
clubs = []
f = open('club_descriptions.txt')
for line in f.readlines():
	pair = (line[:-1]).split(' ::: ')
	clubs.append(pair)
f.close()
print 'Clubs loaded!'

print 'Loading definitions...'
definitions = dict()
f = open('cleaner_dict.txt')
for line in f.readlines():
	pair = (line[:-1]).split(' ::: ')
	definitions[pair[0]] = string.lower(pair[1])
f.close()
print 'Definitions loaded!\n\n'
#print definitions['LINGUISTICS']

#list of all words found in club titles/descriptions
all_words_from_clubs = (' '.join([string.lower(x[0]+' '+x[1]) for x in clubs])).split()
num_words_from_clubs = len(all_words_from_clubs)
#print all_words

all_words_from_defs = (' '.join([string.lower(e+' '+definitions[e]) for e in definitions])).split()
num_words_from_defs = len(all_words_from_defs)
#print clubs

#Returns the fractional prevalence of a word in the corpus all_words_from_clubs
def prevalence(word,corpus):
	word = string.lower(word)
	return (10.0**5.0)*float(corpus.count(word))/float(len(corpus))

#term is a list
def def_per_word(term):
	term = [string.upper(x) for x in term]
	t = []
	for e in term:
		if e in definitions:
			for w in definitions[e].split():
				if w not in t:
					t.append(w)
	return t

#term is a string, n an int
def depth_n_definer(term,n):
	w = term.split()
	for i in xrange(n):
		w = w+def_per_word(w)
	return w

#Scores the similariy of the multiplicities of the elements of lists s and t
#Low score means high similarity
def sim_mult(s,t):
	score = 0.0
	for e in s:
		score += (s.count(e)-t.count(e))**2
	for e in t:
		score += (t.count(e)-s.count(e))**2
	return score


#Returns a set of the terms related to the passed term.
#Either synonyms or uncommon definition constituents.
def related_terms(term, min_prev, max_prev):
	result = [string.lower(x) for x in term.split(' ')]
	others,uncommons = [],[]
	origs = result
	for item in origs:
		if string.upper(item) in definitions:
			others = (definitions[string.upper(item)]).split(' ')
			for e in others:
				if prevalence(e,all_words_from_clubs)>=min_prev and prevalence(e,all_words_from_clubs)<=max_prev:
					uncommons.append(e)
	uncommons = result + uncommons
	result = []
	for e in uncommons:
		if not e in result:
			result.append(e)
	return [string.lower(x) for x in term.split(' ')]+result#+uncommons


#Finds clubs in the club_descriptions.txt file whose definitions contain term
#Returns a set of the names of the relevant clubs.
#NO LONGER NEEDED; SAME FUNCTION SERVED BY SUBROUTINE IN matched_clubs
def relevant_clubs(term):
	result = []
	for e in clubs:
		if term in e[0] or term in e[1]:
			result.append(e)
	return result

#The 'MAGIC' method; returns all clubs pertinent to the query or
#its related terms.
def matched_clubs(query):
	min_prev = 0.1
	max_prev = 65.0
	query = string.upper(query)
	q_rel,q_rel_init = [],related_terms(query, min_prev, max_prev)
	for e in q_rel_init:
		if not e in q_rel:
				q_rel.append(e)
	#q_rel = [x for x in q_rel if (prevalence(x,all_words_from_clubs)>=min_prev and prevalence(x,all_words_from_clubs)<=max_prev)]
	''' for e in query.split(' '):
		if e not in q_rel:
			q_rel = [e]+q_rel '''
	print 'Terms related to \"%s\" between min_prev %.1f and max_prev %.1f: %s.'%(query,min_prev,max_prev,[[x,prevalence(x,all_words_from_clubs)] for x in q_rel])# if prevalence(x,all_words_from_clubs)>=min_prev and prevalence(x,all_words_from_clubs)<=max_prev])
	relevant = []
	for related in q_rel:
		for e in clubs:
			if string.upper(related) in string.upper(e[0]) or string.upper(related) in string.upper(e[1]):
				if e not in relevant:
					relevant.append(e)
		#relevant.append(relevant_clubs(related))
	print '\nClubs containing these terms (%d):'%len(relevant)
	#for c in relevant:
		#print c
	return relevant

#The NEW 'MAGIC' method; returns all clubs pertinent to the query or
#its related terms, ranked by relevance.
def rank_matched_clubs(query,num_winners):
	min_prev = 0.1
	max_prev = 65.0
	query = string.upper(query)
	q_rel,q_rel_init = [],related_terms(query, min_prev, max_prev)
	for e in q_rel_init:
		if not e in q_rel:
				q_rel.append(e)
	#q_rel = [x for x in q_rel if (prevalence(x,all_words_from_clubs)>=min_prev and prevalence(x,all_words_from_clubs)<=max_prev)]
	''' for e in query.split(' '):
		if e not in q_rel:
			q_rel = [e]+q_rel '''
	print '(At most %d) Terms related to \"%s\" between min_prev %.1f and max_prev %.1f: %s.'%(num_winners,query,min_prev,max_prev,[[x,prevalence(x,all_words_from_clubs)] for x in q_rel])# if prevalence(x,all_words_from_clubs)>=min_prev and prevalence(x,all_words_from_clubs)<=max_prev])
	relevant = {}
	for related in q_rel:
		for e in clubs:
			ct = (string.upper(e[0]) + string.upper(e[1])).count(string.upper(related))
			#if string.upper(related) in string.upper(e[0]) + string.upper(e[1]):
			if ct > 0:
				if clubs.index(e) not in relevant:
					relevant[clubs.index(e)] = ct
		#relevant.append(relevant_clubs(related))
	#print '\nClubs containing these terms (%d):'%len(relevant)
	#for c in relevant:
		#print c
	return [clubs[x] for x in sorted(relevant, key=relevant.get, reverse=True)[:num_winners]]

#Identify best-matching club(s) by branching down from term and
#up from each club, scoring highly for high overlap in vocabulary
def two_way_tree_connector(term,depth,num):
	matched = matched_clubs(term)
	c_text = [' '.join(c[0].split()+c[1].split()) for c in matched]
	for i in xrange(len(c_text)):
		c_text[i] = depth_n_definer(c_text[i],depth)

	dnt = depth_n_definer(term,depth)

	#now, find club(s) with greatest c_text overlap with dnt
	winners = []
	scores = []
	for i in xrange(len(c_text)):
		scores.append(sim_mult(c_text[i],dnt))

	for w in xrange(num):
		winner = scores.index(min(scores))
		#print max(scores)
		scores[winner] = max(scores)+1
		winners.append(clubs[winner])
	return winners

#for e in two_way_tree_connector("art",1,6):
#	print e

#for e in matched_clubs('art'):
	#print e

for e in rank_matched_clubs('music',3):
	print '\t%s'%e
print ''
for e in rank_matched_clubs('kayaking',2):
	print '\t%s'%e
print ''
for e in rank_matched_clubs('math',5):
	print '\t%s'%e
print ''
#for e in rank_matched_clubs('leisure',5):
	#print '\t%s'%e
#print '\tSorry, no leisurely activities exist at CMU'