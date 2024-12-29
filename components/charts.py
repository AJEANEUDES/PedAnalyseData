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

# Ajout d'un graphique pour la distribution des scores de difficulté
def create_difficulty_score_distribution(df):
    """Crée un graphique pour la distribution des scores de difficulté"""
    return px.histogram(
        df,
        x="difficulty_score",
        nbins=20,
        title="Distribution des Scores de Difficulté",
        color="difficulty",
        color_discrete_sequence=px.colors.qualitative.Set1
    )

# Graphique pour la relation entre la difficulté et le taux de réussite
def create_clear_rate_vs_difficulty(df):
    """Crée un graphique de taux de réussite en fonction de la difficulté"""
    return px.scatter(
        df,
        x="difficulty_score",
        y="clear_rate",
        color="difficulty",
        title="Taux de Réussite vs Score de Difficulté",
        trendline="ols",
        labels={"difficulty_score": "Score de Difficulté", "clear_rate": "Taux de Réussite"}
    )

# Graphique pour la relation entre l'engagement et les likes
def create_engagement_vs_likes(df):
    """Crée un graphique de l'engagement par rapport aux likes"""
    return px.scatter(
        df,
        x="likes",
        y="engagement_score",
        color="difficulty",
        title="Score d'Engagement vs Likes",
        trendline="ols",
        labels={"likes": "Likes", "engagement_score": "Score d'Engagement"}
    )
