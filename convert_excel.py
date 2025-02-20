import pandas as pd
from models import init_db, CodeAteco, get_db
import os

def convert_and_import_excel():
    print("Inizializzazione del database...")
    init_db()
    db = next(get_db())

    print("Lettura del file Excel...")
    df = pd.read_excel(
        'attached_assets/StrutturaATECO-2025-IT-EN-1.xlsx',
        sheet_name="ATECO 2025 Struttura"
    )

    print("Struttura del DataFrame:")
    print(df.columns.tolist())
    print("\nPrime righe:")
    print(df.head())

    # Rinomina le colonne secondo il formato atteso
    df = df.rename(columns={
        'CODICE_ATECO_2025': 'Codice',
        'TITOLO_ITALIANO_ATECO_2025': 'Descrizione'
    })

    # Pulizia del database esistente
    print("Pulizia del database esistente...")
    db.query(CodeAteco).delete()
    db.commit()

    # Funzione per estrarre la sezione dal codice
    def get_section(code):
        if pd.isna(code):
            return ''
        code = str(code).strip()
        if len(code) == 1:  # È una sezione
            return code
        # Se il codice inizia con un numero, cerca l'ultima sezione vista
        return current_section

    # Funzione per estrarre la divisione dal codice
    def get_division(code):
        if pd.isna(code):
            return ''
        code = str(code).strip()
        if code.isalpha():  # È una sezione
            return code
        parts = code.split('.')
        if len(parts) > 0 and parts[0].isdigit():
            return parts[0].zfill(2)  # Assicura che la divisione sia sempre di 2 cifre
        return ''

    print("Importazione dei nuovi dati...")
    current_section = ''
    for _, row in df.iterrows():
        try:
            if pd.isna(row['Codice']) or pd.isna(row['Descrizione']):
                continue

            codice = str(row['Codice']).strip()
            descrizione = str(row['Descrizione']).strip()

            if not codice or not descrizione:
                continue

            # Aggiorna la sezione corrente se il codice è una lettera
            if codice.isalpha() and len(codice) == 1:
                current_section = codice

            sezione = get_section(codice)
            divisione = get_division(codice)

            code_ateco = CodeAteco(
                codice=codice,
                descrizione=descrizione,
                sezione=current_section,
                divisione=divisione
            )
            db.add(code_ateco)
            print(f"Aggiunto codice: {codice} (Sezione: {current_section}, Divisione: {divisione})")
        except Exception as e:
            print(f"Errore nell'importazione della riga {row}: {str(e)}")
            continue

    db.commit()
    print("Importazione completata!")

if __name__ == "__main__":
    convert_and_import_excel()