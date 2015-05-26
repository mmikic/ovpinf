# importamo potrebne module
import sqlite3
import time


# klasa zaduzena za rad s bazom podataka
class Baza:

	# konstruktor
    def __init__(self, imeBaze='db/poveznice.db'):
	
        # spajanje
        self.__con = sqlite3.connect(imeBaze)


    # destruktor
    def __del__(self):
        
        self.__con.close()
    
    #posalji na bazu
    def posalji(self):
        
        # nista ne vracamo
        self.__con.commit()
    
    
    # pocisti bazu
    def isprazni(self):
        
        self.__con.execute('DELETE FROM Stranica')
        self.posalji()
        
        self.__con.execute('VACUUM')
        self.posalji()
    
    
    # izvrsi na bazu
    def izvrsi(self, upit):
        
        return self.__con.execute(upit)
        
    
    # struktura baze
    def stvoriTablice(self):
        
        self.izvrsi('CREATE TABLE Stranica(stranicaID INTEGER PRIMARY KEY, adresa TEXT, naslov TEXT, datumPobiranja REAL)')
        #self.izvrsi('create table Poveznica(poveznicaId, stranicaId, )')
        #self.izvrsi('CREATE TABLE Poveznica(poveznicaId INTEGER PRIMARY KEY, izvor TEXT, smjer TEXT)')
        self.posalji()
    
    
    # provjera indeksiranosti
    def indeksiranaStranica(self, poveznica):
        
        rez = self.pretraziIndeks(poveznica)
        
        if len(rez.fetchall()) > 0:
            
            return True
            
        return False
    
    
    # pretraga stranice kao izvora
    def pretraziIndeks(self, pojam):
        
        return self.__con.execute("SELECT * FROM Stranica WHERE adresa=?", [unicode(pojam)])
        
    
    
    # dodaj u indeks
    def dodajUIndeks(self, poveznica, naslov):
        
        self.__con.execute('INSERT INTO Stranica(adresa, naslov, datumPobiranja) VALUES (?, ?, ?)', [unicode(poveznica), unicode(naslov), time.time()])
        self.posalji()
    
    
    
    # dodaj poveznicu
    def dodajPoveznicu(self, izvor, smjer):
        
        # dodamo poveznicu na bazi
        self.__con.execute('INSERT INTO Poveznica(izvor, smjer) VALUES (?, ?)', (unicode(izvor), unicode(smjer)))
        self.posalji()
        
        
        
if __name__ == '__main__':
    
    db = Baza()
    #db.stvoriTablice()
    #db.isprazni()
    
    rez = db.izvrsi('SELECT * FROM Stranica')
    #print db.indeksiranaStranica("http://www.ffzg.unizg.hr/vezes/")
    
    rez = rez.fetchall()
    
    for red in rez:
        
        print red