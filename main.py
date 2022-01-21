# Website Link Counter by SmartieTV (smartietv.de or youtube.com/smartietv)
version = ("220121.3")

# Notwendige Libraries (bs4 erfordert manuellen Import)
from bs4 import BeautifulSoup
import os
import requests
import re
import time
  
# URL hier eingeben: / Enter URL here (mit / with https://):
scrape_url = ("") #Leer lassen, um URL im Programm einzugeben / Leave empty to enter URL in the program.

# Nutzereinstellungen / User settings:
deleteAllFiles = ("false") # Alle Result-Dateien löschen / Delete all result files?
printInConsole = ("false") # Ergebnisse in der Console anzeigen / Show results in Console? 
showDuplicates = ("true") #Mehrfach vorkommende Links in Datei anzeigen / Show duplicate links in file?
checkForCookies = ("true") #Nach Cookies checken / Check for cookies? (COMING SOON)
autoReformat = ("false") # Automatisch https:// an eingegebene Url (ohne dies) anhängen / Toggle automatically adding https:// to entered url (without). 

# Experteneinstellungen / Expert settings:
deleteCoolDown = 0.2 # Cooldown in Sekunden. Rate, in welcher Dateien gelöscht werden. Default = 0.2
deletionScope = 100 # Scope, in welchem alleinstehende Dateiendungen auch gefunden und gelöscht werden. Default = 100
enableBugFix = ("true") # BugFix Modus / BugFix Mode


# Ende der Einstellungen, Beginn des Programms. / End of settings, start of program. 
  
# Html Dokument Extrahieren
def htmlDoc(url):
  response = requests.get(url)
  return response.text

def bugfix(content):
  if enableBugFix == ("true"):
    print("[BugFix]: " + str(content))

def deleteAllFilesFunc(): #Dateien löschen
  bugfix("Arrived at deleteAllFilesFunc")
  global resultNr
  resultNr = 0
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
Starte das Programm erneut und ändere ggf die Variable wieder zu false.

