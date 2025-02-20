import pandas as pd
import numpy as np

class DataManager:
    def __init__(self):
        self.df = pd.read_csv('data/codici_ateco.csv')
        
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
            
        results = self.df.copy()
        
        if code:
            code = str(code).lower()
            results = results[results['Codice'].str.lower().str.startswith(code)]
            
        if description:
            description = description.lower()
            results = results[results['Descrizione'].str.lower().str.contains(description, na=False)]
            
        return results.sort_values('Codice')
