import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
import logging

class DatasetBuilder:
    def __init__(self):
        self.columns = [
            "level_id", "difficulty", "clear_rate", "attempts", "clears",
            "likes", "title", "maker", "tags", "difficulty_score",
            "popularity_score", "engagement_score", "completion_rate"
        ]
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self._setup_logging()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('dataset.log'),
                logging.StreamHandler()
            ]
        )
    
    # def build_dataset(self, cleaned_data: Dict[str, List[Dict[str, Any]]]) -> pd.DataFrame:
    #     """
    #     Structure les données nettoyées dans un DataFrame pandas.
    #     Args:
    #         cleaned_data : Dictionnaire contenant les données de niveau nettoyées
    #     Returns:
    #         pandas DataFrame avec des données de jeu structurées
    #     """
    #     try:
    #         # Convert to DataFrame
    #         df = pd.DataFrame(cleaned_data["levels"])
            
    #         # Ensure all required columns are present
    #         missing_cols = set(self.columns) - set(df.columns)
    #         if missing_cols:
    #             raise ValueError(f"Missing required columns: {missing_cols}")
            
    #         # Add metadata
    #         df["timestamp"] = pd.Timestamp.now()
    #         df["data_version"] = "1.0"
            
    #         # Convert tags list to string for easier storage
    #         df["tags"] = df["tags"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)
            
    #         # Save processed dataset
    #         self._save_dataset(df)
            
    #         return df
            
    #     except Exception as e:
    #         logging.error(f"Échec de la structuration du jeu de données: {str(e)}")
    #         raise Exception(f"Échec de la structuration du jeu de données: {str(e)}")

    def build_dataset(self, cleaned_data: Dict[str, List[Dict[str, Any]]]) -> pd.DataFrame:
    """
    Structure les données nettoyées dans un DataFrame pandas.
    """
    try:
        # Convert to DataFrame
        df = pd.DataFrame(cleaned_data.get("levels", []))
        
        # Add missing columns with default values
        for col in self.columns:
            if col not in df.columns:
                logging.warning(f"Colonne manquante détectée : {col}. Ajout avec une valeur par défaut.")
                df[col] = np.nan  # Ou une valeur par défaut
        
        # Add metadata
        df["timestamp"] = pd.Timestamp.now()
        df["data_version"] = "1.0"
        
        # Convert tags list to string
        if "tags" in df.columns:
            df["tags"] = df["tags"].apply(lambda x: ",".join(x) if isinstance(x, list) else "")
        else:
            df["tags"] = ""
        
        # Save processed dataset
        self._save_dataset(df)
        
        return df
        
    except Exception as e:
        logging.error(f"Échec de la structuration du jeu de données: {str(e)}")
        raise Exception(f"Échec de la structuration du jeu de données: {str(e)}")

    
    
    def _save_dataset(self, df: pd.DataFrame):
        """Enregistre le jeu de données aux formats CSV et Pickle"""
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as CSV
        csv_path = self.data_dir / f"dataset_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        logging.info(f"Ensemble de données sauvegardé dans {csv_path}")
        
        # Save as pickle for preserving data types
        pickle_path = self.data_dir / f"dataset_{timestamp}.pkl"
        df.to_pickle(pickle_path)
        logging.info(f"Ensemble de données sauvegardé dans {pickle_path}")
