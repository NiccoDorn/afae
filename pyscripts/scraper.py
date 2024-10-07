# scraper.py
import os
# +- Scraping Modules -+ #
import re
import time
import requests as r
from bs4 import BeautifulSoup as bs


def kursbereich_anfrage(bereich_link: str):
    links = []
    response = r.get(bereich_link)
    html = bs(response.text, 'html.parser')
    front_links = [link.get('href') for link in html.find_all('a') if link.get('href')]
    kurs_links_front = [link for link in front_links if "/kursdetails/" in link]
    links += kurs_links_front
    time.sleep(2)

    pages = set([link for link in front_links if "/browse/forward" in link])
    for page in pages:
        response = r.get(page)
        html = bs(response.text, 'html.parser')
        plinks = [link.get('href') for link in html.find_all('a') if link.get('href') and "/kursdetails/" in link.get("href")]
        links += plinks
        time.sleep(2)
    return links

def sammleAlleKursLinks(bereiche: list[str]):
    alle_kurs_links = []
    i = 1
    for bereich in bereiche:
        links = kursbereich_anfrage(bereich)
        kurs_links = set([re.sub(r'/kategorie-id/\d+', '', link) for link in links if "/programm/" in link])
        alle_kurs_links += kurs_links
        print(f"Kurslinks für {i}/8 Bereiche gesammelt.", end="\r")
    
        i += 1
    alle_kurs_links = set(alle_kurs_links)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    kursliste_path = os.path.join(script_dir, '..', 'data', 'afae-alle-kurse.txt')
    with open(kursliste_path, 'w+') as wf:
        wf.writelines(f"{kurs}\n" for kurs in alle_kurs_links)
    wf.close()
    print()

def scrapeHtml(kurs_link: str, kurs_nummer: str):
    try:
        response = r.get(kurs_link, timeout=5)
        html = bs(response.text, 'html.parser')
        tds = html.find_all("td")
        data = {"Kurs-Id": kurs_nummer.replace("/", ""), "Kursname": kurs_link.split("/")[-1]}
        keys = ['Status', 'Beginn', 'Dauer', 'Kursgebühr', 'Kursleitung', 'Anmeldung']
        for i in range(0, len(tds), 2):
            key = tds[i].get_text(strip=False)
            if key in keys:
                value = extract_value(tds, i)
                data[key] = value     
        return data
    except ConnectionError:
        return "ConnectionError"
    except TimeoutError:
        return "TimeoutError"

def extract_value(tds, i):
    key = tds[i].get_text(strip=False)
    if key == 'Status':
        img_tag = tds[i + 1].find('img')
        return img_tag.get('title') or img_tag.get('alt') if img_tag else ''
    elif key == 'Kursleitung':
        value = [a.get_text(strip=True) for a in tds[i + 1].find_all('a')]
        return ', '.join(value)
    else:
        return tds[i + 1].get_text(strip=True)

def findeKursDetailsMitKursNummer(kurs_nummer: str):
    kurs_link = ""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    kursliste_path = os.path.join(script_dir, '..', 'data', 'afae-alle-kurse.txt')
    with open(kursliste_path, 'r') as rf:
        kurse = rf.readlines()
        for kurs in kurse:
            kurs_nummer_pattern = rf"https://www\.akademie-fuer-aeltere\.de/programm/kw/bereich/kursdetails/kurs/{kurs_nummer}/kursname/.*"
            match = re.match(kurs_nummer_pattern, kurs)
            if match: 
                kurs_link = kurs.strip()
                break 
    if kurs_link:
        data = scrapeHtml(kurs_link, kurs_nummer)
        return handle_scrape_response(data)
    else: 
        return "Fehlerhafte Kursnummer. Überprüfen Sie die Korrektheit der Kursnummer."

def handle_scrape_response(data):
    if data not in ["ConnectionError", "TimeoutError"]:
        result = "\n".join([f"{key}: {value}" for key, value in data.items()])
        return result
    return f"Verbindung nicht möglich für Kursnummer."