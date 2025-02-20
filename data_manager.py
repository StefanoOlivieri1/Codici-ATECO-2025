import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, distinct
from models import CodeAteco, get_db

class DataManager:
    def __init__(self):
        self._db = next(get_db())

    def get_sezioni(self):
        """Ottiene la lista delle sezioni disponibili."""
        return [r[0] for r in self._db.query(distinct(CodeAteco.sezione))
                .order_by(CodeAteco.sezione).all()]

    def get_divisioni(self, sezione=None):
        """
        Ottiene la lista delle divisioni disponibili.
        Se viene specificata una sezione, restituisce solo le divisioni di quella sezione.
        """
        query = self._db.query(distinct(CodeAteco.divisione))
        if sezione:
            query = query.filter(CodeAteco.sezione == sezione)
        return [r[0] for r in query.order_by(CodeAteco.divisione).all()]

    def _get_code_level_filter(self, code_level):
        """Restituisce il filtro per il livello del codice."""
        if code_level == "Sezione":
            return CodeAteco.codice.regexp_match(r'^[A-Z]$')
        elif code_level == "Divisione":
            return CodeAteco.codice.regexp_match(r'^\d{2}$')
        elif code_level == "Gruppo":
            return CodeAteco.codice.regexp_match(r'^\d{2}\.\d{1}$')
        elif code_level == "Classe":
            return CodeAteco.codice.regexp_match(r'^\d{2}\.\d{2}$')
        elif code_level == "Categoria":
            return CodeAteco.codice.regexp_match(r'^\d{2}\.\d{2}\.\d{1}$')
        elif code_level == "Sottocategoria":
            return CodeAteco.codice.regexp_match(r'^\d{2}\.\d{2}\.\d{2}$')
        return None

    def search(self, code=None, description=None, sezione=None, divisione=None, 
              code_level=None, leaf_only=False):
        """
        Cerca nei codici ATECO con filtri avanzati

        Args:
            code (str): Codice ATECO da cercare
            description (str): Descrizione da cercare
            sezione (str): Filtra per sezione specifica
            divisione (str): Filtra per divisione specifica
            code_level (str): Filtra per livello del codice
            leaf_only (bool): Se True, mostra solo i codici di ultimo livello

        Returns:
            pd.DataFrame: Risultati della ricerca
        """
        print(f"Ricerca avanzata con parametri:")
        print(f"- Codice: {code}")
        print(f"- Descrizione: {description}")
        print(f"- Sezione: {sezione}")
        print(f"- Divisione: {divisione}")
        print(f"- Livello codice: {code_level}")
        print(f"- Solo foglie: {leaf_only}")

        if not any([code, description, sezione, divisione, code_level, leaf_only]):
            return None

        query = self._db.query(CodeAteco)

        # Filtro per codice
        if code:
            code = str(code).strip()
            print(f"Cercando codice che inizia con: {code}")
            query = query.filter(func.lower(CodeAteco.codice).like(f"{code.lower()}%"))

        # Filtro per descrizione
        if description:
            description = description.strip()
            print(f"Cercando descrizione che contiene: {description}")
            query = query.filter(func.lower(CodeAteco.descrizione).like(f"%{description.lower()}%"))

        # Filtro per sezione
        if sezione:
            query = query.filter(CodeAteco.sezione == sezione)

        # Filtro per divisione
        if divisione:
            query = query.filter(CodeAteco.divisione == divisione)

        # Filtro per livello del codice
        if code_level:
            level_filter = self._get_code_level_filter(code_level)
            if level_filter is not None:
                query = query.filter(level_filter)

        # Filtro per codici foglia
        if leaf_only:
            query = query.filter(CodeAteco.codice.regexp_match(r'^\d{2}\.\d{2}\.\d{2}$'))

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

        return df

    def import_from_csv(self, csv_path='data/codici_ateco.csv'):
        """Importa i dati dal CSV nel database"""
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