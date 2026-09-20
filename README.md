# Back To Home Chess

Questo progetto, basato sul gioco degli scacchi, ci permette di prendere una scacchiera con un numero limitato di pedine, mescolare i pezzi con mosse casuali per poi utilizzare un **SAT Solver (Z3)** per calcolare la strada esatta che permette a tutte le pedine di **tornare alla loro posizione iniziale** senza scontrarsi.
Il programma gestisce le regole di movimento dei vari pezzi, evita le collisioni lungo le strade e mostra l'intero processo visivamente tramite un'animazione grafica con Matplotlib.

## Obiettivo del progetto

Nel Model Checking, un sistema viene modellato come uno spazio degli stati e una relazione di transizione. In questo contesto:
* **Stato:** La disposizione dei pezzi sulla scacchiera in un dato istante $T$.
* **Transizione:** Una mossa legale rispettando le regole degli scacchi.
* **Quesito Formale:** Data una posizione finale $S_T$, il **SAT Solver** deve verificare la soddisfacibilità di una formula in **Forma Normale Congiuntiva (CNF)** che codifica l'esistenza di una sequenza di transizioni $S_0 \rightarrow S_1 \rightarrow \dots \rightarrow S_T$ valida.

## Struttura del codice

Il progetto è strutturato in diversi file nella cartella principale:

```text
├── ProgettoCCL/
│   ├── board_view.py      # Gestione della grafica e delle animazioni con Matplotlib
│   ├── chess_matrix.py    # Logica della scacchiera, regole dei pezzi e generazione casuale
│   ├── solver.py          # Configurazione dei vincoli e risoluzione del percorso con Z3
│   ├── main.py            # Script principale che coordina l'esecuzione del programma
│   └── README.md          # Documentazione del progetto

