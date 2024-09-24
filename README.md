## Ausführung
 + Doppelklicken auf die **afae.bat** Datei: Kümmert sich um Setup und Programmausführung, muss auf Gerät erlaubt werden.
 + Sofern Python funktioniert und die notwenigen Modules existieren, kann **main.py** direkt ausgeführt werden.

## Setup
### **install_python.bat**:
- Installiert Python, setzt die PATH-Variable und installiert die notwendigen Python-Module.
- Benutzt **requirements.txt** um benötigte Python Module nachzuschauen.

## Scripts in /pyscripts
### 1. **main.py** 
Enthält die abstrakte Programm-Logik:
- **Modi**:
    - **Automatisch**: 
        - Das Skript sammelt alle Kurslinks von der AFÄ-Website und scraped diese nach den entsprechenden Kursdaten.
        - Nach dem Sammeln der Kursdaten werden diese in die Datei `kurse.json` geschrieben.
    - **Interaktiv**: 
        - Zwei Modi: 
            1. **Fensterprogramm**:
                - Oben im leeren Balken die gewünschte Kursnummer eingeben und `[ENTER]` oder auf "Suchen" klicken.
            2. **Terminal**:
                - Nach dem `:` die Kurs-ID eingeben und `[ENTER]` drücken.
### 2. **scraper.py**
Implementiert das eigentliche Webscraping:
- **Funktionen**:
    - `sammleAlleKursLinks()`: Wird in `main.py` aufgerufen, standardmäßig auskommentiert. Sollte gelegentlich ausgeführt werden, um aktuelle Kurslinks zu sammeln.
    - `findeKursDetailsMitKursNummer()`: Wird nur im *Interaktiv-Modus* verwendet. Nach Eingabe einer Kursnummer/ID wird der entsprechende Link gesucht und die Kursinformationen werden gescraped.
### 3. **gui.py**
Stellt eine Fensteranwendung bereit:
- **Hinweis**:
    - Nicht entscheidend für die Kernfunktionalität. Falls gelöscht, sollte der Aufruf `startGui()` in der `main.py` entweder entfernt oder auskommentiert und durch `pass` ersetzt werden.

## Dateien in /data
- **afae-alle-kurse.txt**: Enthält alle gesammelten Kurslinks der Website.
- **afae-kurse.json**: Enthält die *Kursinformationen* zu den gesammelten Kurslinks.

## Dateien in /misc
- **afae-icon.ico**: Wird als Icon im Fensterprogramm verwendet.
- **afae-background.jpg**: Hintergrundbild für das Fensterprogramm.