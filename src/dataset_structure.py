import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
import logging

class DatasetBuilder:
    def __init__(self):
        """Initialisation de la classe DatasetBuilder avec la liste des colonnes attendues."""
        self.columns = [
            "level_id", "difficulty", "clear_rate", "attempts", "clears",
            "likes", "title", "maker", "tags", "difficulty_score",
            "popularity_score", "engagement_score", "completion_rate"
        ]
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)  # Crée le répertoire 'data' si nécessaire
        self._setup_logging()  # Configuration des logs

    def _setup_logging(self):
        """Configure les paramètres de journalisation."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('dataset.log'),
                logging.StreamHandler()
            ]
        )

    def build_dataset(self, cleaned_data: Dict[str, List[Dict[str, Any]]]) -> pd.DataFrame:
        """
        Structure les données nettoyées dans un DataFrame pandas.
        
        Args:
            cleaned_data : Dictionnaire contenant les données nettoyées (niveau).
            
        Returns:
            pd.DataFrame : Le DataFrame structuré.
        """
        try:
            # Conversion des données en DataFrame
            df = pd.DataFrame(cleaned_data.get("levels", []))
            
            # Vérification des colonnes manquantes et ajout avec des valeurs par défaut
            self._add_missing_columns(df)
            
            # Ajout des métadonnées (timestamp, version)
            self._add_metadata(df)
            
            # Traitement des tags (si présents)
            self._process_tags(df)
            
            # Sauvegarde du dataset
            self._save_dataset(df)
            
            return df
        
        except Exception as e:
            logging.error(f"Échec de la structuration du jeu de données: {str(e)}")
            raise Exception(f"Échec de la structuration du jeu de données: {str(e)}")

    def _add_missing_columns(self, df: pd.DataFrame):
        """Ajoute les colonnes manquantes avec une valeur par défaut (NaN)."""
        for col in self.columns:
            if col not in df.columns:
                logging.warning(f"Colonne manquante détectée : {col}. Ajout avec une valeur par défaut.")
                df[col] = np.nan  # Valeur par défaut pour les colonnes manquantes

    def _add_metadata(self, df: pd.DataFrame):
        """Ajoute des métadonnées telles que le timestamp et la version des données."""
        df["timestamp"] = pd.Timestamp.now()
        df["data_version"] = "1.0"

    def _process_tags(self, df: pd.DataFrame):
        """Convertit les tags de liste en chaîne de caractères séparée par des virgules."""
        if "tags" in df.columns:
            df["tags"] = df["tags"].apply(lambda x: ",".join(x) if isinstance(x, list) else "")
        else:
            df["tags"] = ""  # Si "tags" n'existe pas, on l'initialise à une chaîne vide.

    def _save_dataset(self, df: pd.DataFrame):
        """Enregistre le dataset dans des fichiers CSV et Pickle."""
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        
        # Sauvegarde en format CSV
        csv_path = self.data_dir / f"dataset_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        logging.info(f"Ensemble de données sauvegardé dans {csv_path}")
        
        # Sauvegarde en format Pickle pour préserver les types de données
        pickle_path = self.data_dir / f"dataset_{timestamp}.pkl"
        df.to_pickle(pickle_path)
        logging.info(f"Ensemble de données sauvegardé dans {pickle_path}")
