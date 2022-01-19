# Website Link Counter by SmartieTV (smartietv.de or youtube.com/smartietv)

# Notwendige Libraries (bs4 erfordert manuellen Import)
from bs4 import BeautifulSoup
import os
import requests
import re
import time
  
# URL hier eingeben: / Enter URL here (mit / with https://):
scrape_url = ("") #URL Kann auch im Programm eingegeben werden.

# Nutzereinstellungen / User settings:
deleteAllFiles = ("false") # Alle Result Dateien löschen. ACHTUNG, dies löscht unwiderruflich alle resultX.txt Dateien.
printInConsole = ("true") # Ergebnisse in der Console anzeigen? Show results in Console? 

# Experteneinstellungen / Expert settings:
deleteCoolDown = 0.5 # Cooldown in Sekunden. Rate, in welcher Dateien gelöscht werden.
deletionScope = 50 # Scope, in welchem alleinstehende Dateiendungen auch gefunden und gelöscht werden.

# Ende der Einstellungen, Beginn des Programms. / End of settings, start of program. 
  
# Html Dokument Extrahieren
def htmlDoc(url):
  response = requests.get(url)
  return response.text
  
result1 = ""
resultCount = 0
result1List = [""]
try:
  if deleteAllFiles == ("false"):
    if scrape_url == (""):
      print("URL eingeben / Enter URL:")
      print("Beispiel / Example: https://google.com")
      print("")
      scrape_url = input("URL: ")
    # URL zum scrapen
    html_document = htmlDoc(scrape_url)
    soup = BeautifulSoup(html_document, 'html.parser')
    print("Programm startet / Program starting")
    print("Dies könnte eine Weile dauern... / This might take a while...")
    print("")
    print("URL: " + str(scrape_url))
    time.sleep(1)
    print("")
    startTime = time.time()
    # Zeigt alle Ergebnisse mit einem href Tag und https://
    for link in soup.find_all('a',attrs={'href': re.compile("^https://")}):
      if printInConsole == ("true"):
        print(link.get('href'))
      result1 = result1 + "\n" + link.get("href")  
      resultCount = resultCount + 1
      result1List.append(link.get("href"))
    
    resultCountFromList = len(result1List)
    resultCountFromListExclDups = len(set(result1List))
    duplicates = resultCountFromList - resultCountFromListExclDups
    endTime = time.time()
    print("")
    print("Programm erfolgreich beendet. / Program finished successfully.")
    print("Ergebnisse / Results: ")
    print("")
    print("Gesamt / Total: " + str(resultCountFromList))
    print("Einzigartig / Unique: " + str(resultCountFromListExclDups))
    print("Duplikate / Duplicates: " + str(duplicates))
    print("Benötigte Zeit / Elapsed Time: " + str(endTime - startTime) + "s")
    #print(result1List)

  resultNr = 0
  resultFileName = "result" + str(resultNr)
  run = ("true")

  while run == ("true") and deleteAllFiles == ("false"): #Ergebnis in Datei speichern.
    resultNr = resultNr + 1
    resultFileName = "result" + str(resultNr)
    if os.path.exists(resultFileName): #Bereits existierende Dateien ignorieren. 
      "SKIP"
    else:
      f = open(resultFileName, "a")
      f.write("Gesamt / Total: " + str(resultCountFromList) + "\n")
      f.write("Einzigartig / Unique: " + str(resultCountFromListExclDups) + "\n")
      f.write("Duplikate / Duplicates: " + str(duplicates) + "\n")
      f.write("Benötigte Zeit / Elapsed Time: " + str(endTime - startTime) + "s\n")
      f.write("Anfang des Ergebnisses: / Start of result: \n")
      f.write("------------------------------------------\n")
      f.write(str(result1))
      f.write("\nEnde des Ergebnisses. / End of result.")
      f.close()
      run = ("false")
      print("")
      print("Ergebnis wurde in folgender Datei gespeichert: (" + str(resultFileName) + ").")
      print("Result has been saved in the following file: (" + str(resultFileName) + ").")
    
  if deleteAllFiles == ("true"): #Script um Dateien zu löschen, nur aktiviert bei manueller Variablenumstellung.
    runDeletion = ("true")
    while runDeletion == ("true"):
      resultNr = resultNr + 1
      resultFileName = "result" + str(resultNr)
      if os.path.exists(resultFileName):
        os.remove(resultFileName)
        print("Datei wurde entfernt: / File has been removed: " + str(resultFileName))
        time.sleep(deleteCoolDown)
      elif resultNr < deletionScope:
        "Continue..."
      else:
        runDeletion = ("false")
        print("""
  Alle Dateien erfolgreich gelöscht!
  All files deleted successfully!

  Ändere nun die Variable wieder auf false, um das Programm normal zu nutzen.
  Change the variable back to false, to use the program as usual. 
        """)
except Exception as e1:
  print("""
Es ist ein Fehler aufgetreten, welcher das Programm angehalten hat!
An error occured, which prevented this program from executing. 
  """)
  print("Fehler / Error: " + str(e1))

# Ende des Programms / End of Program