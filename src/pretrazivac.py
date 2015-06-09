import re
import sqlite3

db = sqlite3.connect("db/1433846220_6.db")

stop = False

while stop == False:

	upit = raw_input("Upisite pojam za pretrazivanje: ")
	
	if upit.strip() != "":
	
		 stop = True
		 

print "Pretrazujemo za pojam: " + upit
print "----" * 10

sql_select = "SELECT Stranica.adresa, "
sql_from = "FROM Stranica, "
sql_where = "WHERE Stranica.stranicaID = r0.adresa AND "

rijeci = re.findall(r'[^\W\d_]+', upit, re.UNICODE|re.DOTALL)
b = 0
for rijec in rijeci:
	
	sql_select += "r" + str(b) + ".pozicija, "
	sql_from += "Rijec r" + str(b) + ", "
	
	sql_where += "r" + str(b) + ".rijec = ? AND "
	
	if b > 0:
		sql_where += "r" + str(b) + ".adresa = r" + str(b-1) + ".adresa AND "

	b += 1

sql_kompletan = sql_select[:-2] + " " + sql_from[:-2] + " " + sql_where[:-5]
rez = db.execute(sql_kompletan, [unicode(x) for x in rijeci])


def unificirajVrijednosti(vrijednosti):
	
	rangirano = dict()
	
	for skup in range(len(vrijednosti)):
		
		for stranica in vrijednosti[skup]:
			
			if stranica not in rangirano:
				
				rangirano[stranica] = 0
			
			rangirano[stranica] += vrijednosti[skup][stranica]
			
	return rangirano
			

def uvediKoeficijent(rjecnik, koeficijent):
	
	return dict([(stranica, vrijednost * koeficijent) for (stranica, vrijednost) in rjecnik.items()]) 


# str 66.
def normalizacijaVrijednosti(rjecnik, tezi=0):
	
	if tezi == 0:
		
		minimum = min(rjecnik.values())
		return dict([(stranica, float(minimum)/max(0.00001, vrijednost)) for (stranica, vrijednost) in rjecnik.items()]) 
		
	else:
		
		maksimum = max(rjecnik.values())
		return dict([(stranica, float(vrijednost)/maksimum) for (stranica, vrijednost) in rjecnik.items()]) 
		

def pozicijskaDistribucija(rjecnik):
	
	povrat = dict()
	
	for stranica in rjecnik:
		
		povrat[stranica] = [sum(vrijednost)/len(vrijednost) for vrijednost in rjecnik[stranica].values()]
		povrat[stranica] = sum(povrat[stranica])/len(povrat[stranica])
	
	return povrat


def frekvencijskaDistribucija(rjecnik):
	
	povrat = dict()
	
	for stranica in rjecnik:
		
		povrat[stranica] = sum([len(vrijednost) for (kljuc, vrijednost) in rjecnik[stranica].items()])
	
	return povrat
	

def pretvoriURjecnik(rezultat, rijeci):
	
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
	

rjecnik = pretvoriURjecnik(rez.fetchall(), rijeci)

frekvencijska_distribucija = uvediKoeficijent(normalizacijaVrijednosti(frekvencijskaDistribucija(rjecnik), 1), 1.65)
pozicijska_distribucija = uvediKoeficijent(normalizacijaVrijednosti(pozicijskaDistribucija(rjecnik)), 1.35)
	
rang = unificirajVrijednosti([frekvencijska_distribucija, pozicijska_distribucija])
rang = sorted(rang.items(), key=lambda x: -x[1])

print rang[0]

"""rez = rez.fetchall()
print "Broj rezultata: " + str(len(rez))
print "----" * 10

for red in rez:
    
    print red"""