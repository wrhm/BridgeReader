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

'''

from club_scraper import *
import string
import ast, re

alpha = string.ascii_lowercase+string.ascii_uppercase

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
print 'Definitions loaded!'
#print definitions['LINGUISTICS']

#list of all words found in club titles/descriptions
all_words_from_clubs = (' '.join([string.lower(x[0]+' '+x[1]) for x in clubs])).split()
num_words_from_clubs = len(all_words_from_clubs)
#print all_words

all_words_from_defs = (' '.join([string.lower(e+' '+definitions[e]) for e in definitions])).split()
num_words_from_defs = len(all_words_from_defs)
#print clubs

#Returns the fractional prevalence of a word in the corpus all_words_from_clubs
def prevalence(word):
	word = string.lower(word)
	return (10.0**5.0)*float(all_words_from_clubs.count(word))/float(num_words_from_clubs)

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
				if prevalence(e)>=min_prev and prevalence(e)<=max_prev:
					uncommons.append(e)
	uncommons = result + uncommons
	result = []
	for e in uncommons:
		if not e in result:
			result.append(e)
	'''for x in result:
		if string.upper(x) in definitions and prevalence(x)<max_prev:
			for e in (definitions[string.upper(x)]).split(' '):
				if not e in uncommons:
					uncommons += e'''
	return result#+uncommons

'''
#outdated
def related_terms(term, max_prev):
	result = [term]+term.split()
	others, uncommons = [], []
	if string.upper(term) in definitions:
		others = (' '.join([definitions[string.upper(x)] for x in result if string.upper(x) in definitions])).split()
		others += uncommons
		uncommons = [x for x in others if prevalence(x)<max_prev and x not in uncommons]
		singles = []
		for x in uncommons:
			if not x in singles:
				singles.append(x)
		uncommons = singles
		print '%s has a definition: %s'%(term,uncommons)#others)
	for e in term.split() + uncommons:
		if e not in result and prevalence(e)<max_prev:
			result.append(e)
	return result
'''

#print related_terms('linguistics')

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
	min_prev, max_prev = 0.0,65.0
	query = string.upper(query)
	q_rel = related_terms(query, min_prev, max_prev)
	q_rel = [x for x in q_rel if prevalence(x)>=min_prev and prevalence(x)<=max_prev]
	print 'Terms related to \"%s\" between min_prev %.1f and max_prev %.1f: %s.'%(query,min_prev,max_prev,[[x,prevalence(x)] for x in q_rel if prevalence(x)>=min_prev and prevalence(x)<=max_prev])#q_rel)
	relevant = []
	for related in q_rel:
		for e in clubs:
			if string.upper(related) in string.upper(e[0]) or string.upper(related) in string.upper(e[1]):
				relevant.append(e)
		#relevant.append(relevant_clubs(related))
	print '\nClubs containing these terms (%d):'%len(relevant)
	for c in relevant:
		print c
	return

matched_clubs('outdoor sports')