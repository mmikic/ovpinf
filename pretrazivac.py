import re
from Baza import Baza

class Pretrazivac:
	
	
	""" Konstruktor
	
		pokrece pretrazivanje
		
		Args:
			imeBaze (string): naziv SQLite baze prema kojoj ce se pretrazivati
	"""
	def __init__(self, imeBaze):

		# pohranimo objekt Baze
		self.baza = Baza(imeBaze)
		
		# vrtimo se dok ne dobijemo zadovoljavajuci upit
		while True:

			# postavljamo pitanje
			upit = raw_input("Upisite pojam za pretrazivanje: ")
			if upit.strip() != "":
	
				# pretrazimo upit
				self.pretrazi(upit)
	
	
	""" pretrazi()
	
		pretrazuje bazu podataka prema zadanom upitu
	
		Args:
			upit (string): upit pretrage
	"""
	def pretrazi(self, upit):
	
		print "===" * 10
	
		# uredimo pojam pretrage
		rijeci = re.findall(r'[^\W\d_]+', upit.decode('utf8').lower(), re.UNICODE|re.DOTALL)
		
		# pretrazimo bazu
		rezultati = self.baza.pretrazi(rijeci)
		rezultati = rezultati.fetchall()
		
		# ako nema rezultata ispisemo poruku
		if len(rezultati) < 1:
			
			print "Nazalost nema rezultata za trazeni upit"
			
		# ako ima izvedemo cijeli sou program
		else:
		
			# formiramo pravilni rjecnik
			rjecnik = self.pretvoriURjecnik(rezultati, rijeci)
			
			# frekvencijska distribucija, normalizirana, s koeficijentom
			frek_distr = self.frekvencijskaDistribucija(rjecnik)
			frek_distr = self.normalizacijaVrijednosti(frek_distr, 1)
			frek_distr = self.uvediKoeficijent(frek_distr, 1.35)
			
			# pozicijska distribucija, normalizirana, s koeficijentom
			poz_distr = self.frekvencijskaDistribucija(rjecnik)
			poz_distr = self.normalizacijaVrijednosti(poz_distr)
			poz_distr = self.uvediKoeficijent(poz_distr, 1)
			
			# unificiramo vrijednosti u rangiranu listu rezultata
			rangirano = self.unificirajVrijednosti([frek_distr, poz_distr])
			rangirano = sorted(rangirano.items(), key=lambda x: -x[1])
			
			# ispisemo rezultate
			self.ispisiRezultate(rangirano)
	
	
	""" ispisiRezultate()
	
		ispisuje rangirane rezultate u konzolu
		
		Args:
			rangirano (list): lista rangiranih rezultata
			
		Return:
			void
	"""
	def ispisiRezultate(self, rangirano):
		
		for element in rangirano[:10]:
			
			print "<" + element[0] + ">"
			print "Relevantnost: " + str(element[1])
			print "---" * 10
	
	
	""" unificirajVrijednosti()
	
		spaja razlicite distribucije u konacni rezultat i generira konacnu ocjenu relevantnosti
		
		Args:
			vrijednosti (list): lista distribucija
			
		Return:
			dict: rangirani rezultat, bez poretka
	"""
	def unificirajVrijednosti(self, vrijednosti):
	
		rangirano = dict()
	
		for skup in range(len(vrijednosti)):
		
			for stranica in vrijednosti[skup]:
			
				if stranica not in rangirano:
				
					rangirano[stranica] = 0
			
				rangirano[stranica] += vrijednosti[skup][stranica]
			
		return rangirano

	
	""" uvediKoeficijent()
	
		za dani rjecnik umnaza vrijednosti s danimm koeficijentom
		
		Args:
			rjecnik (dict): rjecnik nad kojim se obradjuje
			koeficijent (float): koeficijent umnazanja
	
		Return:
			dict: izmjenjeni rjecnik
	"""
	def uvediKoeficijent(self, rjecnik, koeficijent):
	
		return dict([(stranica, vrijednost * koeficijent) for (stranica, vrijednost) in rjecnik.items()]) 



	""" normalizacijaVrijednosti()
	
		prima strogo definiran rjecnik u kojem su kljucevi adrese i vraca normaliziranu ocjenu u intervalu [0, 1]
		koncept preuzet iz knjige "Programming collective intelligence, str. 66.
		
		Args:
			rjecnik (dict): inicijalna distribucija prije normalizacije
			tezi(int): 0|1 definira prema kojoj vrijednosti rezultati moraju teziti, manjoj ili vecoj
		
		Return:
			dict: normalizirana distribucija
	"""
	def normalizacijaVrijednosti(self, rjecnik, tezi=0):
	
		# ako je cilj da vrijednost bude sto manja
		if tezi == 0:
		
			minimum = min(rjecnik.values())
			return dict([(stranica, float(minimum)/max(0.00001, vrijednost)) for (stranica, vrijednost) in rjecnik.items()]) 
		
		# ako je cilj da vrijednost bude sto veca
		else:
		
			maksimum = max(rjecnik.values())
			return dict([(stranica, float(vrijednost)/maksimum) for (stranica, vrijednost) in rjecnik.items()]) 
		
	
	""" pozicijskaDistribucija()
	
		prima rjecnik i modificira ga na nacin da zapise prosjecnu udaljenost svih relevantnih rijeci za jedan dokument
		
		Args:
			rjecnik (dict): inicijalni rjecnik
			
		Return:
			dict: ureden rjecnik cega
	"""
	def pozicijskaDistribucija(self, rjecnik):
	
		povrat = dict()
		for stranica in rjecnik:
		
			povrat[stranica] = [sum(vrijednost)/len(vrijednost) for vrijednost in rjecnik[stranica].values()]
			povrat[stranica] = sum(povrat[stranica])/len(povrat[stranica])
	
		return povrat



	""" frekvencijskaDistribucija()
	
		prima rjecnik i modificira ga na nacin da zapise ukupan broj pronadjenih relevantnih rijeci za jedan dokument
		
		Args:
			rjecnik (dict): inicijalni rjecnik
			
		Return:
			dict: ureden rjecnik cega
	"""
	def frekvencijskaDistribucija(self, rjecnik):
	
		povrat = dict()
		for stranica in rjecnik:
		
			povrat[stranica] = sum([len(vrijednost) for (kljuc, vrijednost) in rjecnik[stranica].items()])
	
		return povrat
	



	""" pretvoriURjecnik()
	
		prima SQLite rezultat i opojavniceni upit te generira specifican format rjecnika koji se dalje proslijedjuje metodama frekvencijskaDistribucija i pozicijskaDistribucija
		
		Args:
			rezultat (SQLite.fetchall()): rezultat upita na bazi
			rijeci (list of strings): popis pretrazenih rijeci
			
		Return:
			dict: ureden rjecnik
	"""
	def pretvoriURjecnik(self, rezultat, rijeci):
	
		povrat = dict()
		for x in range(len(rezultat)):
		
			#inicijalno
			if rezultat[x][0] not in povrat:
				povrat[rezultat[x][0]] = dict()
			
				for rijec in rijeci:	
					povrat[rezultat[x][0]][rijec] = list()
				
			# dodavanje vrijednosti
			for y in range(len(rijeci)):
			
				if rezultat[x][y+1] not in povrat[rezultat[x][0]][rijeci[y]]:
				
					povrat[rezultat[x][0]][rijeci[y]].append(rezultat[x][y+1])
		
		
		return povrat
		
	
# pokretanje pretrazivaca	
if __name__ == "__main__":
	
	pretrazivanje = Pretrazivac("db/1433846220_6.db")