import pandas as pd
import numpy as np
from typing import Dict, List, Any
import logging

class DataPreprocessor:
    def __init__(self):
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
            
            for level in raw_data.get("levels", []):
                if self._validate_level_data(level):
                    cleaned_level = self._process_level(level)
                    cleaned_data.append(cleaned_level)
            
            return {"levels": cleaned_data}
            
        except Exception as e:
            logging.error(f"Échec de la structuration du jeu de données: {str(e)}")
            raise Exception(f"Échec de la structuration du jeu de données: {str(e)}")
    
    def _validate_level_data(self, level: Dict[str, Any]) -> bool:
        """Validates level data"""
        required_fields = [
            "level_id", "title", "maker", "difficulty", "clear_rate", 
            "attempts", "clears", "likes", "tags", "completion_rate",
            "difficulty_score", "popularity_score", "engagement_score"
        ]
        return all(key in level for key in required_fields)
    
    def _process_level(self, level: Dict[str, Any]) -> Dict[str, Any]:
        """Traite un seul niveau, en s'assurant que tous les champs obligatoires sont présents et valides."""
        processed = {
            "level_id": level["level_id"],
            "title": level["title"],
            "maker": level["maker"],
            "difficulty": level["difficulty"].lower(),
            "clear_rate": float(level["clear_rate"]),
            "attempts": int(level["attempts"]),
            "clears": int(level["clears"]),
            "likes": int(level["likes"]),
            "tags": level["tags"],
            "completion_rate": float(level["completion_rate"]),
            "difficulty_score": float(level["difficulty_score"]),
            "popularity_score": float(level["popularity_score"]),
            "engagement_score": float(level["engagement_score"])
        }
        
        return processed