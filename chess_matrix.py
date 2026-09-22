import copy
import random

# Usato da Z3
stato_iniziale = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['T', 'C', 'A', 'Q', 'K', 'A', 'C', 'T']] 

# Notazione x scacchi 
def tupla_stringa(r: int, c: int) -> str:
    col_char = chr(ord('A') + c)
    row_char = str(8-r)
    return f"{col_char}{row_char}"

# Ausiliaria 
def validità_mosse(r: int, c: int) -> bool:
    return (0 <= c < 8) and (0 <= r < 8)

# Usato da Z3
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
            direzioni.extend([(1, 1), (-1, 1), (1, -1), (-1, -1)])
        for dr, dc in direzioni:
            for passo in range(1,8):
                nr, nc = r + dr*passo, c + dc*passo
                if validità_mosse(nr, nc):
                    mosse.append((nr, nc))
                else: 
                    break # Ha toccato il bordo della scacchiera
    return mosse

# Usato da Z3
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

# Usato da Z3
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

# Per generazione di mosse casuali 
def genera_mosse_casuali(stato_base: list[list[str]], num_mosse: int) -> list[list[list[str]]]:
    cronologia = [copy.deepcopy(stato_base)] 
    stato_corrente = copy.deepcopy(stato_base) 
    for _ in range(num_mosse): 
        mosse_disponibili = [] 
        for r in range(8):
            for c in range(8): 
                pezzo = stato_corrente[r][c] 
                if pezzo != ".": 
                    candidati = mosse_pedine(pezzo, r, c) 
                    for nr, nc in candidati: 
                        if stato_corrente[nr][nc] == ".": 
                            inter = intersezioni((r, c), (nr, nc)) 
                            traiettoria_libera = all(stato_corrente[ir][ic] == "." for ir, ic in inter)
                            if traiettoria_libera: 
                                mosse_disponibili.append(((r, c), (nr, nc))) 
        if not mosse_disponibili: 
            break
        (src_r, src_c), (dst_r, dst_c) = random.choice(mosse_disponibili) 
        pezzo_mosso = stato_corrente[src_r][src_c] 
        stato_corrente[src_r][src_c] = "." 
        stato_corrente[dst_r][dst_c] = pezzo_mosso 
        cronologia.append(copy.deepcopy(stato_corrente))
    return cronologia
