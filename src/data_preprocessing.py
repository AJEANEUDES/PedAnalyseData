import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

class DataPreprocessor:
    def __init__(self):
        # Liste des difficultés valides
        self.valid_difficulties = ["easy", "normal", "hard", "expert"]
        self._setup_logging()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('preprocessing.log'),
                logging.StreamHandler()
            ]
        )
    
    def process_data(self, raw_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Nettoie et traite les données brutes du jeu.
    Args:
        raw_data : Dictionnaire contenant les données de niveau brut
    Returns:
        Dictionnaire contenant les données nettoyées et enrichies
    """
    try:
        cleaned_data = []

        # Vérifier si toutes les colonnes nécessaires sont présentes dans les données brutes
        expected_columns = [
            "level_id", "title", "maker", "difficulty", "clear_rate", 
            "attempts", "clears", "likes", "tags", "completion_rate",
            "difficulty_score", "popularity_score", "engagement_score"
        ]
        
        for level in raw_data.get("levels", []):
            missing_columns = [col for col in expected_columns if col not in level]
            
            if missing_columns:
                logging.warning(f"Colonnes manquantes pour le niveau {level.get('level_id', 'inconnu')}: {', '.join(missing_columns)}")
                for col in missing_columns:
                    level[col] = None  # Ou toute autre valeur par défaut, comme une chaîne vide ou 0
            else:
                cleaned_level = self._process_level(level)
                cleaned_data.append(cleaned_level)

        return {"levels": cleaned_data}
        
    except Exception as e:
        logging.error(f"Échec du prétraitement des données : {str(e)}")
        raise Exception(f"Échec du prétraitement des données : {str(e)}")

    
    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Valide les données, en s'assurant qu'elles contiennent les colonnes nécessaires."""
        required_columns = [
            "level_id", "title", "maker", "difficulty", "clear_rate", 
            "attempts", "clears", "likes", "tags", "completion_rate",
            "difficulty_score", "popularity_score", "engagement_score"
        ]
        
        # Vérification des colonnes requises
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colonnes manquantes : {', '.join(missing_columns)}")
        
        # Filtrage des niveaux avec des données invalides
        df = df.dropna(subset=required_columns)
        
        # Vérification des valeurs de difficulté
        df["difficulty"] = df["difficulty"].apply(lambda x: x.lower() if isinstance(x, str) else x)
        df = df[df["difficulty"].isin(self.valid_difficulties)]
        
        return df
    
    def _process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Traite les données brutes : conversion des types et calculs supplémentaires."""
        # Conversion des colonnes nécessaires en type approprié
        df["clear_rate"] = pd.to_numeric(df["clear_rate"], errors="coerce")
        df["attempts"] = pd.to_numeric(df["attempts"], errors="coerce")
        df["clears"] = pd.to_numeric(df["clears"], errors="coerce")
        df["likes"] = pd.to_numeric(df["likes"], errors="coerce")
        df["completion_rate"] = pd.to_numeric(df["completion_rate"], errors="coerce")
        df["difficulty_score"] = pd.to_numeric(df["difficulty_score"], errors="coerce")
        df["popularity_score"] = pd.to_numeric(df["popularity_score"], errors="coerce")
        df["engagement_score"] = pd.to_numeric(df["engagement_score"], errors="coerce")
        
        # Calcul du taux de réussite (clear_rate) comme ratio de clears / attempts
        df["calculated_clear_rate"] = df["clears"] / df["attempts"] * 100
        
        # Vérification et correction des taux de réussite calculés
        df["clear_rate"] = df["clear_rate"].fillna(df["calculated_clear_rate"])
        
        # Normalisation de certaines métriques pour qu'elles soient sur une échelle de 0 à 1
        df["difficulty_score"] = df["difficulty_score"].clip(0, 1)
        df["engagement_score"] = df["engagement_score"].clip(0, 1)
        df["popularity_score"] = df["popularity_score"].clip(0, 1)
        df["completion_rate"] = df["completion_rate"].clip(0, 1)
        
        # Ajustement des valeurs qui pourraient être incohérentes
        df["likes"] = df["likes"].fillna(0).astype(int)
        
        return df

if __name__ == "__main__":
    # Exemple de test du prétraitement
    from src.data_collection import DataCollector
    collector = DataCollector()
    raw_data = collector.collect_game_data(limit=100)
    
    preprocessor = DataPreprocessor()
    clean_data = preprocessor.process_data(raw_data)
    print(clean_data.head())
