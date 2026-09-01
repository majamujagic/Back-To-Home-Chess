pezzi = ['K', 'Q', 'T', 'A', 'C'] 
stato_iniziale = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['T', 'C', 'A', 'Q', 'K', 'A', 'C', 'T']
] 
# Converte la stringa leggibile degli scacchi nella tupla di indici 
def stringa_tupla(stringa: str) -> tuple[int, int]:
    col_id = stringa[0].upper()
    row_id = stringa[1]
    col = ord(col_id) - ord('A')
    row = 8 - int(row_id)
    return row, col

# Converte la tupla di indici in coordinate per gli scacchi 
def tupla_stringa(r: int, c: int) -> str:
    col_char = chr(ord('A') + c)
    row_char = str(8-r)
    return f"{col_char}{row_char}"

# Da coordinate 2D ad indice lineare 1D
def coordinate_sat(r: int, c: int) -> int:
    return r*8 + c

# Da indice lineare 1D a coordinate 2D
def sat_coordinate(id: int) -> tuple[int, int]:
    return id // 8, id % 8

# Restituisce un booleano per verfiicare se la mossa sta all'interno della scacchiera 
def validità_mosse(r: int, c: int) -> bool:
    return (0 <= c < 8) and (0 <= r < 8)

def mosse_pedine(pezzi: str, r: int, c: int) -> list[tuple[int,int]]:
    mosse = []
    if pezzi == 'C': # Cavallo
        mov_C = [(-2,-1), (-2, 1), (2, -1), (2,1), (1, -2), (1, 2), (-1, 2), (-1, -2)]
        for dr, dc in mov_C:
            nr, nc = r + dr, c + dc
            if validità_mosse(nr, nc):
                mosse.append((nr, nc))
    if pezzi == 'K': # Re
        mov_K = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in mov_K:
            nr, nc = r + dr, c + dc
            if validità_mosse(nr, nc):
                mosse.append((nr, nc))           
    if  pezzi in ['T', 'A', 'Q']: # Torre - Alfiere - Regina
        direzioni = []
        if pezzi in ['T', 'Q']:
            direzioni.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
        if pezzi in ['A', 'Q']:
            direzioni. extend([(1, 1), (-1, 1), (1, -1), (-1, -1)])
        for dr, dc in direzioni:
            for passo in range(1,8):
                nr, nc = r + dr*passo, c + dc*passo
                if validità_mosse(nr, nc):
                    mosse.append((nr, nc))
                else: 
                    break # Ha toccato il bordo della scacchiera
    return mosse

def intersezioni(c_start: tuple[int,int], c_end: tuple[int,int]) -> list[tuple[int,int]]:
    r1, c1 = c_start
    r2, c2 = c_end
    dr = r2 - r1
    dc = c2 - c1
    if max(abs(dr), abs(dc)) <= 1 or (abs(dr)*abs(dc)) == 2:
        return []
    step_r = (dr//abs(dr)) if dr != 0 else 0
    step_c = (dc//abs(dc)) if dc != 0 else 0
    intermedio = []
    current_r, current_c = r1 + step_r, c1 + step_c 
    while(current_r, current_c) != (r2, c2):
        intermedio.append((current_r, current_c))
        current_r += step_r
        current_c += step_c 
    return intermedio

import copy
import random

def genera_mosse_casuali(stato_base: list[list[str]], num_mosse: int) -> list[list[list[str]]]:
    cronologia = [copy.deepcopy(stato_base)] # Conterrà tutti gli dtsti temporali partendo da t = 0
    stato_corrente = copy.deepcopy(stato_base) # Matrice su cui applichiamo gli spostaenti passo dopo passo 
    # copy.deepcopy crea copie indipendenti in memoria della scacchiera iniziale 

    for _ in range(num_mosse): # Avvia un ciclo che tenta di eseguire K mosse
        mosse_disponibili = [] # Inizializza una lista vuota che ad ogni turno raccoglie tutte le mosse legali possibili tra tutti i pezzi presenti
        for r in range(8):
            for c in range(8): 
                pezzo = stato_corrente[r][c] 
                if pezzo != ".": # Se la casella non è vuota prendiamo la pedina in questione e la sua posizione
                    candidati = mosse_pedine(pezzo, r, c) # E verifiachiamo tutte le mosse fattibile da questa
                    for nr, nc in candidati: # cicla su ogni potenziale casella d'arrivo 
                        if stato_corrente[nr][nc] == ".": # E se è libera 
                            inter = intersezioni((r, c), (nr, nc)) # Calcola l'elenco delle caselle attraversate dal pezzo per adndare da r,c a nr, nc
                            traiettoria_libera = all(stato_corrente[ir][ic] == "." for ir, ic in inter) # Verifica che tutte le caselle nella sua ipotetica traiettoria siano libere se no ritorna False 
                            if traiettoria_libera: # Se la traiettoria è libera
                                mosse_disponibili.append(((r, c), (nr, nc))) # Aggiunge alla lista delle mosse_disponibili la coppia
        if not mosse_disponibili: # Controllo: se nessun pezzo ha mosse legali disponibili si fa un break 
            break
        (src_r, src_c), (dst_r, dst_c) = random.choice(mosse_disponibili) # Esrtrae casualmente un mossa tra tutte quelle valide trovate 
        pezzo_mosso = stato_corrente[src_r][src_c] # Salva nella lista l'identificare del pezzo che si trova nella casella di partenza
        stato_corrente[src_r][src_c] = "." # Svuota la casella di partenza
        stato_corrente[dst_r][dst_c] = pezzo_mosso # Scrive il pezzo nella nuova casella di destinazione 
        cronologia.append(copy.deepcopy(stato_corrente))
    return cronologia

def estrai_coordinate(stato: list[list[str]]) -> dict[str, list[tuple[int,int]]]:
    posizioni = {}
    for r in range(8):
        for c in range(8):
            pezzo = stato[r][c]
            if pezzo != '.':
                if pezzo not in posizioni:
                    posizioni[pezzo] = []
                posizioni[pezzo].append((r,c))
    return posizioni
    