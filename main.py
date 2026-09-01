from chess_logic.chess_matrix import (coordinate_sat, estrai_coordinate, genera_mosse_casuali, stato_iniziale, tupla_stringa)
from display.board_view import GraphicViewer

numero_mosse = int(input('Inserire il numero di mosse: '))
viewer = GraphicViewer()

print(f"Generazione di {numero_mosse} mosse casuali in corso...")
cronologia = genera_mosse_casuali(stato_iniziale, num_mosse = numero_mosse)
stato_rimescolato = cronologia[-1]

configurazione_scramble = estrai_coordinate(stato_rimescolato)
print('Dati di partenza per il Sat Solver al tempo t = 0')
for pezzo, coordinate in configurazione_scramble.items():
  for r, c in coordinate:
    idx_sat = coordinate_sat(r, c)
    notazione = tupla_stringa(r, c)
    print(f'Pezzo {pezzo}: Matrice=({r}, {c}) | Scacchi={notazione} | Indice_SAT={idx_sat}')
print('Avvio animazione su Matplotlib...')
viewer.visualizzazione_animata(cronologia, delay = 0.8, title_prefix =' Posizioni')