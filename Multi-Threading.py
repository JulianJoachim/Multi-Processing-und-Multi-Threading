import threading
import time

# Unsere Klasse für die Threads. Es wird eine Barriere gesetzt, in Größe der benötigten Threads.
class MyThread(threading.Thread):         
    
# Hier wird der Bereich dieses Threads instanziiert.
    def __init__(self, numberStart, numberEnd, barrier):
        threading.Thread.__init__(self)
        self.numberStart = numberStart
        self.numberEnd = numberEnd
        self.total = 1
        self.barrier = barrier
        
# Diese Methode wird ausgeführt wenn der Thread startet. In hier wird für jede Zahl im Bereich des Threads
# jene Zahl mit der nächsten multipliziert (Fakultät). Wir nehmen das Ergebnis stehts Modulo der Primzahl, um große Zahlen zu vermeiden.
# Am Ende sagen wir der Barriere das dieser Thread fertig ist und nun warten soll.
    def run(self):
        time.sleep(1)
        while self.numberStart <= self.numberEnd:
            self.total = (self.total * self.numberStart) % prim
            self.numberStart += 1 
        barrier.wait()

# Hier erstellen wir eine Textdatei und öffnen jede. Wir greifend lesend darauf zu und schreiben in jene die Zeiten für die Berechnung hinein.
def writeTimesInFile(file):
    print("Zeit für Berechnung: " + str(time.time()-start_time) + " Sekunden.")
    f = open(file, "a")
    f.write(str(prim) + " wurde in " + str(time.time()-start_time) + " Sekunden mit  " + str(threads_numbers) + " Threads berechnet. \n")
    f.close()
        
# Hier splitten wir jede Primzahl in die jeweiligen Bereiche auf. Hierfür wird zunächst gecheckt ob die Zahl durch die Threads teilbar ist.
# Wenn nicht, wird der Rest davon genommen. Jener wird am Ende dem letzten Intervall hinzugefügt.     
def intervalleBilden():
    rest = (prim - 1) % threads_numbers
    primNew = prim - rest

    #global, damit andere methoden Zugriff haben
    global listeThreads, threadAreaStart, threadAreaEnd
    listeThreads = []
    threadAreaStart = []
    threadAreaEnd = []
    
    # Hier splitten wir jede Primzahl in die jeweiligen Bereiche auf.
    for a in range(threads_numbers):
        threadAreaStart.append((a * (primNew - 1) / threads_numbers) + 1)
        threadAreaEnd.append((a + 1) * (primNew - 1) / threads_numbers)
    threadAreaEnd[-1] = threadAreaEnd[-1] + rest

#Hier multiplizieren wir das Ergebnis der einzelnen Threads miteinander auf und nehmen das Ergebnis schlussendlich noch einmal Modulo der Zahl.
#Wenn jene nun so groß ist wie die Primzahl - 1, dann => Zahl ist Primzahl.
def primzahlPruefen():
    summe = 1
    for i in range(threads_numbers):
        summe = summe * listeThreads[i].total % prim
    
    if summe == prim - 1:
        print(str(prim) + " ist eine Primzahl!\n")
    else:
        print(str(prim) + " ist keine Primzahl!\n")
        
# Methode multi_thread erstellt i Threads wobei i die Anzahl der Threads sind, die erwünscht sind.
# Jedem Thread wird ein Bereich zugeordnet und jeder Thread wird zu der Liste "listeThreads" zugefügt.
# Am Ende wird jeder Thread gestartet.
def multi_thread():
    for i in range(threads_numbers):
        numberStart = threadAreaStart.pop()
        numberEnd = threadAreaEnd.pop()
        listeThreads.append(MyThread(numberStart, numberEnd, barrier))
        listeThreads[i].start()      



if __name__ == '__main__':
    # Es wird eine leere Liste erstellt bzw. bei weiteren durchläufen jede geleert.
    # Anschließend wird aus den 2 Textdateien (müssen im gleichen Verzeichnis sein), jede Zahl ausgelesen
    # und in die List eingefügt. Am Ende wird jene vom kleinsten zum größten Wert sortiert.
    primes = []
    for line in open("Primes-Real.txt"):
        li = line.strip()
        if not li.startswith("#") and not li == '':
            primes.append(int(line.rstrip()))
    
    for line in open("Primes-Fake.txt"):
        li = line.strip()
        if not li.startswith("#") and not li == '':
            primes.append(int(line.rstrip()))
    primes.sort()
    
    # Hier schneiden wir die letzten 7 Zahlen ab, damit die Berechnung schneller geht.
    primes = primes[:len(primes)-4]
    
    file = "threadTimes.txt"
    orderOfThreads = [1, 2, 4, 16]
    # Wir iterieren durch die Anzahl der Primes und rechnen jeden mit 1, 2, 4 und 16 Threads durch.
    for x in range(len(primes)):
        for y in range(len(orderOfThreads)):
            prim = primes[x]
            threads_numbers = orderOfThreads[y]
            barrier = threading.Barrier(threads_numbers+1)
            
            if prim < threads_numbers * 2:
                continue
        
            print("Die zu untersuchende Zahl ist: " + str(prim))
            print("Es werden " + str(threads_numbers) + " Thread(s) benutzt\n")

            intervalleBilden()
        
            #Zeitberechnung starten
            start_time = time.time()
            multi_thread()
        
            #Der Hauptthread wartet hier bis alle anderen Threads auch die Barrier erreicht haben.
            barrier.wait()
            writeTimesInFile(file)
            primzahlPruefen()

        

        
        
     
        
        
        
        
        
        
        
        
        
        
        
