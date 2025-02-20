import pandas as pd
from models import init_db, CodeAteco, get_db
import os

def convert_and_import_excel():
    print("Inizializzazione del database...")
    init_db()
    db = next(get_db())

    print("Lettura del file Excel...")
    # Leggi il file Excel saltando le prime righe di intestazione
    df = pd.read_excel(
        'attached_assets/StrutturaATECO-2025-IT-EN-1.xlsx',
        skiprows=10  # Salta le prime 10 righe di intestazione
    )

    # Rinomina le colonne secondo il formato atteso
    df = df.rename(columns={
        'CODICE_ATECO_2025': 'Codice',
        'TITOLO_ITALIANO_ATECO_2025': 'Descrizione',
        'GERARCHIA_ATECO_2025': 'Livello'
    })

    # Pulizia del database esistente
    print("Pulizia del database esistente...")
    db.query(CodeAteco).delete()
    db.commit()

    print("Importazione dei nuovi dati...")
    for _, row in df.iterrows():
        try:
            codice = str(row['Codice']).strip()
            descrizione = str(row['Descrizione']).strip()

            # Estrai sezione e divisione dal codice
            sezione = codice[0] if len(codice) > 0 else ''
            divisione = codice.split('.')[0] if '.' in codice else codice[:2]

            if codice and descrizione:  # Verifica che i campi non siano vuoti
                code_ateco = CodeAteco(
                    codice=codice,
                    descrizione=descrizione,
                    sezione=sezione,
                    divisione=divisione
                )
                db.add(code_ateco)
        except Exception as e:
            print(f"Errore nell'importazione della riga {row}: {str(e)}")
            continue

    db.commit()
    print("Importazione completata!")

if __name__ == "__main__":
    convert_and_import_excel()