import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from models import CodeAteco, get_db

class DataManager:
    def __init__(self):
        self._db = next(get_db())

    def search(self, code=None, description=None):
        """
        Cerca nei codici ATECO per codice o descrizione

        Args:
            code (str): Codice ATECO da cercare
            description (str): Descrizione da cercare

        Returns:
            pd.DataFrame: Risultati della ricerca
        """
        print(f"Ricerca con codice: {code}, descrizione: {description}")

        if not code and not description:
            return None

        query = self._db.query(CodeAteco)

        if code:
            code = str(code).strip()
            print(f"Cercando codice che inizia con: {code}")
            # Rimuovi eventuali spazi e rendi case-insensitive
            query = query.filter(func.lower(CodeAteco.codice).like(f"{code.lower()}%"))

        if description:
            description = description.strip()
            print(f"Cercando descrizione che contiene: {description}")
            # Rendi case-insensitive e cerca parole parziali
            query = query.filter(func.lower(CodeAteco.descrizione).like(f"%{description.lower()}%"))

        results = query.all()
        print(f"Trovati {len(results)} risultati")

        if not results:
            return pd.DataFrame()

        # Converti i risultati in DataFrame
        data = [{
            'Codice': r.codice,
            'Descrizione': r.descrizione,
            'Sezione': r.sezione,
            'Divisione': r.divisione
        } for r in results]

        df = pd.DataFrame(data)
        print("Colonne del DataFrame:", df.columns.tolist())
        print("Prime righe:", df.head())

        return df.sort_values('Codice')

    def import_from_csv(self, csv_path='data/codici_ateco.csv'):
        """
        Importa i dati dal CSV nel database
        """
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            code_ateco = CodeAteco(
                codice=row['Codice'],
                descrizione=row['Descrizione'],
                sezione=row['Sezione'],
                divisione=row['Divisione']
            )
            self._db.add(code_ateco)

        self._db.commit()