All files deleted successfully!
Restart the program and optionally change the variable back to false, to use the program as usual. 
      """)
      exit()

def getCookies():#Retrieve cookies from entered url.
  r2 = requests.post(scrape_url)
  for cookie in r2.cookies:
    print(cookie.__dict__)
    print(cookie.secure)

bugfix("Arrived in program.")

result1 = ""
resultCount = 0
result1List = [""]
re_go = ("false") #Used to hide intro after first go.

programRunning = ("true")
while programRunning == ("true"):
  try:
    bugfix("Arrived in tryLoop #1")
    if deleteAllFiles == ("false"):
      bugfix("Arrived in deleteAllFiles statement.")
      if scrape_url == (""):
        if re_go == ("false"): #Only show this, if user hasn't seen it before. 
          print("Website Link Tool")
          print("-----------------")
          print("Version: " + str(version))
          print("")
          print("Result-Dateien löschen / Delete result files:")
          print("-> delallfiles")
        print("")
        print("-------------------------")
        print("URL eingeben / Enter URL:")
        print("Beispiel / Example: https://google.com")
        print("")
        scrape_url = input("URL: ")
        if ("delfiles") in scrape_url or ("delallfiles") in scrape_url:
          print("Dateien werden gelöscht. ")
          deleteAllFilesFunc()
        if "https://" in scrape_url or "http://" in scrape_url:
          bugfix("URL-Check successful: Found http/https.")
        else: #Replace url
          newUrl = ("https://" + scrape_url)
          bugfix("URL-Check unsuccessful: Could not find http/https.")
          print("")
          print("Die eingegebene URL (" + str(scrape_url) + ") scheint kein http:// oder https:// zu besitzen. Soll sie wie folgt angepasst werden?")
          print("The entered URL (" + str(scrape_url) + ") doesn't seem to have http:// or https://. Should the URL be changed like this?")
          print("")
          print("Neu/New: -> " + str(newUrl))
          print("")
          print("Tippe ENTER um die Änderungen vorzunehmen oder (1) um abzubrechen. ")
          print("Press ENTER to accept the change or type (1) to cancel. ")
          print("")
          if autoReformat == ("false"):
            userInput2 = input("")
            if userInput2 == (""):
              scrape_url = newUrl
              bugfix("Changing url due to user's command. ")
            else:
              print("Alte URL wird beibehalten / Keeping old URL")
              bugfix("Keeping old url due to user's command. ")
          else:
            scrape_url = newUrl
            bugfix("Changing url automatically. ")
          
      # URL zum scrapen
      html_document = htmlDoc(scrape_url)
      soup = BeautifulSoup(html_document, 'html.parser')
      print("URL wird analysiert... / URL is being analyzed...")
      #print("")
      #print("URL: " + str(scrape_url))
      #time.sleep(1)
      print("")
      startTime = time.time()
      # Zeigt alle Ergebnisse mit einem href Tag und https://
      for link in soup.find_all('a',attrs={'href': re.compile("^https://")}):
        resultCount = resultCount + 1
        if printInConsole == ("true"):
          print(link.get('href'))
        result1 = result1 + "\n" + str(resultCount) + ") " + str(link.get("href"))  
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
    else:
      bugfix("deleteAllFiles != false: " + str(deleteAllFiles))

    resultNr = 0
    resultFileName = "result" + str(resultNr)
    run = ("true")

    while run == ("true") and deleteAllFiles == ("false"): #Ergebnis in Datei speichern.
      resultNr = resultNr + 1
      resultFileName = "result" + str(resultNr)
      if os.path.exists(resultFileName): #Bereits existierende Dateien ignorieren. 
        "SKIP"
      else:
        if showDuplicates == ("true"):
          f = open(resultFileName, "a")
          f.write("Gesamt / Total: " + str(resultCountFromList) + "\n")
          f.write("Einzigartig / Unique: " + str(resultCountFromListExclDups) + "\n")
          f.write("Duplikate / Duplicates: " + str(duplicates) + " (Angezeigt / Showing)\n")
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
        else:
          f = open(resultFileName, "a")
          f.write("Gesamt / Total: " + str(resultCountFromList) + "\n")
          f.write("Einzigartig / Unique: " + str(resultCountFromListExclDups) + "\n")
          f.write("Duplikate / Duplicates: " + str(duplicates) + " (Versteckt / Hidden)\n")
          f.write("Benötigte Zeit / Elapsed Time: " + str(endTime - startTime) + "s\n")
          f.write("Anfang des Ergebnisses: / Start of result: \n")
          f.write("------------------------------------------\n")
          #f.write(str(set(result1List)))
          iCount = 0
          for i in set(result1List):
            iCount = iCount + 1
            f.write(str(iCount) + ") " + str(i) + "\n")
          f.write("\nEnde des Ergebnisses. / End of result.")
          f.close()
          run = ("false")
          print("")
          print("Ergebnis wurde in folgender Datei gespeichert: (" + str(resultFileName) + ").")
          print("Result has been saved in the following file: (" + str(resultFileName) + ").")
      
    if deleteAllFiles == ("true"):
      "Nothin" #Script um Dateien zu löschen, nur aktiviert bei manueller Variablenumstellung.
      bugfix("DeleteAllFiles statement reached. ")
      print("Dateien werden gelöscht / Files are being deleted.")
      deleteAllFilesFunc()
  except Exception as e1:
    print("Ein kritischer Fehler ist aufgetreten! A critical error occured!")
    print("Fehler / Error: " + str(e1))

  bugfix("Arrived at end of program.")
  scrape_url = ("") #Resets scrape URL
  re_go = ("true")
# Ende des Programms / End of Program
bugfix("Arrived outside of (programmRunning) loop. (THIS SHOULD NOT HAPPEN!)")