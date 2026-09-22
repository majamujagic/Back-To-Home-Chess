from chess_matrix import estrai_coordinate, genera_mosse_casuali, stato_iniziale, tupla_stringa
from board_view import GraphicViewer
from solver import soluzione_z3, impostazione_x_soluzione

numero_mosse = int(input('Inserire il numero di mosse (MAX: 6): '))
viewer = GraphicViewer()
print(f"Generazione di {numero_mosse} mosse casuali ->")
cronologia = genera_mosse_casuali(stato_iniziale, num_mosse = numero_mosse)
stato_rimescolato = cronologia[-1]
configurazione = estrai_coordinate(stato_rimescolato)
print('Dati di partenza per il Sat Solver al tempo t = 0')
for pezzo, coordinate in configurazione.items():
  for r, c in coordinate:
    notazione = tupla_stringa(r, c)
    print(f'Pezzo {pezzo}: Matrice=({r}, {c}) | Scacchi: {notazione}')
print('Avvio animazione su Matplotlib...')
viewer.visualizzazione_animata(cronologia, delay = 1.5, title_prefix='Posizioni')

print('Avvio del SAT Solver (Z3) per il ritorno alla posizione iniziale ->')
id_pezzi, partenza, arrivo = impostazione_x_soluzione(stato_rimescolato)
risultato_z3 = soluzione_z3(id_pezzi, partenza, arrivo, t_max=len(cronologia))
if risultato_z3:
    print('Passi compiuti dalle pedine per tornare in posizione originale:')
    for pedina_id, percorso in risultato_z3.items():
        print(f'Pezzo [{pedina_id}]:')
        for t, (r, c) in enumerate(percorso):
            notazione_scacchi = tupla_stringa(r, c)
            print(f'  Tempo t={t}: Matrice=({r}, {c}) | Scacchi: {notazione_scacchi}')
    print('Preparazione animazione...')
    T_max_soluzione = len(next(iter(risultato_z3.values()))) - 1
    cronologia_ritorno = []
    for t in range(T_max_soluzione + 1):
        matrice_t = [['.' for _ in range(8)] for _ in range(8)]
        for inst, percorso in risultato_z3.items():
            pezzo_tipo = inst.split('_')[0]
            r, c = percorso[t]
            matrice_t[r][c] = pezzo_tipo
        cronologia_ritorno.append(matrice_t)
    print('Avvio animazione di ritorno su Matplotlib...')
    viewer.visualizzazione_animata(cronologia_ritorno, delay = 2.0, title_prefix='Ritorno')