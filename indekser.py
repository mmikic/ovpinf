# ucitamo potrebne module
import urllib2
from bs4 import BeautifulSoup
import urlparse
import re

class Poveznica:
    
    def __init__(self, poveznica):
        
        self.naziv = poveznica.get_text()
        self.url = urlparse.urlparse(poveznica.get('href'))
        self.atributi = poveznica.attrs
        
    # metoda provjerava je li druga poveznica, koja se proslijedjuje kao argument metode, identicna
    def identicnaPoveznica(self, drugaPoveznica):
        
        if (self.url.netloc == drugaPoveznica.netloc) and (self.url.path == drugaPoveznica.path) and (self.url.params == drugaPoveznica.params) and (self.url.query == drugaPoveznica.query):
            
            return True
            
        return False 


class Stranica: 
    
    def __init__(self, poveznica, izvor = False):
        
        # pohranimo url
        self.url = poveznica
        
        # izvori
        if izvor != False:
            self.izvor = izvor
        
        else:
            self.izvor = self.dohvatiIzvor()
        
        #self.dohvatiPoveznice()
        

    # metoda koja ucitava izvorni kod starnice
    def dohvatiIzvor(self):
        
        # pokusajmo ucitati stranicu
        try: 
            
            # ucitaj izvorni kod
            return urllib2.urlopen(self.url).read()

            
        except:
            
            print "Pogreska"
        
    # 
   # def rijeci(self):
        
        """rijeci = self.juha.body.find_all(text=True, recursive=True)
        
        for rijec in rijeci: 
            
            print rijec
        
        print "------------------------------------------------------------------------------------------"
        
        print self.juha.body.get_text()"""
        
        
    # metoda rastavlja stranicu na pojedinacne rijeci
    def rijeci(self):
        
        # dohvatimo sadrzaj svakog cvora (BeautifulSoup nam daje listu vrijednosti cvorova)
        cvorovi = self.juha.body.find_all(self.dozvoljeniElementi, text=True, recursive=True)

        for cvor in cvorovi:
            
            if cvor.parent.get_text() == cvor.get_text():
                
                print "E OVO JE POSTENO PODUDARANJE"
            
            print "<" + cvor.name + ">", cvor.get_text(), "</" + cvor.name + ">"
            print ""
        
        
        
        # prodjemo kroz svaki node i izvadimo rijeci
        for cvor in cvorovi:
            
            # razdvojimo recenice na rijeci
            rijeci = re.findall(r'\w+', cvor, re.UNICODE)
            
            # ako ima sadrzaja
            if len(rijeci) > 0:
                
                # prodjemo kroz svaku rijec
                for rijec in rijeci:
                    
                    # i rijec dodamo na listu pojavnica
                    self.pojavnice.append(rijec)


class Cvor:
    
    dozvoljeniElementi = ['body', 'p', 'a', 'strong', 'b', 'em', 'i', 'li',  'span', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'dt', 'dd', 'td', 'th', 'small', 'strike', 'cite', 'blockquote', 'addr', 'sub', 'sup', 'choco']
    linijskiElementi = ['b', 'big', 'i', 'small', 'tt', 'abbr', 'acronym', 'cite', 'dfn', 'em', 'kbd', 'strong', 'samp', 'var', 'a', 'bdo', 'q', 'span', 'sub', 'sup', 'label']
    semantickiElementi = ['b', 'strong', 'em', 'i']
    blokElementi = []
    
    def __init__(self, cvor, dubina=0):
        
        self.dubina = dubina
        self.maks_dubina = 0
        self.sadrzaj = cvor

        # juha 
        self.juha = self.skuhajJuhu()

    
    
    # skuhajmo juhu
    def skuhajJuhu(self):
        
        # iz sadrzaja
        return BeautifulSoup(self.sadrzaj)
    
    
    
    # Vraca sve poveznice koje se nalaze u cvoru
    def poveznice(self):
        
        # dohvatimo poveznice
        sirove_poveznice = self.sadrzaj('a')
        poveznice = [Poveznica(poveznica) for poveznica in sirove_poveznice] 
        
        # vratimo uredjeni par gdje je prva vrijednost lista poveznica, a druga broj poveznica
        return (poveznice, len(poveznice))
      
    #
    # metoda potrebna za indeksiranje, provjerava ima li trenutni cvor semanticku djecu
    #
    def imaSemantickuDjecu(self):
        
        if len(self.juha.find_all(self.semantickiElementi, recursive=False)) > 0:
            
            return True
        
        return False
        
    
    def djeca(self):
        
        #return [dijete for dijete in cvor.children]
        return [Cvor(dijete, self.dubina+1) for dijete in self.juha.find_all(self.dozvoljeniElementi, recursive=False)]



# prima instancu stranice     

class Indekser: 
    
    def __init__(self, stranica):
        
        # pohranimo izvorni kod stranice
        self.stranica = stranica
    

    
    



#izvorna_adresa = 'http://www.ffzg.unizg.hr/'
#izvorna_poveznica = urlparse.urlparse(izvorna_adresa)

strFilozofskog = Stranica('http://www.ffzg.unizg.hr/')
obicanCvor = Cvor(strFilozofskog.izvor)
bodyCvor = Cvor(obicanCvor.juha.body)
print bodyCvor.juha.find_all(bodyCvor.dozvoljeniElementi, recursive=False)



#indeks = Indekser(strFilozofskog)

#print indeks.juha.





#print indeks.djeca(indeks.djeca(indeks.djeca(indeks.tijelo())[0])[1])
#print indeks.imaSemantickuDjecu(indeks.djeca(indeks.djeca(indeks.djeca(indeks.tijelo())[0])[1])[0])


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