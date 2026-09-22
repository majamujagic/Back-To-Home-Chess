from z3 import (Solver,Bool,And,Or,Not,Sum,If,is_true,sat)
from chess_matrix import intersezioni, mosse_pedine, stato_iniziale, estrai_coordinate

def impostazione_x_soluzione(stato_finale_z):
    posizioni_target = {}
    for r in range(8):
        for c in range(8):
            tipo_pezzo = stato_iniziale[r][c]
            if tipo_pezzo != '.':
                if tipo_pezzo not in posizioni_target:
                    posizioni_target[tipo_pezzo] = []
                posizioni_target[tipo_pezzo].append((r, c))

    posizioni_partenza = estrai_coordinate(stato_finale_z)
    id_pezzi = []
    partenza = {}
    arrivo = {}

    for tipo_pezzo, posizioni in posizioni_partenza.items():
        targets = list(posizioni_target[tipo_pezzo])
        targets_disponibili = list(targets)
        pezzi_da_assegnare = []
        for posizione_partenza in posizioni:
            if posizione_partenza in targets_disponibili:
                targets_disponibili.remove(posizione_partenza)
                identificatore = f'{tipo_pezzo}_{len(id_pezzi)}'
                id_pezzi.append((identificatore, tipo_pezzo))
                partenza[identificatore] = posizione_partenza
                arrivo[identificatore] = posizione_partenza
            else:
                pezzi_da_assegnare.append(posizione_partenza)

        for posizione_partenza in pezzi_da_assegnare:
            if targets_disponibili:
                target_migliore = min(targets_disponibili,key=lambda target: (abs(target[0] - posizione_partenza[0])+ abs(target[1] - posizione_partenza[1])))
                targets_disponibili.remove(target_migliore)
            else:
                target_migliore = targets[0]

            identificatore = f'{tipo_pezzo}_{len(id_pezzi)}'
            id_pezzi.append((identificatore, tipo_pezzo))
            partenza[identificatore] = posizione_partenza
            arrivo[identificatore] = target_migliore
    return id_pezzi, partenza, arrivo

def crea_variabili_booleani(id_pezzi, T):
    x = {}
    for identificatore, _ in id_pezzi:
        for t in range(T + 1):
            for r in range(8):
                for c in range(8):
                    nome = (f'{identificatore}_t{t}_r{r}_c{c}')
                    x[(identificatore, t, r, c)] = Bool(nome)
    return x

def aggiungi_almeno_una_posizione(solver, x, id_pezzi, T):
    for identificatore, _ in id_pezzi:
        for t in range(T + 1):
            possibili_posizioni = []
            for r in range(8):
                for c in range(8):
                    possibili_posizioni.append(x[(identificatore, t, r, c)])
            solver.add(Or(possibili_posizioni))

def aggiungi_al_massimo_una_posizione(solver, x, id_pezzi, T):
    caselle = [(r, c) for r in range(8) for c in range(8)]
    for identificatore, _ in id_pezzi:
        for t in range(T + 1):
            for i in range(len(caselle)):
                for j in range(i + 1, len(caselle)):
                    r1, c1 = caselle[i]
                    r2, c2 = caselle[j]
                    solver.add(Or(Not(x[(identificatore, t, r1, c1)]), Not(x[(identificatore, t, r2, c2)])))

def aggiungi_vincoli_inizio_fine(solver, x, id_pezzi, partenza, arrivo,T):
    for identificatore, _ in id_pezzi:
        r_init, c_init = partenza[identificatore]
        r_end, c_end = arrivo[identificatore]
        solver.add(x[(identificatore, 0, r_init, c_init)])
        solver.add(x[(identificatore, T, r_end, c_end)])

def aggiungi_pezzi_immobili(solver,x,id_pezzi,partenza,arrivo,T):
    for identificatore, _ in id_pezzi:
        if partenza[identificatore] != arrivo[identificatore]:
            continue
        r, c = partenza[identificatore]
        for t in range(T + 1):
            solver.add(x[(identificatore, t, r, c)])

