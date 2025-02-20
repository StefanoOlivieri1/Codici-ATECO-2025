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
st.markdown("***Ricerca avanzata per codici e attività economiche***")

# Creazione delle colonne per i filtri di ricerca
col1, col2 = st.columns(2)

with col1:
    search_code = st.text_input(
        "Ricerca per Codice ATECO",
        placeholder="Es. 01.11"
    )

    # Aggiunta filtro per livello gerarchico
    code_level = st.select_slider(
        "Livello di dettaglio del codice",
        options=["Tutti", "Sezione", "Divisione", "Gruppo", "Classe", "Categoria", "Sottocategoria"],
        value="Tutti"
    )

with col2:
    search_desc = st.text_input(
        "Ricerca per Descrizione",
        placeholder="Es. coltivazione cereali"
    )

    # Aggiunta ordinamento
    sort_by = st.selectbox(
        "Ordina risultati per",
        options=["Codice", "Descrizione", "Sezione", "Divisione"],
        index=0
    )

# Filtri avanzati in un expander
with st.expander("Filtri Avanzati", expanded=False):
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        # Lista delle sezioni disponibili
        sezioni = data_manager.get_sezioni()
        selected_sezione = st.selectbox(
            "Filtra per Sezione",
            options=["Tutte"] + list(sezioni),
            key="sezione_filter"
        )

    with filter_col2:
        # Lista delle divisioni disponibili (aggiornata in base alla sezione selezionata)
        divisioni = data_manager.get_divisioni(sezione=selected_sezione if selected_sezione != "Tutte" else None)
        selected_divisione = st.selectbox(
            "Filtra per Divisione",
            options=["Tutte"] + list(divisioni),
            key="divisione_filter"
        )

    with filter_col3:
        # Opzione per mostrare solo i codici foglia (ultimo livello)
        show_leaf_only = st.checkbox("Mostra solo codici di ultimo livello", value=False)

# Esecuzione della ricerca con i filtri avanzati
results = data_manager.search(
    code=search_code,
    description=search_desc,
    sezione=selected_sezione if selected_sezione != "Tutte" else None,
    divisione=selected_divisione if selected_divisione != "Tutte" else None,
    code_level=code_level if code_level != "Tutti" else None,
    leaf_only=show_leaf_only
)

# Visualizzazione dei risultati
if results is not None and not results.empty:
    st.markdown("### Risultati della ricerca")

    # Ordinamento dei risultati
    results = results.sort_values(sort_by)

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
        <p>Utilizzare i filtri avanzati per una ricerca più precisa.</p>
    </div>
    """, unsafe_allow_html=True)