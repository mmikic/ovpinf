# importamo potrebne module
import sqlite3


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
    
    # izvrsi na bazu
    def izvrsi(self, upit):
        
        return self.__con.execute(upit)
        
    
    # struktura baze
    def stvoriTablice(self):
        
        #self.izvrsi('create table Stranica(stranicaId, adresa, naslov, datumPobiranja)')
        #self.izvrsi('create table Poveznica(poveznicaId, stranicaId, )')
        self.izvrsi('CREATE TABLE Poveznica(poveznicaId INTEGER PRIMARY KEY, izvor TEXT, smjer TEXT)')
        self.posalji()
    
    
    # dodaj poveznicu
    def dodajPoveznicu(self, izvor, smjer):
        
        # dodamo poveznicu na bazi
        self.__con.execute('INSERT INTO Poveznica(izvor, smjer) VALUES (?, ?)', (unicode(izvor), unicode(smjer)))
        self.posalji()
        
        
        
if __name__ == '__main__':
    
    db = Baza()
    #db.stvoriTablice()
    
    
    
    
    rez = db.izvrsi('SELECT * FROM Poveznica')
    rez = rez.fetchall()
    
    for red in rez:
        
        print red