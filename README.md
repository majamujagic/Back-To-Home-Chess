# Back To Home Chess

Questo progetto, basato sul gioco degli scacchi, ci permette di prendere una scacchiera con un numero limitato di pedine, mescolare i pezzi con mosse casuali per poi utilizzare un **SAT Solver (Z3)** per calcolare la strada esatta che permette a tutte le pedine di tornare alla loro posizione iniziale senza scontrarsi.
Il programma gestisce le regole di movimento dei vari pezzi, evita le collisioni lungo le strade e mostra l'intero processo visivamente tramite un'animazione grafica con Matplotlib.

Progetto di Mujagic Maja per il corso di Computabilià, Complessità e Logica - Università degli Studi di Trieste

## Obiettivo del progetto

L'obiettivo centrale del progetto è applicare la logica proposizionale e la soddisfacibilità (SAT) per risolvere un problema di pianificazione e ricerca del percorso.
Per fare ciò ci avvaliamo del solver Z3 come motore di ragionamento logico, traducendo il problema nei seguenti concetti:
* **Stato:** La disposizione dei pezzi sulla scacchiera in un dato istante $T$.
* **Transizione:** Una mossa legale rispettando le regole degli scacchi.
* **Quesito Formale:** Data una posizione finale $S_T$, il **SAT Solver** deve verificare la soddisfacibilità di una formula in **Forma Normale Congiuntiva (CNF)** che codifica l'esistenza di una sequenza di transizioni $S_0 \rightarrow S_1 \rightarrow \dots \rightarrow S_T$ valida.
Z3 ci permette di analizzare simultaneamente tutte le condizioni e i vincoli imposti per trovare matematicamente l'assegnazione che soddisfa l'intera formula, garantendo la correttezza del percorso di ritorno.

## Struttura del codice

Il progetto è strutturato in diversi file nella cartella principale:

```text
├── ProgettoCCL/
│   ├── board_view.py      # Gestione della grafica e delle animazioni con Matplotlib
│   ├── chess_matrix.py    # Logica della scacchiera, regole dei pezzi e generazione casuale
│   ├── solver.py          # Configurazione dei vincoli e risoluzione del percorso con Z3
│   ├── main.py            # Script principale che coordina l'esecuzione del programma
│   └── README.md          # Documentazione del progetto
```
## Istruzioni e Installazione
### Librerie utilizzate:
* **Z3-solver**: Motore logico per la risoluzione dei problemi di soddisfacibilità (SMT/SAT).
* **Matplotlib**: Per la generazione della grafica e delle animazioni della scacchiera.
* **NumPy**: Per la gestione della matrice della scacchiera.
### Installazione
Assicurasi di avere Python installato sul computer. Dopodiché aprire il terminale all'interno della cartella del progetto e installare le librerie necessarie con il comando:
```bash
pip install z3-solver matplotlib numpy
```
Dopodichè puoi avviare il programma eseguendo lo script principale: 
```bash
python main.py
```
