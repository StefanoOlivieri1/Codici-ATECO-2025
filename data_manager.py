import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import or_
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
        if not code and not description:
            return None

        query = self._db.query(CodeAteco)

        if code:
            code = str(code).lower()
            query = query.filter(CodeAteco.codice.ilike(f"{code}%"))

        if description:
            description = description.lower()
            query = query.filter(CodeAteco.descrizione.ilike(f"%{description}%"))

        results = query.all()

        if not results:
            return pd.DataFrame()

        # Converti i risultati in DataFrame
        data = [{
            'Codice': r.codice,
            'Descrizione': r.descrizione,
            'Sezione': r.sezione,
            'Divisione': r.divisione
        } for r in results]

        return pd.DataFrame(data).sort_values('Codice')

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