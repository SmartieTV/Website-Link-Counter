# Website Tool by SmartieTV (smartietv.de or youtube.com/smartietv)
# Lese readme.txt für weitere Informationen und eine Anleitung. 
# View readme.txt for further information and instructions. 

version = ("220202.08")

# Notwendige Libraries (bs4 erfordert manuellen Import)
try:
  from bs4 import BeautifulSoup
  import os
  import requests
  import re
  import time
  #import random # Unused
except Exception as e4:
  print("Website Tool")
  print("------------")
  print("Version: " + str(version))
  print("")
  print("Erforderliche Libraries konnten nicht importiert werden! ")
  print("Necesarry libraries could not be imported! ")
  print("")
  print("BeautifulSoup4 muss vorher installed werden:")
  print("BeautifulSoup4 must be installed first:")
  print("")
  print("-> sudo pip install BeautifulSoup4")
  print("oder/or")
  print("-> sudo apt-get install python3-bs4")
  print("")
  print("Fehler / Error: (" + str(e4) + ").")
  #exit()
  
# URL hier eingeben: / Enter URL here (mit / with https://):
scrape_url = ("") #Leer lassen, um URL im Programm einzugeben / Leave empty to enter URL in the program.

# Nutzereinstellungen / User settings:
deleteAllFiles = ("false") # Alle Result-Dateien löschen / Delete all result files?
printInConsole = ("true") # Ergebnisse in der Console anzeigen / Show results in Console? 
showDuplicates = ("true") #Mehrfach vorkommende Links in Datei anzeigen / Show duplicate links in file?
checkForCookies = ("true") #Nach Cookies checken / Check for cookies? (COMING SOON)
autoReformat = ("false") # Automatisch https:// an eingegebene Url (ohne dieses) anhängen / Toggle automatically adding https:// to entered url (without). 

# Experimentelle Features:
treeMode = ("false")
# Dieser Modus scraped alle URL's auf der Website, indem es jede gefundene URL aufnimmt. 
# This mode scrapes all URLs on the website, by including every found url.

# Experteneinstellungen / Expert settings:
deleteCoolDown = 0.2 # Cooldown in Sekunden. Rate, in welcher Dateien gelöscht werden. Default = 0.2
deletionScope = 100 # Scope, in welchem alleinstehende Dateiendungen auch gefunden und gelöscht werden. Default = 100
treeModeCoolDown = 2.0 # Cooldown in Sekunden, in welchem im Treemode eine neue Seite aufgerufen und geparsed wird. Default = 2
# Cooldown between scraping sites in treemode. 
enableBugFix = ("false") # BugFix Modus / BugFix Mode



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
    resultFileName2 = "result-TM" + str(resultNr)
    if os.path.exists(resultFileName):
      os.remove(resultFileName)
      print("Datei wurde entfernt: / File has been removed: " + str(resultFileName))
      time.sleep(deleteCoolDown)
    if os.path.exists(resultFileName2):
      os.remove(resultFileName2)
      print("Datei wurde entfernt: / File has been removed: " + str(resultFileName2))
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


def getCookies(cookie_url, inTreeMode):#Retrieve cookies from entered url.
  try:
    bugfix("Arrived in getCookies function. Depending on the amount and complexity of the cookies this might take a while. Checking for: " + str(cookie_url))
    global cookieList
    r2 = requests.post(cookie_url)
    for cookie in r2.cookies:
      bugfix("Found cookie: " + str(cookie.__dict__) + str(cookie.secure))
      if printInConsole == ("true"):
        print("Cookie-Dict: " + str(cookie.__dict__))
        print("Cookie-Secure: " + str(cookie.secure))
      if inTreeMode == ("true"):
        bugfix("inTreeMode is true, changing cookieList append method. ")
        #cookieList.append("URL: (" + str(cookie_url) + "): " + str(cookie.__dict__) + " -> " + str(cookie.secure))
        if cookie.__dict__ != (""):
          #appendTxt1 = ("URL: " + str(cookie_url) + " -> " + str(cookie.__dict__))
          appendTxt1 = str(cookie.__dict__) #Replaces above line, not including URL in treemode, where cookie was found. (Fix later)
          cookieList.append(appendTxt1)
        if cookie.secure != (""):
          #appendTxt2 = ("URL: " + str(cookie_url) + " -> " + str(cookie.secure))
          appendTxt2 = str(cookie.secure) #Replaces above line, not including URL in treemode, where cookie was found. (Fix later)
          cookieList.append(appendTxt2)
      else:
        if cookie.__dict__ != (""):
          appendTxt1 = (str(cookie.__dict__))
          cookieList.append(appendTxt1)
        if cookie.secure != (""):
          appendTxt2 = (str(cookie.secure))
          cookieList.append(appendTxt2)
    return cookieList
  except Exception as e19:
    bugfix("Error occured while trying to find cookies: " + str(e19))
    

