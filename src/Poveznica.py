# pozovemo potrebne module
import urlparse
import re


""" Poveznica.py klasa prilagodbu i obradu poveznica """
class Poveznica:
    
    
    """ Konstruktor
    
    Instancira klasu Baza.py, stvara konekciju sa SQLite bazom podataka, zapocinje puzanje po Internetu
    
    Args:
        poveznica (BeautifulSoup <a> cvor): poveznica koju provjeravamo i krojimo
        izvornaPoveznica (Poveznica): izvorna poveznica s koje sve i dolazi
    """
    def __init__(self, poveznica, izvornaPoveznica):
        
        # pohranimo izvornu poveznicu
        self.izvorno = izvornaPoveznica
        
        # pohranimo naziv poveznice 
        self.naziv = poveznica.get_text()
        
        # pohranimo ispravljenu punu putanju poveznice
        self.url = self.ispravi(poveznica.get('href'))
        
        # pohranimo atribute poveznice
        self.atributi = poveznica.attrs
        
        # pohranimo segmente poveznice
        self.segment = urlparse.urlparse(self.url)
       
        
    
    """ ispravi()
    
    Ispravlja adresu
    
    Args:
        adresa (string): adresa koja se ispravlja
    
    Return:
        adresa (string): ispravljena adresa
    """
    def ispravi(self, adresa):
        
        # uklonimo www.
        adresa = self.pocistiWorldWideWeb(adresa)
        
        # vratimo ispravljenu adresu
        return adresa
        
        
        
    
    
    """ provjeri()
    
    Provjerava je li vazeca adresa
    
    Return:
        bool
    """
    def provjeri(self):
        
     
        
    """ pocistiWorldWideWeb()
    
    Uklanja www. iz adrese
    
    Args:
        adresa (string): adresa iz koje se treba ukloniti www. ako postoji
    
    Return:
        adresa (string): prociscena adresa
    """ 
    def pocistiWorldWideWeb(self, adresa):
        
        # procisti i vrati
        return adresa.replace('www.', '')
        
        # filtriraj i vrati
        #return adresa[4:] if len(adresa) > 0 and adresa[0:4] == 'www.' else adresa
        
    
    
    """ lokalnaPoveznica()
    
    Provjerava je li adresa lokalna
    
    Args:
        lokali (list of strings): lista adresa unutar koje mora biti
    
    Return:
        bool
    """
    def lokalnaPoveznica(self, lokali):
        
        # prodjemo kroz sve lokale
        for lokal in lokali:
            
            # i provjerimo nalaze li se unutar zeljene adrese
            if lokal in self.segment.netloc:
                
                # ako je, vratimo True i zavrsimo petlju
                return True

        # ako nije, na kraju iteracije kroz petlju vratimo False
        return False
    
    
    
    """ zabranjenaPoveznica()
    
    Provjerava je li adresa na popisu zabranjenih
    
    Args:
        zabranjene (list of strings): lista adresa unutar koje mora biti
    
    Return:
        bool
    """
    def zabranjenaPoveznica(self, zabranjene):
        
        # prodjemo kroz sve zabranjene adrese
        for zabranjena in zabranjene:
            
            # i provjerimo nalaze li se unutar zeljene adrese
            if zabranjena in self.segment.netloc:
                
                # ako je, vratimo True i zavrsimo petlju
                return True

        # ako nije, na kraju iteracije kroz petlju vratimo False
        return False
    
    
        
    """ identicnaPoveznica()
    
    Provjerava je li adresa identicna izvornoj adresi
    
    Return:
        bool
    """
    def identicnaPoveznica(self):
        
        #if self.segment.netloc == '' and self.segment.path.split('/')[-1] == drugaPoveznica.path.split('/')[-1]:
            
            #return True
    
        #if (self.segment.netloc == drugaPoveznica.netloc) and (self.pocistiKrajAdrese(self.segment.path) == self.pocistiKrajAdrese(drugaPoveznica.path)) and (self.segment.params == drugaPoveznica.params) and (self.segment.query == drugaPoveznica.query):
        if self.segment == self.izvorno.segment:
            
            # potvrdimo da je
            return True
            
        # potvrdimo da nije
        return False
        
        
        
""" 
Testiranje
"""    
if __name__ == '__main__':
    
    # pozovemo BS4
    from bs4 import BeautifulSoup
    
    # stvorimo juhu
    juha = BeautifulSoup('<a href="http://www.web.index.hr/info/about">Index link</a>')
    link = juha('a')
    
    # instanciramo poveznicu
    poveznica = Poveznica(link[0])