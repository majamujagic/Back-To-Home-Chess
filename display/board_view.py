import matplotlib.pyplot as plt
import numpy as np

# Pedine Bianche (no pedoni)
scacchi = {'C': '♘', 'A': '♗', 'T': '♖', 'Q': '♕', 'K': '♔'} 

class GraphicViewer:
    def __init__(self, size=8):
        self.size = size

    def board(self, asse):  # Impostiamo la griglia e le coordinate
        griglia = np.zeros((self.size, self.size))
        griglia[::2, 1::2] = 1
        griglia[1::2, ::2] = 1
        
        # Corretto: 'alpha' (singolare)
        asse.imshow(griglia, cmap='Oranges', alpha=0.3)
        
        # Corretto: variabili coerenti e nomi metodi Matplotlib giusti
        cols = ['A','B','C','D','E','F','G','H'] 
        rows = ['8','7','6','5','4','3','2','1'] 
        
        asse.set_xticks(np.arange(self.size))
        asse.set_xticklabels(cols, fontsize=11, fontweight='bold')
        
        asse.set_yticks(np.arange(self.size))
        asse.set_yticklabels(rows, fontsize=11, fontweight='bold')
        
        asse.tick_params(left=False, bottom=False)

    def posizionamento(self, board_matrix, title='Posizionamento'):
        figura, asse = plt.subplots(figsize=(6, 6))
        self.board(asse)
        
        for r in range(self.size):
            for c in range(self.size):
                piece = board_matrix[r][c]
                symbol = scacchi.get(piece, '')
                if symbol:
                    # Corretto: usa 'asse' anziché 'ax'
                    asse.text(c, r, symbol, fontsize=28, ha='center', va='center', 
                              color='darkblue', fontweight='bold')
        
        # Corretta l'indentazione: queste righe devono stare DENTRO il metodo
        plt.title(title, fontsize=13, pad=10, fontweight='bold')
        plt.tight_layout()
        plt.show()