def treeModeExec():
  global result1List
  try:
    bugfix("Arrived at treeModeExec")
    if treeMode == ("true") and deleteAllFiles == ("false"):
      bugfix("treeMode == true")
      resultCountTree = 0
      result1Tree = ""
      scrapedList = [""]
      startTimeTree = time.time()
      resultNr = 0
      bugfix("Starting treemode...")
      bugfix("Result1List contents: " + str(result1List))
      for urlInTreeMode in result1List:
        if urlInTreeMode in scrapedList:
          bugfix("Ignored url (" + str(urlInTreeMode) + "), because it has already been scraped. ")
        else:
          scrapedList.append(urlInTreeMode)

          result1List = list(dict.fromkeys(result1List)) #Removes duplicates
          bugfix("Treemode - Current URL: (" + str(urlInTreeMode) + "). ")
          if scrape_url in urlInTreeMode:
            html_document = htmlDoc(urlInTreeMode)
            soup = BeautifulSoup(html_document, 'html.parser')
            bugfix("Beginning compilation mode for current url. ")
            for link in soup.find_all('a',attrs={'href': re.compile("^https://")}):
              resultCountTree = resultCountTree + 1
              if printInConsole == ("true"):
                print(link.get('href'))
              result1Tree = result1Tree + "\n" + str(resultCountTree) + ") " + str(link.get("href"))  
              result1List.append(link.get("href"))
            if checkForCookies == ("true"):
              bugfix("Check for cookies for current url active, calling function. ")
              try:
                urlForCookieCheck = str(urlInTreeMode)
                getCookies(urlForCookieCheck,"true")
              except Exception as e20:
                bugfix("Could not check for cookies for current url! Skipping it: " + str(urlInTreeMode) +" / Reason: " +  str(e20))
            bugfix("Running cooldown (" + str(treeModeCoolDown) + "s).")
            time.sleep(treeModeCoolDown)
          else:
            bugfix("Treemode - URL: (" + str(urlInTreeMode) + ") is not in scrape_url, ignoring it.")
      bugfix("Treemode - Finished scraping all urls. ")
      resultCountFromList = len(result1List)
      resultCountFromListExclDups = len(set(result1List))
      duplicates = resultCountFromList - resultCountFromListExclDups
      endTimeTree = time.time()
      print("")
      print("Programm erfolgreich beendet. / Program finished successfully.")
      print("Ergebnisse / Results: ")
      print("")
      print("Gesamt / Total: " + str(resultCountFromList))
      print("Einzigartig / Unique: " + str(resultCountFromListExclDups))
      print("Duplikate / Duplicates: " + str(duplicates))
      print("Benötigte Zeit / Elapsed Time: " + str(endTimeTree - startTimeTree) + "s")
      bugfix("Finished treemode! All url's from scrape_url parsed.")
      bugfix("Logging results to file.")
      runTreeModeFileSearch = ("true")
      resultFileNameTree = ("result-TM1")
      while runTreeModeFileSearch == ("true"):
        if os.path.exists(resultFileNameTree): #Bereits existierende Dateien ignorieren. 
          "SKIP"
          bugfix("File exists already (" + str(resultFileNameTree) + "), increasing by 1.")
          resultNr = resultNr + 1
          resultFileNameTree = "result-TM" + str(resultNr)
        else:
          runTreeModeFileSearch = ("false")
          print("Gespeichert in der Datei: / Saved in the file: " + str(resultFileNameTree))
          bugfix("Found file to log results to: (" + str(resultFileNameTree) + ").")
          f = open(resultFileNameTree, "a")
          f.write("Gesamt / Total: " + str(resultCountFromList) + "\n")
          f.write("Einzigartig / Unique: " + str(resultCountFromListExclDups) + "\n")
          f.write("Duplikate / Duplicates: " + str(duplicates) + "\n")
          f.write("Benötigte Zeit / Elapsed Time: " + str(endTimeTree - startTimeTree) + "s\n")
          f.write("Anfang des Ergebnisses: / Start of result: \n")
          f.write("------------------------------------------\n")
          iCount = 0
          for i in set(result1List):
            result1ListLogContent = [""]
            if showDuplicates == ("false"):
              if i in result1ListLogContent:
                "IGNORE"
                bugfix("Logging issue: (" + str(i) + ") is already logged, ignoring it. ")
              else:
                result1ListLogContent.append(i)
                iCount = iCount + 1
                f.write(str(iCount) + ") " + str(i) + "\n")
            else:
              iCount = iCount + 1
              f.write(str(iCount) + ") " + str(i) + "\n")
          iCountCookies = 0
          iCookie = ""
          f.write("\n Ende der Urls / End of urls. \n")
          f.write("Cookies: \n")
          for iCookie in set(cookieList):
            iCountCookies = iCountCookies + 1
            f.write(str(iCountCookies) + ") " + str(iCookie) + "\n")
          f.write("\nEnde des Ergebnisses. / End of result.")
          f.close()
          bugfix("Treemode logging complete. ")
      bugfix("Treemode finished. ")
  except Exception as e18:
    bugfix("An error occured while running treeMode exec: " + str(e18))
    print("Während dem treeMode ist ein Fehler aufgetreten!")
    print("An error occured while running treeMode exec! ")
    print("Fehler / Error: " + str(e18))

