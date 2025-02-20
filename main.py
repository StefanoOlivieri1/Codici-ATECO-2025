import streamlit as st
import pandas as pd
from data_manager import DataManager

# Configurazione della pagina
st.set_page_config(
    page_title="Ricerca Codici ATECO",
    page_icon="📊",
    layout="wide"
)

# Caricamento stile personalizzato
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inizializzazione del gestore dati
data_manager = DataManager()

# Titolo principale
st.title("📊 Ricerca Codici ATECO")
st.markdown("***Ricerca per codice o descrizione delle attività economiche***")

# Creazione delle colonne per i filtri di ricerca
col1, col2 = st.columns(2)

with col1:
    search_code = st.text_input(
        "Ricerca per Codice ATECO",
        placeholder="Es. 01.11"
    )

with col2:
    search_desc = st.text_input(
        "Ricerca per Descrizione",
        placeholder="Es. coltivazione cereali"
    )

# Esecuzione della ricerca
results = data_manager.search(
    code=search_code,
    description=search_desc
)

# Visualizzazione dei risultati
if results is not None and not results.empty:
    st.markdown("### Risultati della ricerca")
    
    # Aggiunta di filtri per le colonne
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        divisione_filter = st.multiselect(
            "Filtra per Divisione",
            options=sorted(results['Divisione'].unique())
        )
    
    with col_filter2:
        sezione_filter = st.multiselect(
            "Filtra per Sezione",
            options=sorted(results['Sezione'].unique())
        )

    # Applicazione dei filtri
    if divisione_filter:
        results = results[results['Divisione'].isin(divisione_filter)]
    if sezione_filter:
        results = results[results['Sezione'].isin(sezione_filter)]

    # Visualizzazione della tabella dei risultati
    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Codice": st.column_config.TextColumn("Codice ATECO", width="medium"),
            "Descrizione": st.column_config.TextColumn("Descrizione", width="large"),
            "Sezione": st.column_config.TextColumn("Sezione", width="medium"),
            "Divisione": st.column_config.TextColumn("Divisione", width="medium")
        }
    )
    
    # Mostra il numero di risultati
    st.info(f"Trovati {len(results)} risultati")

elif search_code or search_desc:
    st.warning("Nessun risultato trovato per i criteri di ricerca specificati.")

# Footer informativo
st.markdown("---")
st.markdown("""
    <div class='footer'>
        <p>Questa applicazione permette di cercare i codici ATECO 2007. 
        È possibile effettuare la ricerca sia per codice che per descrizione dell'attività.</p>
    </div>
    """, unsafe_allow_html=True)
