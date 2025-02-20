# Ricerca Codici ATECO 2025

Un'applicazione Streamlit per la ricerca e visualizzazione efficiente dei codici ATECO 2025, con funzionalità di ricerca multipla e filtri dettagliati.

## Caratteristiche

- Ricerca per codice ATECO
- Ricerca per descrizione
- Filtri avanzati:
  - Sezione
  - Divisione
  - Livello del codice
  - Codici foglia
- Ordinamento personalizzabile
- Interfaccia user-friendly

## Requisiti

- Python 3.11 o superiore
- pip (gestore pacchetti Python)

## Installazione

1. Clona il repository:
```bash
git clone [URL_DEL_REPOSITORY]
cd [NOME_DIRECTORY]
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Avvia l'applicazione:
```bash
streamlit run main.py
```

L'applicazione sarà accessibile all'indirizzo `http://localhost:5000`

## Struttura del Database

L'applicazione utilizza un database SQLite per archiviare i codici ATECO. La struttura include:
- Codice ATECO
- Descrizione
- Sezione
- Divisione

## Utilizzo

1. Apri l'applicazione nel browser
2. Usa la barra di ricerca per cercare per codice o descrizione
3. Utilizza i filtri avanzati per una ricerca più precisa:
   - Seleziona la sezione di interesse
   - Filtra per divisione
   - Scegli il livello di dettaglio del codice
4. I risultati verranno mostrati in una tabella ordinabile

## Licenza

Questo progetto è distribuito con licenza MIT. Vedere il file `LICENSE` per i dettagli.
