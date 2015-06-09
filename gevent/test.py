import urllib2
from time import time

"""import gevent
from gevent import monkey"""
# napisemo zahtjev
"""ms['prereq'] = time()
zahtjev = urllib2.Request('http://ffzg.unizg.hr/?p=2663')
ms['request'] = time()
zahtjev.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
ms['header'] = time()

# pokusamo dohvatiti sadrzaj
odgovor = urllib2.urlopen(zahtjev)
ms['resp'] = time()

# ako je sve u redu
if odgovor.getcode() == 200 and odgovor.info()['Content-Type'].split(';')[0] == 'text/html':
    
    print ms
    
    # ucitaj izvorni kod
    #return odgovor.read().decode('utf8')




"""

def otvori(adresa):
    
    ms = {}
    ms['start'] = time()
    try:
    
        odgovor = urllib2.urlopen(adresa, timeout=5)
        ms['after'] = time()

    except:
    
        print "Error"
        ms['after'] = time()

    
    print "Adresa: " + adresa
    for s in ms:
    
        print s, str(ms[s]-ms['start']) + "s"
        
    print "....."
        
        
adrese = ['http://ffzg.unizg.hr', 'http://wp.ffzg.unizg.hr', 'http://net.hr', 'http://www.ffzg.unizg.hr/files/019746_1.doc']
for adresa in adrese:
    
    otvori(adresa)