def aggiungi_vincoli_non_collisione(solver, x, id_pezzi, T):
    for t in range(T + 1):
        for r in range(8):
            for c in range(8):
                for i in range(len(id_pezzi)):
                    for j in range(i + 1, len(id_pezzi)):
                        pezzo_1 = id_pezzi[i][0]
                        pezzo_2 = id_pezzi[j][0]
                        solver.add(Or(Not(x[(pezzo_1, t, r, c)]),Not(x[(pezzo_2, t, r, c)])))

def aggiungi_vincoli_mosse(solver, x, id_pezzi, partenza, arrivo, T):
    for t in range(T):
        for identificatore, tipo_pezzo in id_pezzi:
            if partenza[identificatore] == arrivo[identificatore]:
                continue
            condizioni_mossa = []
            for r_val in range(8):
                for c_val in range(8):
                    posizione_corrente = x[(identificatore, t, r_val, c_val)]
                    posizione_successiva = x[(identificatore, t + 1, r_val, c_val)]
                    condizioni_mossa.append(And(posizione_corrente, posizione_successiva))
                    mosse = mosse_pedine(tipo_pezzo, r_val, c_val)
                    for nr, nc in mosse:
                        celle_intermedie = intersezioni((r_val, c_val),(nr, nc))
                        condizioni_celle_libere = []
                        for ir, ic in celle_intermedie:
                            condizioni_altri_pezzi = []
                            for altro_pezzo, _ in id_pezzi:
                                if altro_pezzo == identificatore:
                                    continue
                                condizioni_altri_pezzi.append(Not(x[(altro_pezzo, t, ir, ic)]))
                            if condizioni_altri_pezzi:
                                condizioni_celle_libere.append(And(condizioni_altri_pezzi))
                        posizione_successiva = x[(identificatore, t+1, nr, nc)]
                        if condizioni_celle_libere:
                            condizioni_mossa.append(
                                And(posizione_corrente, posizione_successiva, And(*condizioni_celle_libere)))
                        else:
                            condizioni_mossa.append(
                                And(posizione_corrente, posizione_successiva))
            solver.add(Or(condizioni_mossa))

def estrai_percorso_dal_modello(modello, x, id_pezzi, T):
    risultato_passi = {}
    for identificatore, _ in id_pezzi:
        percorso_pezzo = []
        for t in range(T + 1):
            posizione_trovata = None
            for r in range(8):
                for c in range(8):
                    variabile = x[(identificatore, t, r, c)]
                    valore = modello.evaluate(variabile, model_completion=True)
                    if is_true(valore):
                        posizione_trovata = (r, c)
                        break
                if posizione_trovata is not None:
                    break
            percorso_pezzo.append(posizione_trovata)
        risultato_passi[identificatore] = percorso_pezzo
    return risultato_passi


def soluzione_z3(id_pezzi, partenza, arrivo, t_max=10):
    for T in range(1, t_max + 1):
        print(f'Tentativo di risoluzione con T = {T}...')
        solver = Solver()
        x = crea_variabili_booleani(id_pezzi, T)
        aggiungi_almeno_una_posizione(solver, x, id_pezzi, T)
        aggiungi_al_massimo_una_posizione(solver, x, id_pezzi, T)
        aggiungi_vincoli_inizio_fine(solver, x, id_pezzi, partenza, arrivo, T)
        aggiungi_pezzi_immobili(solver, x, id_pezzi, partenza, arrivo, T)
        aggiungi_vincoli_non_collisione(solver, x, id_pezzi, T)
        aggiungi_vincoli_mosse(solver, x, id_pezzi, partenza, arrivo, T)
        if solver.check() == sat:
            print(f'Soluzione trovata con successo in T = {T} passi!')
            modello = solver.model()
            return estrai_percorso_dal_modello(modello, x, id_pezzi, T)
    print('Nessuna soluzione trovata entro il bound massimo.')
    return None