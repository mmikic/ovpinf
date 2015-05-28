""" Puzac.py klasa za puzanje Internet stranicama """


class Puzac:
    
    # pohranimo neke predefinirane postavke
    self.maksimalnaDubina = 10
    self.lokalno = True
    
    
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
        if dubina < self.maksimalnaDubina and adresa not in self.posjeceneAdrese:
            
            # dodamo ju na popis posjecenih adresa, neovisno o tome hoce li posjet biti uspjesan ili ne
            self.posjeceneAdrese.append(adresa)
            
            # namjestimo praznu listu poveznica koju cemo napuniti ako se pronadu nove poveznice
            poveznice = []
            
            # pokusamo posjetiti
            try:
                
                # pohranimo instancu klase Stranica u varijablu sadrzaj kojoj proslijedimo instancu klase Poveznica
                sadrzaj = Stranica(adresa)
                
                # indeksiramo instancu klase Stranica
                podaci = Indeksiraj(sadrzaj)
                
                # pohranimo sve poveznice aktualne stranice, postaje lista instanci klase Poveznica
                poveznice = podaci.poveznice()
                
            # u slucaju pogreske, javimo
            except:
                
                # preskocimo problem
                print "Neuspjesno puzanje po stranici"
                pass
        
        
            # postupak ponovimo za svaku poveznicu
            for poveznica in poveznice:
                
                # rekurzivno pozovemo metodu 
                puz(poveznica, dubina=(dubina+1))
                
                
        