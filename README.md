# Back To Home Chess

Questo progetto prende una scacchiera con un numero limitato di pezzi, li mescola mediante mosse casuali e poi usa Z3 per verificare se esiste una sequenza di spostamenti che riporti ogni pezzo alla sua posizione originaria senza collisioni.
Il programma gestisce le regole di movimento dei vari pezzi, evita le collisioni lungo le strade e mostra l'intero processo visivamente tramite un'animazione grafica con Matplotlib.

Progetto di Mujagic Maja 

## Obiettivo del progetto

L'obiettivo centrale del progetto è applicare la logica proposizionale e la soddisfacibilità (SAT) per risolvere un problema di pianificazione e ricerca del percorso.
Per fare ciò ci avvaliamo del solver Z3 come motore di ragionamento logico, traducendo il problema nei seguenti concetti:
* **Stato:** La disposizione dei pezzi sulla scacchiera in un dato istante $T$.
* **Transizione:** Una transizione corrisponde al movimento legale di un pezzo secondo le regole geometriche implementate nel progetto.
* **Quesito Formale:** Dato uno stato iniziale mescolato `S_0`, il solver verifica se esiste una sequenza di stati `S_0 -> S_1 -> ... -> S_T` che porti i pezzi alla configurazione iniziale, rispettando i vincoli di movimento e di non collisione.
Z3 analizza simultaneamente tutte le condizioni e i vincoli imposti per trovare un'assegnazione delle variabili che li soddisfi tutti, determinando così un percorso valido di ritorno.

## Struttura del codice

Il progetto è strutturato in diversi file nella cartella principale:

```text
├── board_view.py      # Gestione della grafica e delle animazioni con Matplotlib
├── chess_matrix.py    # Logica della scacchiera, regole dei pezzi e generazione casuale
├── solver.py          # Configurazione dei vincoli e risoluzione del percorso con Z3
├── main.py            # Script principale che coordina l'esecuzione del programma
└── README.md          # Documentazione del progetto
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
