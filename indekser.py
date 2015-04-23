# ucitamo potrebne module
import urllib2
from bs4 import BeautifulSoup as bs
from urlparse import urljoin

class Poveznica:
    
    def __init__(self, poveznica):
        
        self.poveznica = "Jedna poveznica"


class Stranica: 
    
    def __init__(self, poveznica):
        
        # namjestimo
        self.izvor = ""
        self.poveznice = []
        
        self.juha
        
        # pohranimo url
        self.url = poveznica
        
        self.dohvatiIzvor()
        self.dohvatiPoveznice()
        

    # metoda koja ucitava izvorni kod starnice
    def dohvatiIzvor(self):
        
        # pokusajmo ucitati stranicu
        try: 
            
            # ucitaj izvorni kod
            self.izvor = urllib2.urlopen(self.url.read())
            self.juha = bs(self.izvor)
            
        except:
            
            print "Pogreska"
        

    
    # metoda koja vraca popis poveznica na stranici
    def dohvatiPoveznice(self):
        
        # pronadjemo poveznice 
        # ne pronalazi juhu
        
        # prodjemo kroz svaku poveznicu
        for a in poveznice: 
            
            # instanciramo novu poveznicu i pohranimo ju
            self.poveznice.append(Poveznica(a))
        
        


stran = Stranica("http://ffzg.unizg.hr")
print stran.__poveznice



"""
Klasa za indeksiranje sadrzaja
"""
"""class Indekser:
    

    # Inicijalizacija 
    def __init__(self, poveznice):
    
        # malo vizualne magije ~~~~~
        print "Pocetak"
        
        
        # za svaku poveznicu u listi poveznica pokrenemo pretrazivanje
        for poveznica in poveznice:
            
            # pretrazi poveznicu
            self.stranica(poveznica)



nesto = Indekser(['http://ffzg.unizg.hr'])"""