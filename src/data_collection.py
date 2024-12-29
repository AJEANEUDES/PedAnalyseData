import requests
import json
import time
from typing import Dict, List, Any
import logging
from pathlib import Path
import git
import os
import uuid
import pandas as pd  # Ajouté pour traiter les fichiers CSV ou JSON
import numpy as np

class DataCollector:
    def __init__(self):
        self.repo_url = "https://github.com/AJEANEUDES/PED.git"
        self.local_repo_path = Path("data/PED")
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self._setup_logging()
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_collection.log'),
                logging.StreamHandler()
            ]
        )
    
    def collect_game_data(self, limit: int = 100) -> Dict[str, List[Dict[str, Any]]]:
        """
        Collecte les données de jeu depuis le dépôt GitHub PED.
        Args:
            limit: Nombre maximum d'entrées à collecter
        Returns:
            Dictionnaire contenant les données collectées avec la clé 'levels'
        """
        try:
            logging.info(f"Clonage du dépôt depuis {self.repo_url}...")

            # Cloner ou mettre à jour le dépôt
            self._setup_repository()

            # Charger les données depuis le dépôt cloné
            levels_data = self._load_data_from_repo(limit)
            
            # Sauvegarder les données brutes
            collected_data = {"levels": levels_data}
            self._save_raw_data(collected_data)
            
            return collected_data
            
        except Exception as e:
            logging.error(f"Échec de la collecte des données : {str(e)}")
            return {"levels": []}
    
    def _setup_repository(self):
        """Clone ou met à jour le dépôt local"""
        if not self.local_repo_path.exists():
            git.Repo.clone_from(self.repo_url, self.local_repo_path)
            logging.info("Dépôt cloné avec succès")
        else:
            repo = git.Repo(self.local_repo_path)
            repo.remotes.origin.pull()  # Mettre à jour le dépôt
            logging.info("Dépôt mis à jour avec succès")
    
    def _load_data_from_repo(self, limit: int) -> List[Dict[str, Any]]:
        """Charge les données depuis les fichiers dans le dépôt cloné."""
        levels_data = []
        
        # Exemple de chemin vers un fichier CSV ou JSON dans le dépôt
        file_path = self.local_repo_path / "data" / "game_levels.csv"
        
        if file_path.exists():
            # Si le fichier est CSV
            df = pd.read_csv(file_path)
            levels_data = df.head(limit).to_dict(orient="records")  # Limite le nombre d'entrées
            
        else:
            logging.warning(f"Le fichier {file_path} n'a pas été trouvé dans le dépôt.")
        
        return levels_data
    
    def _save_raw_data(self, data: Dict[str, List[Dict[str, Any]]]):
        """Sauvegarde les données brutes dans un fichier JSON"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = self.data_dir / f"raw_data_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Données brutes sauvegardées dans {filepath}")

if __name__ == "__main__":
    collector = DataCollector()
    data = collector.collect_game_data()
    print(f"{len(data['levels'])} niveaux collectés")
