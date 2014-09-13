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

'''harvest_all_clubs()'''

'''Clean up dictionary'''
'''
print 'Cleaning dictionary...'
print 'Reading in lines...'
f = open('cleaned_dict.txt','r')
lines = []
for x in f.readlines():
	line = ''
	for i in xrange(len(x)):
		if ord(line[i])<128: #Remove non-ASCII-compatible characters
			line += line[i]
	lines.append(line)
f.close()
'''

'''
print 'Writing out lines...'
f = open('cleaned_dict.txt','w')
for e in lines:
	if len(e)>2:
		f.write(e)
f.close()
print 'Dictionary cleaned.'
'''

'''End cleanup'''

#Print all entries found in the dictionary



clubs = []
f = open('club_descriptions.txt')
for line in f.readlines():
	pair = (line[:-1]).split(' ::: ')
	clubs.append(pair)
f.close()

#all_words = ' '.join([x[0]+' '+x[1] for x in clubs])
#print all_words

#print clubs

#Returns a set of the terms related to the passed term.
#Either synonyms or uncommon definition constituents.
def related_terms(term):
	result = [term]
	for e in term.split(' '):
		if e not in result:
			result.append(e)
	return result

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
	query = string.lower(query)
	q_rel = related_terms(query)
	print 'Terms related to \"%s\": %s.'%(query,q_rel)
	print '\nClubs containing these terms:'
	relevant = []
	for related in q_rel:
		for e in clubs:
			if related in string.lower(e[0]) or related in string.lower(e[1]):
				relevant.append(e)
		#relevant.append(relevant_clubs(related))
	for c in relevant:
		print c
	return relevant

#matched_clubs('fun trips')