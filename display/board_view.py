import matplotlib.pyplot as plt
import numpy as np

scacchi = {'C': '♘', 'A': '♗', 'T': '♖', 'Q': '♕', 'K': '♔'}


class GraphicViewer:

  def __init__(self, size=8):
    self.size = size

  def board(self, asse):
    griglia = np.zeros((self.size, self.size))
    griglia[::2, 1::2] = 1
    griglia[1::2, ::2] = 1

    asse.imshow(griglia, cmap='Oranges', alpha=0.3)

    cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    rows = ['8', '7', '6', '5', '4', '3', '2', '1']

    asse.set_xticks(np.arange(self.size))
    asse.set_xticklabels(cols, fontsize=11, fontweight='bold')
    asse.set_yticks(np.arange(self.size))
    asse.set_yticklabels(rows, fontsize=11, fontweight='bold')
    asse.tick_params(left=False, bottom=False)

  def disegna_pezzi(self, asse, board_matrix):
    for r in range(self.size):
      for c in range(self.size):
        piece = board_matrix[r][c]
        symbol = scacchi.get(piece, '')
        if symbol:
          asse.text(c, r, symbol, fontsize=28, ha='center', va='center', color='darkblue', fontweight='bold')

  def posizionamento(self, board_matrix, title='Posizionamento'):
    figura, asse = plt.subplots(figsize=(6, 6))
    self.board(asse)
    self.disegna_pezzi(asse, board_matrix)
    plt.title(title, fontsize=13, pad=10, fontweight='bold')
    plt.tight_layout()
    plt.show()

  def visualizzazione_animata(self, sequenza_stati, delay=1.0, title_prefix='Passo'):
    plt.ion()
    fig, ax = plt.subplots(figsize=(6, 6))
    for t, stato in enumerate(sequenza_stati):
      ax.clear()
      self.board(ax)
      self.disegna_pezzi(ax, stato)
      ax.set_title(f'{title_prefix} t = {t}', fontsize=13, pad=10, fontweight='bold')
      fig.canvas.draw()
      fig.canvas.flush_events()
      plt.pause(delay)
    plt.ioff()
    plt.show()