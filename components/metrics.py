import streamlit as st

def display_metrics(df):
    """Affiche les métriques principales avec plus de détails"""
    # Calcul des métriques principales
    avg_clear_rate = df['clear_rate'].mean()
    avg_engagement_score = df['engagement_score'].mean()
    total_levels = len(df)
    avg_difficulty_score = df['difficulty_score'].mean() if 'difficulty_score' in df.columns else None

    # Calcul des autres métriques (si disponibles)
    difficulty_distribution = df['difficulty'].value_counts() if 'difficulty' in df.columns else None
    avg_likes = df['likes'].mean() if 'likes' in df.columns else None

    # Affichage des métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Taux de Réussite Moyen", f"{avg_clear_rate:.2f}%")
    with col2:
        st.metric("Score d'Engagement Moyen", f"{avg_engagement_score:.2f}")
    with col3:
        st.metric("Nombre Total de Niveaux", total_levels)
    with col4:
        if avg_difficulty_score:
            st.metric("Difficulté Moyenne", f"{avg_difficulty_score:.2f}")
    
    # Affichage des autres statistiques si disponibles
    if difficulty_distribution is not None:
        st.markdown("---")
        st.subheader("Distribution des Niveaux par Difficulté")
        st.write(difficulty_distribution)
        
    if avg_likes is not None:
        st.markdown("---")
        st.subheader("Moyenne des Likes")
        st.write(f"Le nombre moyen de likes par niveau est de {avg_likes:.2f}.")

    # Affichage de la distribution des niveaux de difficulté
    if 'difficulty' in df.columns:
        st.markdown("---")
        st.subheader("Distribution des Niveaux par Difficulté")
        st.bar_chart(difficulty_distribution)
