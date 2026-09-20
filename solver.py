from z3 import *
from chess_matrix import intersezioni, mosse_pedine, stato_iniziale, estrai_coordinate

def impostazione_x_soluzione(stato_finale_z):
    posizioni_target = {} 
    for r in range(8):
        for c in range(8):
            p = stato_iniziale[r][c]
            if p != '.':
                if p not in posizioni_target:
                   posizioni_target[p] = []
                posizioni_target[p].append((r,c))
                
    start_pedina = estrai_coordinate(stato_finale_z) 
    id_pezzi = [] 
    partenza = {} 
    arrivo = {} 

    for nome_pezzo, starts in start_pedina.items():
        targets = list(posizioni_target[nome_pezzo])
        targets_disponibili = list(targets)
        pezzi_da_assegnare = []
        for c_partenza in starts:
            if c_partenza in targets_disponibili:
                targets_disponibili.remove(c_partenza)
                istanza_id = f'{nome_pezzo}_{len(id_pezzi)}'
                id_pezzi.append((istanza_id, nome_pezzo))
                partenza[istanza_id] = c_partenza
                arrivo[istanza_id] = c_partenza  
            else:
                pezzi_da_assegnare.append(c_partenza)
                
        for c_partenza in pezzi_da_assegnare:
            if targets_disponibili:
                best_t = min(targets_disponibili, key=lambda t: abs(t[0] - c_partenza[0]) + abs(t[1] - c_partenza[1]))
                targets_disponibili.remove(best_t)
            else:
                best_t = targets[0] 
            istanza_id = f'{nome_pezzo}_{len(id_pezzi)}'
            id_pezzi.append((istanza_id, nome_pezzo))
            partenza[istanza_id] = c_partenza
            arrivo[istanza_id] = best_t
            
    return id_pezzi, partenza, arrivo

def soluzione_z3(id_pezzi, partenza, arrivo, t_max = 10):
    inst_list = [item[0] for item in id_pezzi]
    pezzi_immobili = {inst for inst in inst_list if partenza[inst] == arrivo[inst]}
    pezzi_mobili = [inst for inst in inst_list if inst not in pezzi_immobili]

    for T in range(1, t_max + 1):
        print(f'Tentativo di risoluzione con T = {T}...')
        s = Solver()
        pos = {}
        for inst, _ in id_pezzi:
            for t in range(T + 1):
                pos[(inst, t, 'r')] = Int(f'{inst}_t{t}_r')
                pos[(inst, t, 'c')] = Int(f'{inst}_t{t}_c')
        for inst, _ in id_pezzi:
            r_init, c_init = partenza[inst]
            r_end, c_end = arrivo[inst]
            s.add(pos[(inst, 0, 'r')] == r_init)
            s.add(pos[(inst, 0, 'c')] == c_init)
            s.add(pos[(inst, T, 'r')] == r_end)
            s.add(pos[(inst, T, 'c')] == c_end)
            if inst in pezzi_immobili:
                for t in range(T + 1):
                    s.add(pos[(inst, t, 'r')] == r_init)
                    s.add(pos[(inst, t, 'c')] == c_init)

        for t in range(T):
            for inst, _ in id_pezzi:
                r = pos[(inst, t, 'r')]
                c = pos[(inst, t, 'c')]
                s.add(And(r >= 0, r < 8, c >= 0, c < 8))
                r_next = pos[(inst, t + 1, 'r')]
                c_next = pos[(inst, t + 1, 'c')]
                s.add(And(r_next >= 0, r_next < 8, c_next >= 0, c_next < 8))
            for i in range(len(inst_list)):
                for j in range(i + 1, len(inst_list)):
                    p1 = inst_list[i]
                    p2 = inst_list[j]
                    s.add(Or(pos[(p1, t, 'r')] != pos[(p2, t, 'r')], pos[(p1, t, 'c')] != pos[(p2, t, 'c')]))
                    s.add(Or(pos[(p1, t + 1, 'r')] != pos[(p2, t + 1, 'r')], pos[(p1, t + 1, 'c')] != pos[(p2, t + 1, 'c')]))
            for inst, p_type in id_pezzi:
                if inst in pezzi_immobili:
                    continue  
                r_curr = pos[(inst, t, 'r')]
                c_curr = pos[(inst, t, 'c')]
                r_next = pos[(inst, t + 1, 'r')]
                c_next = pos[(inst, t + 1, 'c')]
                condizioni_mossa = []
                condizioni_mossa.append(And(r_next == r_curr, c_next == c_curr))
                for r_val in range(8):
                    for c_val in range(8):
                        m_list = mosse_pedine(p_type, r_val, c_val)
                        base_pos_cond = And(r_curr == r_val, c_curr == c_val)
                        for nr, nc in m_list:
                            inter = intersezioni((r_val, c_val), (nr, nc))
                            if not inter:
                                condizioni_mossa.append(And(base_pos_cond, r_next == nr, c_next == nc))
                            else:
                                inter_clauses = []
                                for ir, ic in inter:
                                    cel_libera_checks = []
                                    for alt_inst, _ in id_pezzi:
                                        if alt_inst != inst:
                                            cel_libera_checks.append(
                                                Or(pos[(alt_inst, t, 'r')] != ir, pos[(alt_inst, t, 'c')] != ic))
                                    if cel_libera_checks:
                                        inter_clauses.append(And(*cel_libera_checks))
                                if inter_clauses:
                                    condizioni_mossa.append(And(base_pos_cond, r_next == nr, c_next == nc, And(*inter_clauses)))
                                else:
                                    condizioni_mossa.append(And(base_pos_cond, r_next == nr, c_next == nc))
                
                if condizioni_mossa:
                    s.add(Or(condizioni_mossa))
                    
        if s.check() == sat:
            modello = s.model()
            print(f'Soluzione trovata con successo in T = {T} passi!\n')
            risultato_passi = {}
            for inst, _ in id_pezzi:
                percorso_pezzo = []
                for t in range(T + 1):
                    rv = modello.evaluate(pos[(inst, t, 'r')]).as_long()
                    cv = modello.evaluate(pos[(inst, t, 'c')]).as_long()
                    percorso_pezzo.append((rv, cv))
                risultato_passi[inst] = percorso_pezzo
            return risultato_passi

    print("Nessuna soluzione trovata entro l'orizzonte massimo.")
    return None