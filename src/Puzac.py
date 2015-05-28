""" Puzac.py klasa za puzanje Internet stranicama """

# ucitamo vanjske klase
from bs4 import BeautifulSoup
from Stranica import Stranica
from Indekser import Indekser
from Poveznica import Poveznica
from Baza import Baza


class Puzac:
    
    # pohranimo neke predefinirane postavke
    maksimalnaDubina = 10
    lokalno = True
    
    
    """ Konstruktor
    
    Instancira klasu Baza.py, stvara konekciju sa SQLite bazom podataka, zapocinje puzanje po Internetu
    
    Args:
        adresa (Poveznica): instanca klase Poveznica
        lokali (list of strings): lista adresa unutar kojih se stranica mora nalaziti
        iznimke (list of strings): lista adresa koje se nece posjecivati
    """
    def __init__(self, adresa, lokali = [], iznimke = []):
        
        # pohranimo lokale i iznimke
        self.lokali = lokali
        self.iznimke = iznimke
        
        # pohranimo instancu baze
        self.baza = Baza()
        
        # kreiramo praznu listu posjecenih stranica
        self.posjeceneAdrese = []
        
        # pokrenemo inicijalno indeksiranje za
        self.puz(adresa)
        
    
    
    """ Puze po Internetu
    
    Args:
        adresa (Poveznica): instanca klase Poveznica
        dubina (int): trenutna dubina na kojoj se puz nalazi
    """
    def puz(self, adresa, dubina=1):
        
        # ako je trenutna dubina manja od maksimalne i stranice vec nije posjecena
        if dubina < self.maksimalnaDubina and adresa.url not in self.posjeceneAdrese:
            
            # ispisemo nesto ipak da znamo sto se dogada
            print "<" + adresa.url + "> (D: " + str(dubina) + ")"
            
            # dodamo ju na popis posjecenih adresa, neovisno o tome hoce li posjet biti uspjesan ili ne
            self.posjeceneAdrese.append(adresa.url)
            
            # namjestimo praznu listu poveznica koju cemo napuniti ako se pronadu nove poveznice
            poveznice = []
            
            # pokusamo posjetiti
            try:
                
                # pohranimo instancu klase Stranica u varijablu sadrzaj kojoj proslijedimo instancu klase Poveznica
                sadrzaj = Stranica(adresa)
                
                # indeksiramo instancu klase Stranica
                podaci = Indekser(sadrzaj, adresa, self.baza, self.lokali, self.iznimke)
                
                # pohranimo sve poveznice aktualne stranice, postaje lista instanci klase Poveznica
                poveznice = podaci.poveznice()
                
            # u slucaju pogreske, javimo
            except:
                
                # preskocimo problem
                print "Neuspjesno puzanje po stranici"
                pass
        
            
            # postupak ponovimo za svaku poveznicu
            for poveznica in poveznice:
                
                # provjerimo je li vazeca poveznica
                if poveznica.ispravna():
                
                    # rekurzivno pozovemo metodu 
                    self.puz(poveznica, dubina=(dubina+1))
                    
                    

""" ispaljivanje rakete """
if __name__ == "__main__":
    
    # definiramo lokale i iznimke
    lokali = ['ffzg.hr', 'ffzg.unizg.hr']
    iznimke = ['czon.ffzg.hr', 'czon.ffzg.unizg.hr']
    
    # definiramo inicijalnu adresu
    inicijalnaAdresa = BeautifulSoup('<a href="http://www.ffzg.unizg.hr/">Filozofski fakultet Sveucilista u Zagrebu</a>')
    inicijalnaAdresa = inicijalnaAdresa('a')[0]
    
    # instanciramo incijalnu poveznicu
    inicijalnaPoveznica = Poveznica(inicijalnaAdresa, lokali=lokali, iznimke=iznimke)
    
    # javimo da krecemo
    print "Zapocinjem indeksiranje.."
    
    # zapocnemo puzanje
    Puzac(inicijalnaPoveznica, lokali, iznimke) 
    
    # javimo da je kraj
    print "Indeksiranje zavrseno"