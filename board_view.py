import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

scacchi = {'C': '♘', 'A': '♗', 'T': '♖', 'Q': '♕', 'K': '♔'}

class GraphicViewer:

  def __init__(self, size=8):
    self.size = size

  def board(self, asse):
    griglia = np.zeros((self.size, self.size))
    griglia[::2, 1::2] = 1
    griglia[1::2, ::2] = 1
    cmap_scacchi = ListedColormap(['#f0d9b5', '#b58863'])
    asse.imshow(griglia, cmap=cmap_scacchi, extent=[-0.5, 7.5, 7.5, -0.5])
    cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    rows = ['8', '7', '6', '5', '4', '3', '2', '1']
    asse.set_xticks(np.arange(self.size))
    asse.set_xticklabels(cols, fontsize=11, fontweight='bold', color='#333333')
    asse.set_yticks(np.arange(self.size))
    asse.set_yticklabels(rows, fontsize=11, fontweight='bold', color='#333333')
    asse.tick_params(left=False, bottom=False)
    asse.set_aspect('equal')

  def disegna_pezzi(self, asse, board_matrix):
    for r in range(self.size):
      for c in range(self.size):
        piece = board_matrix[r][c]
        symbol = scacchi.get(piece, '')
        if symbol:
          asse.text(c, r, symbol, fontsize=32, ha='center', va='center', color='#1a1a1a', fontweight='bold', zorder=3)

  def visualizzazione_animata(self, sequenza_stati, delay=1.0, title_prefix='Passo'):
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#f8f9fa')
    for t, stato in enumerate(sequenza_stati):
      ax.clear()
      self.board(ax)
      self.disegna_pezzi(ax, stato)
      ax.set_title(f'{title_prefix} t = {t}', fontsize=13, pad=12, fontweight='bold', color='#222222')
      fig.canvas.draw()
      fig.canvas.flush_events()
      plt.pause(delay)
      
    plt.ioff()
    plt.show()