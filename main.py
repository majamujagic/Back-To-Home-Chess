from chess_logic.chess_matrix import stato_iniziale, stringa_tupla, mosse_pedine
from display.board_view import GraphicViewer

r, c = stringa_tupla("B1")
pezzo = stato_iniziale[r][c]  # Sarà 'N'
mosse = mosse_pedine(pezzo, r, c)

print(f"Pezzo trovato in B1: {pezzo}")
print(f"Mosse legali calcolate: {mosse}")

viewer = GraphicViewer()
viewer.posizionamento(stato_iniziale, title = 'Scacchiera Iniziale')
