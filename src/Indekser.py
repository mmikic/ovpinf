# ucitamo potrebne module
import sys
from bs4 import BeautifulSoup
import re
import urlparse


# ucitamo vanjske klase
from Stranica import Stranica
from Poveznica import Poveznica
from Baza import Baza

class Pretrazivac:
    
    # zapocnemo indeksiranje
    def __init__(self, pocetna, lokali = []):
        
        # lokalne adrese
        self.lokali = lokali
        
        # pospremimo inicijalnu adresu
        self.inicijalnaPoveznica = pocetna.poveznica
        
        # namjestimo bazu
        self.baza = Baza()
        
        # pokrenemo inicijalno indeksiranje
        self.indeksiraj(pocetna)
        self.baza.dodajUIndeks(pocetna.stranica.url, pocetna.juha.title.string)
           
    
    # metoda odlucuje hocemo li posjetiti proslijedjenu adresu
    def dozvoljenaAdresa(self, adresa, lokalno=True):
        
        # ako je vec na popisu indeksiranih
        if self.baza.indeksiranaStranica(adresa.url):
            
            # nista od toga
            print "adresa je vec indeksirana"
            return False
        
        
        # ako je identicna poveznica, ne zelimo
        if adresa.identicnaPoveznica(self.inicijalnaPoveznica):
                    
            print "Ista adresa"
            #print adresa.segment
            return False
        
            
        # ako protokol u startu nije http:// ili https://
        #elif adresa.segment.scheme not in [unicode('http'), unicode('https')]:
                    
            #print "Krivi protokol";
            #print adresa.segment.scheme
         #   return False
        
        # ako je eksterna stranica u pitanju, a mi imamo ukljucenu samo lokalnu pretragu
        elif lokalno == True and adresa.lokalnaPoveznica(self.lokali) == False:
            
            print "Adresa nije lokalna, konkretno"
            #print adresa.segment
            return False
        
        else:
            
            #print "Sve ok"
            return True
            
    
    # glavna metoda, indeksira stranice
    def indeksiraj(self, indekser, maksimalno=3, lokalno=True, dubina=1):
        
        # ispisemo dubinu
        print "==========================="
        print "Dubina: " + str(dubina)
        print "Stranica: " + str(indekser.stranica.url)
        print "==========================="

        # dodamo na popis indeksiranih
        #self.indeksirano.add(indekser.stranica.url)
            
        #
        # indeksiranje samog sadrzaja
        # // naknadno //
        # 
        
        
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
                    
                    # pohranimo poveznicu u bazu
                    #self.baza.dodajPoveznicu(indekser.stranica.url, novaStranica.url)
                
                    # pokusajmo ucitati novu stranicu
                    try:
                    
                        # posjetimo i ponovimo proceduru
                        stranica = Stranica(novaStranica.url)
                    
                    except:
                    
                        # ispisemo da je bilo problema
                        print "Doslo je do pogreske prilikom ucitavanja stranice"
                    
                        # preskocimo problem
                        pass
                        
                        
                    # pokusamo ucitati indekser na stranicu
                    try:
                    
                        # dohvatimo metode
                        indeks = Indekser(Stranica(novaStranica.url))
                        self.baza.dodajUIndeks(novaStranica.url, indeks.juha.title.string)
                        
                        
                    except:
                        
                        print "Indekser ne radi"
                        #print sys.exc_info()[0]
                        pass
                    

                    # pokusamo indeksirati
                    try:
                        
                        # indeksiramo, ali povecamo dubinu
                        self.indeksiraj(indeks, dubina=(dubina+1))

                    except:
                        
                        print "Indeksiranje ne radi"
                        pass

        else:
            
            print "preduboko si"


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
        


try:

    web = Stranica('http://lab.nemojkliknut.com/ovptest/dok1.html') # instanca klase Stranica
    #web = Stranica('http://fer.unizg.hr') # instanca klase Stranica
    indeks = Indekser(web) # instanca klase Indekser koji prima objekt(Stranica)
    #pretraga = Pretrazivac(indeks, ['ffzg.unizg.hr', 'ffzg.hr'])
    pretraga = Pretrazivac(indeks, ['lab.nemojkliknut.com'])
    
except:
    
    print sys.exc_info()[0]
    raise
    

print "****************"
print "Kraj indeksiranja"