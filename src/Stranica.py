# importamo potrebne module
import urllib2


# Predstavlja jedinicu Stranice
class Stranica: 
    
    # 
    def __init__(self, poveznica, izvor = False):
        
        # pohranimo url
        self.url = poveznica
        
        # izvori
        if izvor != False:
            self.izvor = izvor
        
        else:
            self.izvor = self.dohvatiIzvor()
    

    # metoda koja ucitava izvorni kod stranice
    def dohvatiIzvor(self):
        
        # pokusajmo ucitati stranicu
        try: 
            
            # napisemo zahtjev
            zahtjev = urllib2.Request(self.url)
            zahtjev.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
            
            # pokusamo dohvatiti sadrzaj
            odgovor = urllib2.urlopen(self.url)
            
            # ako je sve u redu
            if odgovor.getcode() == 200 and odgovor.info()['Content-Type'].split(';')[0] == 'text/html':
                
                # ucitaj izvorni kod
                return odgovor.read()
            

        except:
            
            print "Pogreska prilikom ucitavanje stranice na adresi: " + self.url
            raise