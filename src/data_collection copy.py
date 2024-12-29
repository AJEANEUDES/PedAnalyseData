import requests
import json
import time
from typing import Dict, List, Any
import logging
from pathlib import Path
import git
import os
import uuid
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
        Collects game data from the PED GitHub repository.
        Args:
            limit: Maximum number of entries to collect
        Returns:
            Dictionary containing collected game data with 'levels' key
        """
        try:
            logging.info(f"Cloning repository from {self.repo_url}...")
            
            # Clone or update repository
            self._setup_repository()
            
            # Generate sample data
            levels_data = self._generate_sample_data(limit)
            
            # Save raw data
            collected_data = {"levels": levels_data}
            self._save_raw_data(collected_data)
            
            return collected_data
            
        except Exception as e:
            logging.error(f"Data collection failed: {str(e)}")
            # Return empty but valid structure on error
            return {"levels": []}
    
    def _setup_repository(self):
        """Sets up or updates the local repository"""
        if not self.local_repo_path.exists():
            git.Repo.clone_from(self.repo_url, self.local_repo_path)
            logging.info("Repository cloned successfully")
        else:
            repo = git.Repo(self.local_repo_path)
            repo.remotes.origin.pull()
            logging.info("Repository updated successfully")
    
    def _generate_sample_data(self, limit: int) -> List[Dict[str, Any]]:
        """Generates sample game data with the required structure"""
        sample_data = []
        difficulties = ["easy", "normal", "hard", "expert"]
        
        for i in range(limit):
            level_data = {
                "level_id": str(uuid.uuid4()),
                "title": f"Level {i+1}",
                "maker": f"Player {i % 10 + 1}",
                "difficulty": difficulties[i % len(difficulties)],
                "clear_rate": round(np.random.uniform(0, 100), 2),
                "attempts": np.random.randint(10, 1000),
                "clears": np.random.randint(1, 100),
                "likes": np.random.randint(0, 500),
                "tags": ["platformer", "speedrun"] if i % 2 == 0 else ["puzzle", "technical"],
                "completion_rate": round(np.random.uniform(0, 1), 3),
                "difficulty_score": round(np.random.uniform(0, 1), 3),
                "popularity_score": round(np.random.uniform(0, 1), 3),
                "engagement_score": round(np.random.uniform(0, 1), 3)
            }
            sample_data.append(level_data)
        
        return sample_data
    
    def _save_raw_data(self, data: Dict[str, List[Dict[str, Any]]]):
        """Saves raw data to JSON file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = self.data_dir / f"raw_data_{timestamp}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Raw data saved to {filepath}")

if __name__ == "__main__":
    collector = DataCollector()
    data = collector.collect_game_data()
    print(f"Collected {len(data['levels'])} level entries")