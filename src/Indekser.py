# ucitamo potrebne module
from bs4 import BeautifulSoup
import re
import text_hr
from Poveznica import Poveznica


""" Indekser.py klasa za Indeksiranje sadrzaja jedne stranice """

class Indekser:
       
        
    """ Konstruktor
    
    Prima instancu Stranica, dakle izvorni kod stranice i indeksira njen sadrzaj, opojavnicuje tekst, pronalazi poveznice 
    i iz njih stvara instancira Poveznia
    
    Args:
        stranica (Stranica): instanca klase Stranica
        adresa (Poveznica): instanca klase Poveznica
        baza (Baza): instanca klase Baza
        lokali (list of strings): lista adresa unutar kojih se stranica mora nalaziti
        iznimke (list of strings): lista adresa koje se nece posjecivati
    """
    def __init__(self, stranica, adresa, baza, lokali=[], iznimke=[]):
        
        # pospremimo objekte
        self.stranica = stranica
        self.adresa = adresa
        self.baza = baza
        
        # pospremimo lokale i iznimke
        self.lokali = lokali
        self.iznimke = iznimke

        # pospremimo juhu
        self.juha = self.skuhajJuhu()
        
        # pohranimo stranicu
        self.baza.dodajStranicu(self.adresa.url, self.juha.title.string)
        
        # indeksiramo stranicu
        self.sadrzaj()
    
    
    
    """ skuhajJuhu()
    
    Vraca objekt BeautifulSoup4 modula za lakse manipuliranje DOM-om
    
    Returns:
        BeautifulSoup
    """
    def skuhajJuhu(self):
        
        # iz sadrzaja
        return BeautifulSoup(self.stranica.izvor)
    
    
    
    """ poveznice()
    
    Pronalazi poveznice na trenutnoj stranici i vraca listu objekata Pooveznica
    
    Returns:
        list of Poveznica
    """
    def poveznice(self):
        
        # dohvatimo poveznice
        sirove_poveznice = self.juha('a')
        
        # vratimo listu objekata
        return [Poveznica(poveznica, self.adresa, self.lokali, self.iznimke) for poveznica in sirove_poveznice]
        
        
		
	"""
	
		Iskljucuje elemente koji su unutar CSS-a i sl.
		Preuzeto: http://www.quora.com/How-I-can-extract-only-text-data-from-HTML-pages
	"""
    def iskljucno(self, element):		
		
        if element.parent.name in ['style', 'script', '[document]', 'head']:
            return False
		
        elif re.match(r'a href=".*?" rel=".*?" title=".*?', str(element.encode('utf8').strip()), re.UNICODE|re.DOTALL):
            return False
		
        return True
    
    
    """ opojavnici()
    
    Opojavnicuje sadrzaj stranice na rijeci i vraca listu rijeci
    
    Returns:
        list of strings 
    """
    def opojavnici(self):
        
        # spremimo iskljucivo tekst stranice, bez ocuvanja semantickih elemenata
		sadrzaj = self.juha.findAll(text=True)
		
		# profiltriramo
		sadrzaj = filter(self.iskljucno, sadrzaj)
        
		# razdvojimo na rijeci
        #rijeci = re.findall(r'\w+', sadrzaj, re.UNICODE|re.DOTALL)
        # [^\W\d_]
		rijeci = re.findall(r'[^\W\d_]+', ",".join(sadrzaj), re.UNICODE|re.DOTALL)
        
        # vratimo listu rijeci
		return rijeci
        
       
       
    """ sadrzaj()
    
    Zapisuje sadrzaj stranice u bazu podataka
    
    Returns:
        void
    """
    def sadrzaj(self):
        
        # saznamo id stranice
        stranicaID = self.baza.stranicaID(self.adresa.url)
        
        # lista rijeci
        rijeci = self.opojavnici()
        
        # dohvatimo stop rijeci
        stop_rijeci = [redak[0] if redak[5] == None else redak[5] for redak in text_hr.get_all_std_words()]
        
        # pohranimo svaku rijec
        for k in range(len(rijeci)):
            
            # preskocimo stop rijeci
            if rijeci[k] not in stop_rijeci:
                
                # pohranimo u bazu
                self.baza.dodajRijec(rijeci[k].strip().lower(), k, int(stranicaID))
                
                
   
# testiranje
             
if __name__ == "__main__":
    
    """import urllib2
    
    adresa = "http://www.ffzg.unizg.hr"
    sadrzaj = urllib2.urlopen(adresa).read().decode('utf8')
    
    juha = BeautifulSoup(sadrzaj)
    
   
	rijeci = re.findall(r'[^\W\d_]+', ",".join(result), re.UNICODE|re.DOTALL)
    
    print rijeci[-40:]"""