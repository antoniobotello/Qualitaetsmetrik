import json 
from typing import List, Dict
from algorithm import finde_unternetze, berechne_groessen, gesamtqualitaet

faces_data_json = 'pikachu/pikachu_1.json'


with open(faces_data_json, 'r') as file:
    faces_data = json.load(file)       


def erstelle_nachbarschafts_dictionary(vollständige_scheitelpunkte_liste: List[List[int]]) -> Dict:
    
    # Initialisiere ein leeres Dictionary, um die Nachbarschaften der Scheitelpunkte zu speichern
    scheitelpunkte_dict = {}
    
    for teilliste in vollständige_scheitelpunkte_liste:
        for scheitelpunkt in teilliste:
            # Falls der Scheitelpunkt bereits im Dictionary existiert, füge die Nachbarn hinzu
            if scheitelpunkt in scheitelpunkte_dict:
                # Füge alle anderen Knoten der Teilliste als Nachbarn hinzu, außer dem aktuellen Scheitelpunkt selbst
                scheitelpunkte_dict[scheitelpunkt].extend([x for x in teilliste if x != scheitelpunkt])
            else:
                # Wenn der Scheitelpunkt noch nicht im Dictionary ist, erstelle einen neuen Eintrag
                scheitelpunkte_dict[scheitelpunkt] = [x for x in teilliste if x != scheitelpunkt]
    
    # Gib ein Dictionary züruck, wobei alle Scheitelpunkte des 3D-Modells als Schlüssel und ihre verbundene Scheitelpunkte als Values gespeichert werden
    return scheitelpunkte_dict


if __name__ == '__main__':

    clusters = erstelle_nachbarschafts_dictionary(faces_data)
    clusters = finde_unternetze(clusters)
    tamano_submallas = berechne_groessen(clusters)

    h_n, u, q = gesamtqualitaet(tamano_submallas, 10)
 
    clusters['H'] = h_n
    clusters['U'] = u
    clusters['Q'] = q

    with open('pikachu_test.json', 'w') as json_file:
        json.dump(clusters,json_file)
 