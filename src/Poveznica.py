# pozovemo potrebne module
import urlparse
import re


# Klasa Poveznica predstavlja jedinku poveznice
class Poveznica:
    
    
    # prima cvor beautifulSoup 
    def __init__(self, poveznica):
        
        self.naziv = poveznica.get_text()
        self.segment = urlparse.urlparse(poveznica.get('href'))
        self.url = poveznica.get('href')
        self.atributi = poveznica.attrs

    # cisti trailing slash    
    def pocistiKrajAdrese(self, adresa):
        
        return adresa[:-1] if len(adresa) > 0 and adresa[-1] == '/' else adresa
        
        
        
    # cisti www.    
    def pocistiWorldWideWeb(self, adresa):
        
        return adresa[4:] if len(adresa) > 0 and adresa[0:4] == 'www.' else adresa
        
        
        
    # metoda provjerava je li druga poveznica, koja se proslijedjuje kao argument metode, identicna
    def identicnaPoveznica(self, drugaPoveznica):
        
        if self.segment.netloc == '' and self.segment.path.split('/')[-1] == drugaPoveznica.path.split('/')[-1]:
            
            return True
    
        if (self.segment.netloc == drugaPoveznica.netloc) and (self.pocistiKrajAdrese(self.segment.path) == self.pocistiKrajAdrese(drugaPoveznica.path)) and (self.segment.params == drugaPoveznica.params) and (self.segment.query == drugaPoveznica.query):
            
            return True
            
        return False
        
        
        
    # metoda provjerava je li druga poveznica, koja se proslijedjuje kao argument metode, lokalna
    def lokalnaPoveznica(self, lokali):
        
        # ako opce nema netloc, onda je definitivno lokalna
        if self.segment.netloc == '':
            
            return True
        
        # maknemo www.
        adresa = self.pocistiWorldWideWeb(self.segment.netloc) 

        # prodjemo kroz sve lokale
        for lokal in lokali:
            
            # i provjerimo nalaze li se unutar zeljene adrese
            if lokal in adresa:
                
                return True

        return False