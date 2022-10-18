import multiprocessing
import time

# Hier splitten wir jede Primzahl in die jeweiligen Bereiche auf. Hierfür wird zunächst gecheckt ob die Zahl durch die Threads teilbar ist.
# Wenn nicht, wird der Rest davon genommen. Jener wird am Ende dem letzten Intervall hinzugefügt. 
def intervalleBilden(prim, process_nubers):
    global threadAreaStart, threadAreaEnd, ListeProcesse
    rest = (prim - 1) % process_numbers
    primNew = prim - rest
    threadAreaStart = []
    threadAreaEnd = []
    for x in range(process_numbers):
        threadAreaStart.append((x * (primNew - 1) / process_numbers) + 1)
        threadAreaEnd.append((x + 1) * (primNew - 1) / process_numbers)
    threadAreaEnd[-1] = threadAreaEnd[-1] + rest


# Unsere Klasse für die Threads. Es wird eine Barriere gesetzt, in Größe der benötigten Threads.
class MyProcess(multiprocessing.Process):

    # Hier wird der Bereich dieses Threads instanziiert.
    def __init__(self, numberStart, numberEnd, queue, prim):
        multiprocessing.Process.__init__(self)
        self.numberStart = numberStart
        self.numberEnd = numberEnd
        self.total = 1
        self.queue = queue
        self.prim = prim

    # Diese Methode wird ausgeführt wenn der Thread startet. In hier wird für jede Zahl im Bereich des Threads
    # jene Zahl mit der nächsten multipliziert (Fakultät). Wir nehmen das Ergebnis stehts Modulo der Primzahl, um große Zahlen zu vermeiden.
    # Am Ende fügen wir den Prozess in die Schlange (queue) ein.
    def run(self):
        print("starte Prozess")
        time.sleep(1)
        while self.numberStart <= self.numberEnd:
            self.total = (self.total * self.numberStart) % self.prim
            self.numberStart += 1
        self.queue.put(self.total)

# In dieser Methode wird zunächst eine queue angelegt. Es wird dann durch die Anzahl der Prozessnummern durch iteriert.
# Jeder Durchlauf startet ein Prozess, welcher dann in die Liste "listeProzesse" hinzugefügt werden. Am Ende der Schleife starten wir den Prozess.
# Später wird dann das Ergebnis aus der Queue
def multi_pro(prim, process_numbers):
    queue = multiprocessing.Queue()
    ListeProcesse = []
    for i in range(process_numbers):
        numberStart = threadAreaStart.pop()
        numberEnd = threadAreaEnd.pop()
        ListeProcesse.append(MyProcess(numberStart, numberEnd, queue, prim))
        ListeProcesse[i].start()

    summe = []
    for i in range(len(ListeProcesse)):
        summe.append(queue.get())

    for i in range(process_numbers):
        ListeProcesse[i].join

    return summe

#Hier multiplizieren wir das Ergebnis der einzelnen Prozesse miteinander auf und nehmen das Ergebnis schlussendlich noch einmal Modulo der Zahl.
#Wenn jene nun so groß ist wie die Primzahl - 1, dann => Zahl ist Primzahl.
def primzahlPruefen(summeProzesse):
    summe = 1
    for i in range(process_numbers):
        summe = summe * summeProzesse[i] % prim

    if summe == prim - 1:
        print(str(prim) + " ist eine Primzahl\n")
    else:
        print(str(prim) + " ist keine Primzahl\n")

# Hier erstellen wir eine Textdatei und öffnen jede. Wir greifend lesend darauf zu und schreiben in jene die Zeiten für die Berechnung hinein.
def writeTimesInFile(file):
    print("Zeit für Berechnung: " + str(time.time()-start_time) + " Sekunden.")
    f = open(file, "a")
    f.write(str(prim) + " wurde in " + str(time.time()-start_time) + " Sekunden mit  " + str(process_numbers) + " Prozesse berechnet. \n")
    f.close()

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

    file = "processTimes.txt"
    orderOfProcess = [1, 2, 4, 16]
    
    # Wir iterieren durch die Anzahl der Primes und rechnen jeden mit 1, 2, 4 und 16 Prozessen durch.
    for x in range(len(primes)):
        for y in range(len(orderOfProcess)):       
            prim = primes[x]
            process_numbers = orderOfProcess[y]
        
            if prim < process_numbers * 2:
                continue    
            
            print("Die zu untersuchende Zahl ist: " + str(prim))
            print("Es werden " + str(process_numbers) + " Prozess(e) benutzt\n")
        
            intervalleBilden(prim, process_numbers)
        
            start_time = time.time()
            file = "processTimes.txt"
        
            # prozesse erstellen
            summeProzesse = multi_pro(prim, process_numbers)
        
            writeTimesInFile(file)
        
            primzahlPruefen(summeProzesse)
