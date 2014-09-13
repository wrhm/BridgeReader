#club_scraper.py
#Scrapes pages of CMU's site TheBridge to harvest names and descriptions of clubs and
#student organizations.

from bs4 import BeautifulSoup
import requests

def page_specific_url(n):
	return 'https://thebridge.cmu.edu/organizations?SearchType=None&SelectedCategoryId=0&CurrentPage=%d'%n

#Returns a string containing the html source of the nth page of org results.
def get_html(n):
	return BeautifulSoup(requests.get(page_specific_url(n)).text)

def get_club_details_from_page(n):
	gh = get_html(n)
	clubs = []
	for tag in gh.find_all('div', class_='result clearfix'):
		club_name = (tag.h5.contents[1].contents)[0]
		club_description = (tag.p.contents)[0]

		#Replace non-ascii characters with spaces
		vcn  = '' #validated club name
		for i in xrange(len(club_name)):
			if ord(club_name[i])<0 or ord(club_name[i])>127:
				vcn += ' '
			else:
				vcn += club_name[i]

		#Replace non-ascii characters with spaces
		vcd = '' #validated club description
		for i in xrange(len(club_description)):
			if ord(club_description[i])<0 or ord(club_description[i])>127:
				vcd += ' '
			elif str(club_description[i]) in '\n\r': #Deletes erroneously blank line entries
				vcd += ''
			else:
				vcd += club_description[i]
		clubs.append([str(vcn),str(vcd)])
	return clubs

#Finds the lowest valid page number for the last page of results.
#Now correct but unneeded; harvest_all_clubs now does the calculation internally,
#improving efficiency.
def max_page_num():
	old_data = get_club_details_from_page(1)
	n = 2
	new_data = get_club_details_from_page(n)
	while not (new_data == old_data):
		old_data = new_data
		n += 1
		new_data = get_club_details_from_page(n)
	return n-1

#Determines highest page number, then scrapes pages for club names and
#descriptions, writing them to club_descriptions.txt.
def harvest_all_clubs():
	print 'Harvesting club data...'
	#print 'Calculating mpn...'
	#mpn = max_page_num()
	#print 'Determined mpn = %d'%mpn
	clubs = []
	page_list = ' '
	last_page_list = ''
	#for page in xrange(mpn+1):
	page = 0
	while not page_list == last_page_list: #rephrased loop condition to omit need for max_page_num. (now faster)
		last_page_list = page_list
		page += 1
		page_list = get_club_details_from_page(page)
		for c in page_list:
			if c not in clubs:
				clubs.append(c)
		#print 'Done scraping page %d.'%page
	f = open('club_descriptions.txt','w')
	##print '\n All clubs:'
	#for c in clubs:
	for w in xrange(len(clubs)):
		##print c
		f.write('%s ::: %s'%(clubs[w][0],clubs[w][1]))
		if w<len(clubs)-1:
			f.write('\n')
	f.close()
	#print '\nTotal clubs found/written: %d'%len(clubs)
	print 'Found %d clubs on %d pages.'%(len(clubs),page-1)