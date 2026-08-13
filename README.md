# Retrograde Chess Analysis via SAT Solver

Questo progetto applica tecniche di **Model Checking** ed esecuzione simbolica al gioco degli scacchi. 
L'obiettivo è determinare se una data configurazione sulla scacchiera sia **raggiungibile**, ovvero se esista una sequenza valida di $N$ mosse legali che la generi a partire da uno stato iniziale.

---

## Obiettivo del progetto

Nel Model Checking, un sistema viene modellato come uno spazio degli stati e una relazione di transizione. In questo contesto:
* **Stato:** La disposizione dei pezzi sulla scacchiera in un dato istante $T$.
* **Transizione:** Una mossa legale rispettando le regole degli scacchi.
* **Quesito Formale:** Data una posizione finale $S_T$, il **SAT Solver** deve verificare la soddisfacibilità di una formula in **Forma Normale Congiuntiva (CNF)** che codifica l'esistenza di una sequenza di transizioni $S_0 \rightarrow S_1 \rightarrow \dots \rightarrow S_T$ valida.
