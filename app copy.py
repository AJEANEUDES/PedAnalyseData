import streamlit as st
from utils.data_loader import load_data
from components.filters import create_sidebar_filters
from components.charts import (
    create_difficulty_distribution,
    create_clear_rate_chart,
    create_engagement_chart,
    create_popularity_chart
)
from components.metrics import display_metrics

# Configuration de la page
st.set_page_config(
    page_title="Analyse de Jeux Platformer",
    page_icon="🎮",
    layout="wide"
)

# Titre principal
st.title("📊 Analyse de Données de Jeux Platformer")
st.markdown("---")

# Chargement des données
df = load_data(use_processed=True)

if df is not None:
    # Filtres
    selected_difficulty = create_sidebar_filters(df)
    
    # Application des filtres
    df_filtered = df[df["difficulty"] == selected_difficulty] if selected_difficulty != "Tous" else df.copy()
    
    # Layout en colonnes pour les graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution des Niveaux par Difficulté")
        st.plotly_chart(create_difficulty_distribution(df), use_container_width=True)
        
        st.subheader("Taux de Réussite vs Difficulté")
        st.plotly_chart(create_clear_rate_chart(df_filtered), use_container_width=True)
    
    with col2:
        st.subheader("Score d'Engagement vs Difficulté")
        st.plotly_chart(create_engagement_chart(df_filtered), use_container_width=True)
        
        st.subheader("Popularité vs Difficulté")
        st.plotly_chart(create_popularity_chart(df_filtered), use_container_width=True)
    
    # Statistiques détaillées
    st.markdown("---")
    st.header("Statistiques Détaillées")
    display_metrics(df_filtered)
    
    # Table des données
    st.markdown("---")
    st.header("Données Brutes")
    st.dataframe(
        df_filtered[["title", "difficulty", "clear_rate", "likes", "engagement_score"]],
        use_container_width=True
    )
else:
    st.error("Impossible de charger les données. Veuillez vérifier les URLs des données.")