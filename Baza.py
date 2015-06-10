# importamo potrebne module
import sqlite3
import time


# klasa zaduzena za rad s bazom podataka
class Baza:


    """ Konstruktor
    
    Instancira klasu Baza.py, stvara konekciju sa SQLite bazom podataka, zapocinje puzanje po Internetu
    
    Args:
        imeBaze (string): ime zeljene baze
    """
    def __init__(self, imeBaze=''):
	
		# nova baza
		novaBaza = True if imeBaze == '' else False

		# generiramo nasumicno ime baze
		if novaBaza:
            
			# nasumicno ime
			imeBaze = 'db/' + (str(time.time()).replace('.', '_')) + ".db"
    
		# spajanje
		self.__con = sqlite3.connect(imeBaze)
        
		# napravimo tablice
		if novaBaza:
			
			self.stvoriTablice()


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
        self.__con.execute('DELETE FROM Rijec')
        self.posalji()
        
        self.__con.execute('VACUUM')
        self.posalji()
    
	
	# pretrazi bazu
    def pretrazi(self, rijeci):
		
        sql_select = "SELECT Stranica.adresa, "
        sql_from = "FROM Stranica, "
        sql_where = "WHERE "
		
        b = 0
        for rijec in rijeci:
	
            sql_select += "r" + str(b) + ".pozicija, "
            sql_from += "Rijec r" + str(b) + ", "
	
            sql_where += "r" + str(b) + ".rijec = ? AND Stranica.stranicaID = r" + str(b) + ".adresa AND "

            if b > 0:
                sql_where += "r" + str(b) + ".adresa = r" + str(b-1) + ".adresa AND "

            b += 1

        sql_kompletan = sql_select[:-2] + " " + sql_from[:-2] + " " + sql_where[:-5]

        return self.__con.execute(sql_kompletan, [unicode(x) for x in rijeci])
		
    
    
    # izvrsi na bazu
    def izvrsi(self, upit, args = None):
        
        if args == None:
        
            return self.__con.execute(upit)
            
        else:
            
            return self.__con.execute(upit, args)
        
    
    # struktura baze
    def stvoriTablice(self):
        
        self.izvrsi('CREATE TABLE Stranica(stranicaID INTEGER PRIMARY KEY, adresa TEXT, naslov TEXT, datumPobiranja REAL)')
        self.izvrsi('CREATE TABLE Rijec(rijecID INTEGER PRIMARY KEY, rijec TEXT, pozicija INTEGER, adresa INTEGER)')
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
    def dodajStranicu(self, adresa, naslov):
        
        self.__con.execute('INSERT INTO Stranica(adresa, naslov, datumPobiranja) VALUES (?, ?, ?)', [unicode(adresa), unicode(naslov), time.time()])
        self.posalji()
    
    
    
    # dodaj rijec u bazu
    # pozicija nije neka egzaktna mjera pozicije rijeci u dokumentu, vec je redni broj iteracije u dokumentu
    def dodajRijec(self, rijec, pozicija, adresa):
        
        self.__con.execute('INSERT INTO Rijec(rijec, pozicija, adresa) VALUES (?, ?, ?)', [unicode(rijec), unicode(pozicija), adresa])
        self.posalji()
        
       
    # vraca ID stranice ako ona postoji u bazi
    def stranicaID(self, adresa):
        
        # upit
        upit = self.__con.execute('SELECT stranicaID FROM Stranica WHERE adresa = ?', [unicode(adresa)]).fetchall()
        
        # ako postoji podataka
        if len(upit) == 1:
            
            # vratimo vrijednost
            return upit[0][0]
            
            
        # vratimo pogresku
        return -1
             
         
    # dodaj poveznicu
    def dodajPoveznicu(self, izvor, smjer):
        
        # dodamo poveznicu na bazi
        self.__con.execute('INSERT INTO Poveznica(izvor, smjer) VALUES (?, ?)', (unicode(izvor), unicode(smjer)))
        self.posalji()
		
		
        
if __name__ == '__main__':
    
    db = Baza()
    #db.stvoriTablice()
    #db.isprazni()
    
    #rez = db.izvrsi('SELECT naslov FROM Stranica')
    #rez = db.izvrsi('SELECT rijec FROM Rijec')
    rez = db.izvrsi('SELECT Rijec.rijec, Rijec.pozicija, Stranica.adresa FROM Rijec INNER JOIN Stranica ON Rijec.adresa = Stranica.stranicaID WHERE Rijec.rijec = ? LIMIT 20', [unicode('fakultetu')])
    
    rez = rez.fetchall()
    print len(rez)
    
    for red in rez:
        
        print red
    