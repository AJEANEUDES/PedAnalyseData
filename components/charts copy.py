import plotly.express as px

def create_difficulty_distribution(df):
    """Crée le graphique de distribution des difficultés"""
    return px.pie(
        df,
        names="difficulty",
        title="Répartition des Niveaux par Difficulté",
        color_discrete_sequence=px.colors.qualitative.Set3
    )

def create_clear_rate_chart(df):
    """Crée le graphique de taux de réussite"""
    return px.box(
        df,
        x="difficulty",
        y="clear_rate",
        title="Distribution des Taux de Réussite par Difficulté",
        color="difficulty"
    )

def create_engagement_chart(df):
    """Crée le graphique d'engagement"""
    return px.scatter(
        df,
        x="difficulty_score",
        y="engagement_score",
        color="difficulty",
        title="Score d'Engagement en fonction de la Difficulté",
        trendline="ols"
    )

def create_popularity_chart(df):
    """Crée le graphique de popularité"""
    return px.violin(
        df,
        x="difficulty",
        y="likes",
        title="Distribution des Likes par Difficulté",
        color="difficulty"
    )