bugfix("Arrived in program.")

result1 = ""
resultCount = 0
result1List = [""]
cookieList = [""]
iCookie = ""
re_go = ("false") #Used to hide intro after first go.

programRunning = ("true")
while programRunning == ("true"):
  try:
    bugfix("Arrived in tryLoop #1")
    if deleteAllFiles == ("false"):
      bugfix("Arrived in deleteAllFiles statement.")
      if scrape_url == (""):
        if re_go == ("false"): #Only show this, if user hasn't seen it before. 
          print("Website Tool")
          print("------------")
          print("Version: " + str(version))
          print("Wichtig / Important:")
          print("Überprüfe nur Websites, welche du besitzt und/oder scrapen + überprüfen darfst. ")
          print("Only check websites, which you own and/or have the permission to scrape + check. ")
          print("")
          print("Result-Dateien löschen / Delete result files:")
          print("-> delallfiles")
        if treeMode == ("true"):
          print("""
          TreeMode ist aktiv!
          """)
        print("")
        print("-------------------------")
        print("URL eingeben / Enter URL:")
        print("Beispiel / Example: https://example.com")
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
      bugfix("Arrived in scraping mode (non-treemode).")
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
      if checkForCookies == ("true"):
        bugfix("Calling getCookies function now. Non-Treemode.")
        getCookies(scrape_url, "false")
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
          if checkForCookies == ("true"):
            iCountCookies = 0
            f.write("\n Ende der Urls / End of urls. \n")
            f.write("Cookies: \n")
            for iCookie in set(cookieList):
              iCountCookies = iCountCookies + 1
              f.write(str(iCountCookies) + ") " + str(iCookie) + "\n")
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
          if checkForCookies == ("true"):
            iCountCookies = 0
            f.write("\n Ende der Urls / End of urls. \n")
            f.write("Cookies: \n")
            for iCookie in set(cookieList):
              iCountCookies = iCountCookies + 1
              f.write(str(iCountCookies) + ") " + str(iCookie) + "\n")
          f.write("\nEnde des Ergebnisses. / End of result.")
          f.close()
          run = ("false")
          print("")
          print("Ergebnis wurde in folgender Datei gespeichert: (" + str(resultFileName) + ").")
          print("Result has been saved in the following file: (" + str(resultFileName) + ").")
    treeModeExec()
      
    if deleteAllFiles == ("true"):
      "Nothin" #Script um Dateien zu löschen, nur aktiviert bei manueller Variablenumstellung.
      bugfix("DeleteAllFiles statement reached. ")
      print("Dateien werden gelöscht / Files are being deleted.")
      deleteAllFilesFunc()
  except Exception as e1:
    print("Ein kritischer Fehler ist aufgetreten! A critical error occured!")
    print("Fehler / Error: " + str(e1))

  

  bugfix("Arrived at the end of the program.")
  scrape_url = ("") #Resets scrape URL
  re_go = ("true")
# Ende des Programms / End of Program
bugfix("Arrived outside of (programmRunning) loop. (THIS SHOULD NOT HAPPEN!)")