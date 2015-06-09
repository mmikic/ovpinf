from Baza import Baza


stop = False

while stop == False:

	upit = raw_input("Upisite pojam za pretrazivanje: ")
	
	if upit.strip() != "":
	
		 stop = True
		 

print "Pretrazujemo za pojam: " + upit