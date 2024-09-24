# gui.py
import os
# +- GUI Modules -+ #
import tkinter as tk
from PIL import Image, ImageTk
from scraper import findeKursDetailsMitKursNummer

""" Definiere Trigger-Funktion für Button/Keyboard-Event """
def triggerSearch(event=None):
    kurs_nummer = entry.get()
    if kurs_nummer:
        ergebnis = findeKursDetailsMitKursNummer(kurs_nummer)   # rufe Logik-Funktion auf
        output_label.config(text=ergebnis)                      # packe Ergebnis ins Output-Fenster
        print("\n"+ergebnis+"\n")                                    # Zusätzlich Ausgabe im Terminal

""" Fensterprogramm Layout """
def startGui():
    global entry, output_label
    root = tk.Tk()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, '..', 'misc', 'afae-icon.ico')
    root.iconbitmap(icon_path)
    root.title("Akademie für Ältere - Kurs Finder")
    root.geometry("600x600")
    
    jpg_path = os.path.join(script_dir, '..', 'misc', 'afae-background.jpg')
    background_image = Image.open(jpg_path)
    bg_photo = ImageTk.PhotoImage(background_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    label = tk.Label(root, text="Kurs-Id:", bg="lightblue", font=("Calibri", 14), highlightbackground="#77CEEB", highlightthickness=3)
    label.place(x=90, y=55)
    entry = tk.Entry(root, font=("Calibri", 14), bg="lightgrey")
    entry.place(x=215, y=60, width=200)
    entry.bind('<Return>', triggerSearch)
    # Hier im Button wird die triggerSearch() Funktion on click oder mit [Enter] ausgeführt.
    button = tk.Button(root, text="Suchen", command=triggerSearch, font=("Calibri", 14, "bold"), bg="#ffeb3b", highlightbackground="#ffeb3b", highlightthickness=2, relief="raised")
    button.place(x=450, y=55)
    output_label = tk.Label(root, text="", bg="lightblue", font=("Calibri", 12), highlightbackground="#77CEEB", highlightthickness=4, justify="left")
    output_label.place(x=50, y=150, width=500, height=300)
    title_label = tk.Label(root, text="Kursinformationen: ", bg="lightblue", font=("Calibri", 14, "italic"))
    title_label.place(x=300, y=190, anchor='center')

    root.mainloop()