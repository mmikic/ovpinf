# ucitamo potrebne module
"""from bs4 import BeautifulSoup
import urllib2

juha = BeautifulSoup(urllib2.urlopen("http://ffzg.unizg.hr").read())

print juha.get_text()"""

from text_hr import get_all_std_words

print get_all_std_words()[0]