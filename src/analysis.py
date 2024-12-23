import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc
from pathlib import Path
import logging
from typing import Dict, Any
import webbrowser
from threading import Timer

class DataAnalyzer:
    def __init__(self):
        self.difficulty_thresholds = {
            "easy": 0.2,
            "medium": 0.4,
            "hard": 0.6,
            "very_hard": 0.8
        }
        self.output_dir = Path("analysis_output")
        self.output_dir.mkdir(exist_ok=True)
        self._setup_logging()
        self.app = Dash(__name__)
    
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('analysis.log'),
                logging.StreamHandler()
            ]
        )
    
    def analyze_difficulty_patterns(self, dataset: pd.DataFrame) -> Dict[str, Any]:
        """
        Effectue une analyse complète des schémas de difficultés et lance un tableau de bord interactif.
        """
        try:
            analysis_results = {
                "difficulty_distribution": self._analyze_difficulty_distribution(dataset),
                "performance_metrics": self._calculate_performance_metrics(dataset),
                "player_patterns": self._analyze_player_patterns(dataset),
                "correlations": self._analyze_correlations(dataset)
            }
            
            # Create and launch interactive dashboard
            self._create_dashboard(dataset, analysis_results)
            
            return analysis_results
            
        except Exception as e:
            logging.error(f"L'analyse a échoué: {str(e)}")
            raise
    
    def _analyze_difficulty_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "mean_difficulty": df["difficulty_score"].mean(),
            "median_difficulty": df["difficulty_score"].median(),
            "difficulty_std": df["difficulty_score"].std(),
            "difficulty_percentiles": df["difficulty_score"].quantile([0.25, 0.5, 0.75]).to_dict(),
            "difficulty_distribution": df["difficulty"].value_counts().to_dict()
        }
    
    def _calculate_performance_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "average_clear_rate": df["clear_rate"].mean(),
            "median_attempts": df["attempts"].median(),
            "total_levels": len(df),
            "difficulty_correlation": df["clear_rate"].corr(df["difficulty_score"]),
            "average_completion_rate": df["completion_rate"].mean(),
            "average_engagement_score": df["engagement_score"].mean()
        }
    
    def _analyze_player_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "likes_vs_difficulty": df["likes"].corr(df["difficulty_score"]),
            "attempts_vs_clears_ratio": (df["attempts"] / df["clears"]).mean(),
            "popularity_metrics": {
                "most_liked_difficulty": df.groupby("difficulty")["likes"].mean().idxmax(),
                "most_attempted_difficulty": df.groupby("difficulty")["attempts"].mean().idxmax(),
                "most_engaging_difficulty": df.groupby("difficulty")["engagement_score"].mean().idxmax()
            }
        }
    
    def _analyze_correlations(self, df: pd.DataFrame) -> Dict[str, float]:
        metrics = ["difficulty_score", "popularity_score", "engagement_score", "completion_rate"]
        corr_matrix = df[metrics].corr()
        
        correlations = {}
        for i in range(len(metrics)):
            for j in range(i + 1, len(metrics)):
                key = f"{metrics[i]}_vs_{metrics[j]}"
                correlations[key] = corr_matrix.iloc[i, j]
        
        return correlations
    
    def _create_dashboard(self, df: pd.DataFrame, analysis_results: Dict[str, Any]):
        """Création et lancement d'un tableau de bord interactif avec Plotly/Dash"""
        
        # Create figures
        fig_difficulty_dist = px.histogram(
            df, 
            x="difficulty_score",
            color="difficulty",
            title="Distribution des notes de difficulté"
        )
        
        fig_correlation = px.imshow(
            df[["difficulty_score", "popularity_score", "engagement_score", "completion_rate"]].corr(),
            title="Carte thermique des corrélations"
        )
        
        fig_metrics = px.box(
            df,
            x="difficulty",
            y=["clear_rate", "completion_rate", "engagement_score"],
            title="Mesures par niveau de difficulté"
        )
        
        fig_engagement = px.scatter(
            df,
            x="difficulty_score",
            y="engagement_score",
            color="difficulty",
            title="Score d'engagement par rapport à la difficulté"
        )
        
        # Create dashboard layout
        self.app.layout = html.Div([
            html.H1("Tableau de bord d'analyse de la difficulté des jeux"),
            
            html.Div([
                html.H2("Principaux indicateurs"),
                html.Ul([
                    html.Li(f"Niveaux totaux: {analysis_results['performance_metrics']['total_levels']}"),
                    html.Li(f"Taux d'effacement moyen: {analysis_results['performance_metrics']['average_clear_rate']:.2f}%"),
                    html.Li(f"Score d'engagement moyen: {analysis_results['performance_metrics']['average_engagement_score']:.2f}")
                ])
            ]),
            
            html.Div([
                dcc.Graph(figure=fig_difficulty_dist),
                dcc.Graph(figure=fig_correlation),
                dcc.Graph(figure=fig_metrics),
                dcc.Graph(figure=fig_engagement)
            ])
        ])
        
        # Open browser and run dashboard
        Timer(1, lambda: webbrowser.open('http://127.0.0.1:8050/')).start()
        self.app.run_server(debug=False)

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    # Test with sample data if needed