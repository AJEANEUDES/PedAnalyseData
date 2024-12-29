import streamlit as st

def create_sidebar_filters(df):
    """Crée les filtres dans la barre latérale"""
    st.sidebar.header("Filtres")
    
    difficulties = ["Tous"] + sorted(df["difficulty"].unique().tolist())
    selected_difficulty = st.sidebar.selectbox("Sélectionner la difficulté", difficulties)
    
    return selected_difficulty