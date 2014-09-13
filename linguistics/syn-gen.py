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

'''harvest_all_clubs()'''

clubs = []
f = open('club_descriptions.txt')
for line in f.readlines():
	pair = (line[:-1]).split(' ::: ')
	clubs.append(pair)
f.close()

#print clubs

#Returns a set of the terms related to the passed term.
#Either synonyms or uncommon definition constituents.
def related_terms(term):
	pass

#Finds clubs in the club_descriptions.txt file whose definitions contain term
#Returns a set of the names of the relevant clubs.
def relevant_clubs(term):
	result = []
	for e in clubs:
		if term in e[0] or term in e[1]:
			result.append(e)
	return result

query = 'math'
print 'Clubs related to \"%s\":'%query
rel = relevant_clubs(query)
for c in rel:
	print c