import os
import logging
from src.data_collection import DataCollector
from src.data_preprocessing import DataPreprocessor
from src.dataset_structure import DatasetBuilder
from src.analysis import DataAnalyzer

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('main.log'),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logging.info("Démarrage du pipeline d'analyse de la difficulté des jeux")
    
    try:
        # Initialize components
        collector = DataCollector()
        preprocessor = DataPreprocessor()
        dataset_builder = DatasetBuilder()
        analyzer = DataAnalyzer()
        
        # 1. Data Collection
        logging.info("Démarrage de la collecte de données à partir du référentiel PED...")
        raw_data = collector.collect_game_data(limit=200)
        logging.info(f"Recueil {len(raw_data['levels'])} des entrées de niveau")
        
        # 2. Data Preprocessing
        logging.info("Démarrage du prétraitement des données...")
        clean_data = preprocessor.process_data(raw_data)
        logging.info("Prétraitement des données terminé")
        
        # 3. Dataset Building
        logging.info("Construction d'un ensemble de données...")
        structured_dataset = dataset_builder.build_dataset(clean_data)
        logging.info("Jeu de données construit avec succès")
        
        # 4. Analysis and Visualization
        logging.info("Analyse de départ...")
        analysis_results = analyzer.analyze_difficulty_patterns(structured_dataset)
        
        # Print summary of results
        print("\nRésumé de l'analyse:")
        print("-" * 50)
        print(f"Niveaux totaux analysés: {analysis_results['performance_metrics']['total_levels']}")
        print(f"Taux d'achèvement moyen: {analysis_results['performance_metrics']['average_clear_rate']:.2f}%")
        print(f"Score d'engagement moyen: {analysis_results['performance_metrics']['average_engagement_score']:.2f}")
        print("\nRépartition des difficultés:")
        for diff, count in analysis_results['difficulty_distribution']['difficulty_distribution'].items():
            print(f"{diff}: {count} niveaux")
        
        logging.info("Le pipeline d'analyse s'est achevé avec succès")
        print("\nLe tableau de bord interactif s'ouvre dans votre navigateur...")
        
    except Exception as e:
        logging.error(f"Échec du pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()