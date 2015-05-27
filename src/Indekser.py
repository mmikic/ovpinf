# ucitamo potrebne module
import sys
from bs4 import BeautifulSoup
import re
import urlparse
import text_hr


# ucitamo vanjske klase
from Stranica import Stranica
from Poveznica import Poveznica
from Baza import Baza

class Puzac:
    
    # zapocnemo indeksiranje
    def __init__(self, pocetna, lokali = []):
        
        # lokalne adrese
        self.lokali = lokali
        
        # pospremimo inicijalnu adresu
        self.inicijalnaPoveznica = pocetna.poveznica
        
        # namjestimo bazu
        self.baza = Baza()
        
        # pokrenemo inicijalno indeksiranje
        self.baza.dodajStranicu(pocetna.stranica.url, pocetna.juha.title.string)
        self.indeksiraj(pocetna)
           
    
    # metoda odlucuje hocemo li posjetiti proslijedjenu adresu
    def dozvoljenaAdresa(self, adresa, lokalno=True):
        
        # ako je vec na popisu indeksiranih
        if self.baza.indeksiranaStranica(adresa.url):
            
            # nista od toga
            print "adresa je vec indeksirana"
            return False
        
        
        # ako je identicna poveznica, ne zelimo
        if adresa.identicnaPoveznica(self.inicijalnaPoveznica):
                    
            return False
        
            
        # ako protokol u startu nije http:// ili https://
        elif adresa.segment.netloc != '' and adresa.segment.scheme not in [unicode('http'), unicode('https')]:
                    
            #print "Krivi protokol";
            #print adresa.segment.scheme
            return False
        
        # ako je eksterna stranica u pitanju, a mi imamo ukljucenu samo lokalnu pretragu
        elif lokalno == True and adresa.lokalnaPoveznica(self.lokali) == False:
            
            return False
        
        else:
            
            #print "Sve ok"
            return True
            
    
    
    # zapisuje rijeci u bazu
    def sadrzaj(self, indekser):
        
        # id stranice
        stranicaID = self.baza.stranicaID(indekser.stranica.url)
        
        # lista rijeci
        rijeci = indekser.opojavnici()
        
        # dohvatimo stop rijeci
        stop_rijeci = [redak[0] if redak[5] == None else redak[5] for redak in text_hr.get_all_std_words()]
        
        # pohranimo svaku rijec
        for k in range(len(rijeci)):
            
            # preskocimo stop rijeci
            if rijeci[k] not in stop_rijeci:
                
                # pohranimo u bazu
                self.baza.dodajRijec(rijeci[k], k, int(stranicaID))
    
    
    
    # glavna metoda, indeksira stranice
    def indeksiraj(self, indekser, maksimalno=9, lokalno=True, dubina=1):
        
        # ispisemo dubinu
        print "==========================="
        print "Dubina: " + str(dubina)
        print "Stranica: " + str(indekser.stranica.url)
        print "==========================="
            
        #
        # indeksiranje samog sadrzaja
        # 
        self.sadrzaj(indekser)
        
        # provjerimo smijemo li uci nivo nize
        if dubina <= maksimalno:
            
            # dohvatimo sve poveznice
            poveznice = indekser.poveznice()
            
            # za svaku od tih poveznica, napravimo isto
            for novaStranica in poveznice:
                
                # popravimo problem s URL-om kod pravih lokalnih stranica
                if novaStranica.segment.netloc == '':
                
                    # iskrojimo putanju i samo nadodamo novu lokaciju
                    novaStranica.url = indekser.poveznica.scheme + "://" + indekser.poveznica.netloc + "/".join(indekser.poveznica.path.split("/")[:-1]) + "/" + novaStranica.url
                
                # provjerimo zelimo li to posjetiti
                if self.dozvoljenaAdresa(novaStranica):
                    
                    # pokusajmo ucitati novu stranicu
                    try:
                    
                        # posjetimo i ponovimo proceduru
                        stranica = Stranica(novaStranica.url)
                    
                        # dohvatimo metode
                        indeks = Indekser(Stranica(novaStranica.url))
                        self.baza.dodajStranicu(novaStranica.url, indeks.juha.title.string)
                        
                        # indeksiramo, ali povecamo dubinu
                        self.indeksiraj(indeks, dubina=(dubina+1))

                    except:
                        
                        print "Indeksiranje ne radi"
                        pass


# Klasa za indeksiranje sadrzaja jedne stranice
#
# Njen zadatak je indeksiranje sadrzaja jedne stranice, sto joj otvara metode poput traversanja kroz stablo i sve ostalo
class Indekser:
    
    def __init__(self, stranica):
        
        # pospremimo instancu stranice 
        self.stranica = stranica
        
        # pospremimo detalje njene poveznice
        self.poveznica = urlparse.urlparse(unicode(stranica.url))
        
        # pospremimo juhu
        self.juha = self.skuhajJuhu()
    
    
    # metoda vraca instancu BeautifulSoup modula za danu stranicu
    def skuhajJuhu(self):
        
        # iz sadrzaja
        return BeautifulSoup(self.stranica.izvor)
    
    
    
    # Vraca sve poveznice koje se nalaze u stranici
    def poveznice(self):
        
        # dohvatimo poveznice
        sirove_poveznice = self.juha('a')
        poveznice = [Poveznica(poveznica) for poveznica in sirove_poveznice] 
        
        # vratimo uredjeni par gdje je prva vrijednost lista poveznica, a druga broj poveznica
        return poveznice
    
    
    
    # razdvaja na rijeci
    def opojavnici(self):
        
        # spremimo iskljucivo tekst stranice, bez ocuvanja semantickih elemenata
        sadrzaj = self.juha.get_text()
        
        # razdvojimo na rijeci
        rijeci = re.findall(r'\w+', sadrzaj, re.UNICODE|re.DOTALL)
        
        # vratimo listu rijeci
        return rijeci


try:

    web = Stranica('http://www.ffzg.unizg.hr') # instanca klase Stranica
    #web = Stranica('http://lab.nemojkliknut.com/ovptest2/dok1.html') # instanca klase Stranica
    indeks = Indekser(web) # instanca klase Indekser koji prima objekt(Stranica)
    pretraga = Puzac(indeks, ['ffzg.unizg.hr', 'ffzg.hr'])
    #pretraga = Pretrazivac(indeks, ['lab.nemojkliknut.com'])
    
except:
    
    print sys.exc_info()[0]
    raise
    

print "****************"
print "Kraj indeksiranja"