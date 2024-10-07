# main.py

# +- System Modules -+ #
import os
import json
import time
import re

# +- Custom Modules -+ #
from scraper import sammleAlleKursLinks, scrapeHtml, findeKursDetailsMitKursNummer
from gui import startGui

BEREICHE = [
    "https://www.akademie-fuer-aeltere.de/neu-online-digitalkurse/",
    "https://www.akademie-fuer-aeltere.de/gesundheit-bewegung/",
    "https://www.akademie-fuer-aeltere.de/natur-umwelt/",
    "https://www.akademie-fuer-aeltere.de/sprachen/",
    "https://www.akademie-fuer-aeltere.de/gesellschaft-kultur/",
    "https://www.akademie-fuer-aeltere.de/kunst-literatur-musik/",
    "https://www.akademie-fuer-aeltere.de/akademie-unterwegs/",
    "https://www.akademie-fuer-aeltere.de/computer-mobile-geraete/"
]

def main():
    # Optionales Sammeln der Kurslinks und Information
    print("\nPROGRAMM GESTARTET.\n")
    c = input("Alle Kurslinks sammeln? Das kann eine Minute dauern. [ja/nein]: ")
    if c in ["j", "ja", "Ja", "JA"]:
        sammleAlleKursLinks(BEREICHE)                                   
        print("Kurslinks-Datei updated.\n")                               # ganz vorne löschen
    
    print("INFO: Option A bedeutet: Alle Links aus 'afae-alle-kurse.txt' automatisch abgehen und Kursdaten sammeln.")
    print("INFO: Die neuen Kurs-Daten werden in eine Datei 'kurse.json' geschrieben.")
    print("INFO: Danach kann man mit Steuerung+F in der kurse.json nach den Kurs-Ids suchen.\n")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Programm-Ablauf
    prozess = input("Automatisch oder Interaktiv? [A/I]: ")
    if prozess.lower() in ["a", "automatisch"]:        
        kurse = []
        kursliste_path = os.path.join(script_dir, '..', 'data', 'afae-alle-kurse.txt')
        with open(kursliste_path) as rf:
            links = rf.read().splitlines()
        rf.close()
        scraped_links = 0
        for link in links:
            pattern = r"/(\d{3}-[A-Z]?\d{4})/"  # Kurs-Id Pattern 
            kurs_nummer = re.search(pattern, link)
            if kurs_nummer:
                data = scrapeHtml(link, kurs_nummer.group())
                if data not in ["ConnectionError", "TimeoutError"]:
                    print(f"Scraping für Kurs-Id: {kurs_nummer.group()} \t {str(scraped_links)}/{str(len(links))} Kursdaten gesammelt.", end="\r")
                    kurse.append(data)
                time.sleep(3)
                scraped_links += 1

        json_obj = {"kurse": kurse}
        kurse_json_path = os.path.join(script_dir, '..', 'data', 'afae-kurse.json')
        with open(kurse_json_path, "w", encoding="utf-8") as json_file:
            json.dump(json_obj, json_file, ensure_ascii=False, indent=4)
        
    else:
        modus = input("Im Fenster oder Terminal starten? [f/t]: ")
        if modus.lower() in ["f", "fenster"]:
            startGui()
            #pass
        else:
            while True:
                kurs_nummer = input("Bitte geben Sie eine Kurs-Id an: ")
                kurs_infos = findeKursDetailsMitKursNummer(kurs_nummer)
                print("\n"+ kurs_infos + "\n")
                weiter = input("Möchten sie weitere Kurs-Ids abrufen? [ja/nein]: ")
                if weiter.lower() not in ["j", "ja", "ha", "ka"]:
                    break

    print("\nPROGRAMM BEENDET.\n")

if __name__ == "__main__":
    main()