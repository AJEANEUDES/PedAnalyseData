import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_collection import DataCollector
from src.data_preprocessing import DataPreprocessor
from src.dataset_structure import DatasetBuilder
from src.analysis import DataAnalyzer

st.set_page_config(page_title="Analyse de la Difficulté des Jeux", layout="wide")

def main():
    st.title("Analyse de la Difficulté des Jeux")
    
    # Sidebar pour les contrôles
    st.sidebar.header("Paramètres")
    limit = st.sidebar.slider("Nombre de niveaux à analyser", 10, 500, 100)
    
    # Collecte des données
    with st.spinner("Collecte des données en cours..."):
        collector = DataCollector()
        raw_data = collector.collect_game_data(limit=limit)
    
    # Prétraitement
    with st.spinner("Prétraitement des données..."):
        preprocessor = DataPreprocessor()
        clean_data = preprocessor.process_data(raw_data)
        
        dataset_builder = DatasetBuilder()
        df = dataset_builder.build_dataset(clean_data)
    
    # Affichage des métriques principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nombre total de niveaux", len(df))
    with col2:
        st.metric("Taux moyen de réussite", f"{df['clear_rate'].mean():.2f}%")
    with col3:
        st.metric("Score moyen d'engagement", f"{df['engagement_score'].mean():.2f}")
    with col4:
        st.metric("Difficulté moyenne", f"{df['difficulty_score'].mean():.2f}")
    
    # Visualisations
    st.header("Visualisations")
    
    # Distribution de la difficulté
    st.subheader("Distribution des Scores de Difficulté")
    fig_difficulty = px.histogram(
        df,
        x="difficulty_score",
        color="difficulty",
        title="Distribution des Scores de Difficulté"
    )
    st.plotly_chart(fig_difficulty, use_container_width=True)
    
    # Carte thermique des corrélations
    st.subheader("Carte Thermique des Corrélations")
    correlation_cols = ['difficulty_score', 'clear_rate', 'engagement_score', 
                       'popularity_score', 'completion_rate']
    correlation_matrix = df[correlation_cols].corr()
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=correlation_cols,
        y=correlation_cols,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        text=correlation_matrix.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False
    ))
    fig_heatmap.update_layout(
        title="Matrice de Corrélation des Métriques Principales",
        height=500
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Mesures par niveau de difficulté
    st.subheader("Mesures par Niveau de Difficulté")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Taux de réussite moyen par difficulté
        fig_clear_rate = px.box(
            df,
            x="difficulty",
            y="clear_rate",
            title="Taux de Réussite par Niveau de Difficulté",
            color="difficulty"
        )
        st.plotly_chart(fig_clear_rate, use_container_width=True)
    
    with col2:
        # Score d'engagement moyen par difficulté
        fig_engagement = px.box(
            df,
            x="difficulty",
            y="engagement_score",
            title="Score d'Engagement par Niveau de Difficulté",
            color="difficulty"
        )
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    with col3:
        fig_engagement_dificulty = px.scatter(
            df,
            x="difficulty_score",
            y="engagement_score",
            color="difficulty",
            title="Score d'engagement par rapport à la difficulté"
        )
        st.plotly_chart(fig_engagement_dificulty, use_container_width=True)
         
    # Statistiques détaillées par niveau de difficulté
    st.subheader("Statistiques Détaillées par Niveau de Difficulté")
    stats_by_difficulty = df.groupby('difficulty').agg({
        'clear_rate': ['mean', 'std'],
        'engagement_score': ['mean', 'std'],
        'completion_rate': ['mean', 'std'],
        'likes': ['mean', 'sum']
    }).round(2)
    
    stats_by_difficulty.columns = [
        'Taux de réussite (moy)', 'Taux de réussite (std)',
        'Engagement (moy)', 'Engagement (std)',
        'Complétion (moy)', 'Complétion (std)',
        'Likes (moy)', 'Likes (total)'
    ]
    st.dataframe(stats_by_difficulty, use_container_width=True)
    
    # Données brutes
    st.header("Données Brutes")
    st.dataframe(df)

if __name__ == "__main__":
    main()