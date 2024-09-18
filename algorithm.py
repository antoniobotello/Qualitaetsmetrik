
import numpy as np
from typing import Dict


def finde_unternetze(scheitelpunkte_dict: Dict) -> Dict:
    zusammenhängendes_unternetz = []

    # Konvertiere die Schlüssel und Werte in ganze Zahlen und speichere die Werte als Sets
    scheitelpunkte_dict = {int(k): set(map(int, v)) for k, v in scheitelpunkte_dict.items()}

    # Erstelle eine Menge aller Scheitelpunkte (Knoten), sowohl aus den Schlüsseln als auch den Werten
    alle_scheitelpunkte = set(scheitelpunkte_dict.keys())
    for werte in scheitelpunkte_dict.values():
        alle_scheitelpunkte.update(werte)

    besucht = set()  # Set zum Speichern der bereits besuchten Knoten

    # Breitensuche (BFS) zum Finden von zusammenhängenden Unternetzen
    def bfs(scheitelpunkt):
        warteschlange = [scheitelpunkt]  
        unternetz = set()  # Set für das aktuelle Unternetz
        while warteschlange:
            aktueller_scheitelpunkt = warteschlange.pop(0) 
            if aktueller_scheitelpunkt not in besucht: 
                besucht.add(aktueller_scheitelpunkt)  
                unternetz.add(aktueller_scheitelpunkt) 
                # Füge alle unbesuchten Nachbarn des Knotens zur Warteschlange hinzu
                for nachbar in scheitelpunkte_dict.get(aktueller_scheitelpunkt, []):  
                    if nachbar not in besucht:
                        warteschlange.append(nachbar)
        return unternetz  # Gib das gefundene Unternetz zurück

    # Finde alle verbundenen Unternetze
    for scheitelpunkt in scheitelpunkte_dict:  
        if scheitelpunkt not in besucht:  
            unternetz = bfs(scheitelpunkt)  # Finde das zugehörige Unternetz über BFS
            zusammenhängendes_unternetz.append(unternetz)  # Füge das Unternetz zur Liste hinzu
            besucht.update(unternetz)  # Markiere alle Knoten des Unternetzes als besucht

    # Vereine Unternetze, die durch gemeinsame Knoten verbunden sind
    #Nachdem alle initialen Unternetze gefunden sind, prüft der Algorithmus auf mögliche Zusammenführungen von Unternetze, die indirekt durch gemeinsame Scheitelpunkte verbunden sind.
    for i in range(len(zusammenhängendes_unternetz)):
        for j in range(i+1, len(zusammenhängendes_unternetz)):
            erste_menge = zusammenhängendes_unternetz[i]
            zweite_menge = zusammenhängendes_unternetz[j]
            # Prüfe, ob es gemeinsame Scheitelpunkte zwischen den Unternetzen gibt
            for iterator_zweite in zweite_menge:
                for werte_zweite in scheitelpunkte_dict.get(iterator_zweite):
                    if werte_zweite in erste_menge:
                        # Vereine die beiden Unternetze zu einem neuen Unternetz
                        neues_unternetz = zusammenhängendes_unternetz[i].union(zusammenhängendes_unternetz[j])
                        # Entferne die beiden alten Unternetze und füge das neue Unternetz hinzu
                        zusammenhängendes_unternetz.pop(i)
                        zusammenhängendes_unternetz.pop(j-1)
                        zusammenhängendes_unternetz.insert(0, neues_unternetz)

    # Erstelle ein Dictionary, das die Größe der generierten Unternetze enthält
    unternetze_dict = {}
    for i in range(len(zusammenhängendes_unternetz)):
        unternetze_dict[f'unternetz {i}'] = len(zusammenhängendes_unternetz[i])

    return unternetze_dict 


# Gibt eine Liste mit der Größe jedes Clusters zurück
def berechne_groessen(subteile):
    groessen = []
    for i in subteile:
        groessen.append(subteile[i])
    return groessen



def konzentrationsindex(groessen):
    gesamt = np.sum(groessen)
    if gesamt == 0:
        return 0
    prozente = (groessen / gesamt) * 100
    hhi = np.sum(prozente ** 2)
    # Normalisierung des HHI auf einen Bereich von 0 bis 1
    normalisiertes_hhi = hhi / 10000
    return normalisiertes_hhi



def bewertung_anzahl_untergitter(anzahl_untergitter, n_max):
    return 1 - (anzahl_untergitter - 1) / (n_max - 1)



def gesamtqualitaet(groessen, n_max, alpha=0.5, beta=0.5):
    anzahl_untergitter = len(groessen)
    h_n = konzentrationsindex(np.array(groessen))
    u = bewertung_anzahl_untergitter(anzahl_untergitter, n_max)
    return h_n, u, alpha * h_n + beta * u
