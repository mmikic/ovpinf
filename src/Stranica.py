# importamo potrebne module
import urllib2


""" Stranica.py klasa za ucitavanje Internet stranice """
class Stranica: 
    
    
    """ Konstruktor
    
    Instancira klasu Baza.py, stvara konekciju sa SQLite bazom podataka, zapocinje puzanje po Internetu
    
    Args:
        adresa (Poveznica): instanca klase Poveznica
        izvor (string): izvorni kod stranice
    """ 
    def __init__(self, adresa, izvor = False):
        
        # pohranimo url
        self.adresa = adresa
        
        # izvori
        if izvor != False:
            self.izvor = izvor
        
        else:
            self.izvor = self.dohvatiIzvor()
    


    """ dohvatiIzvor()
    
    Pokusa dohvatiti izvorni kod stranice i provjerava je li stranica dostupna (HTTP response 200), te je li content-type HTML
    
    Returns:
        string
    """
    def dohvatiIzvor(self):
        
        # pokusajmo ucitati stranicu
        try: 
            
            # napisemo zahtjev
            zahtjev = urllib2.Request(self.adresa.url)
            zahtjev.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
            
            # pokusamo dohvatiti sadrzaj
            odgovor = urllib2.urlopen(self.adresa.url)
            
            # ako je sve u redu
            if odgovor.getcode() == 200 and odgovor.info()['Content-Type'].split(';')[0] == 'text/html':
                
                # ucitaj izvorni kod
                return odgovor.read().decode('utf8')
            

        except:
            
            print "Pogreska prilikom ucitavanje stranice na adresi: " + self.url
            raise