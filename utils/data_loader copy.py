import pandas as pd
import streamlit as st
import requests
import io

# URL pour télécharger un fichier spécifique depuis Google Drive (traitées)
def get_gdrive_download_url(file_id: str) -> str:
    """Génère l'URL de téléchargement direct pour un fichier Google Drive"""
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Liste des IDs des fichiers traités sur Google Drive
processed_file_ids = [
    "1-0mA5_98MGeEmWvnP0JYgUmhdMCVrrLg",
    "1-QN7Lv1Hab4KEtwTofkHptWGyp9IDlEi",
    "1-mIws4Jvb0Blf46FijFEBvxxbozZ18rU",
    "10p-JKoJo8ulYvaOUmiJmjYojZLOGk5tC",
    "11i-nZCWbkL-0_xa53W9wYZzt3qj1HZpb",
    "12246tr1mqIPeWfPOX7qPJLTnLlLZDelC",
    "13t7_OUhu4B226e9UsNwcD8ILoJtS8FPI",
    "16JNeMx5Pm6vQDJtmOcpwl9nlx9iijO7d",
    "19I0CynKZH4zL_Omh410foIHiCDL6QBbF",
    "19k78qA_3xB5TIhuCLcZ3gk4p3b6hnhpt",
    "1ALLdMh7pFCE3dj_bVJOJXuSgx-E28ZHu",
    "1BCFcgk_C4XT1_VX_MXh-DA3Uaq-nf99I",
    "1Bo3YY9TMmhYN5Bl3MZxgr2AIlAj_mYlL",
    "1FqncgnLmndW_ys21JIY86fUxWYLoq_ZZ",
    "1J9pDGVhL5huu5tQG4bivp7mTZhiLJkQk",
    "1JXaZzDKsIg_untCc1KbXiiC_Wg2eB6k3",
    "1JtyBnoqYLJ8q4WTwwGYu1NVb2hH8S0P0",
    "1KdPrIMgmB_7pvgEh_nYr1Nv_mgbp7lop",
    "1L8Faztgn_adFMP0kjW1HiK1LvF4F52Bv",
    "1Oxsmcy7dki2oH8wEX9PfUkRiOnSWvsJA",
    "1SpDnD0BE-FYaov88VenXFyVcHlSjA7DA",
    "1UYr410CerFiDA7e0Gk7zShqWeHFuPJG4",
    "1WXw6SSNqrqAqWFpgGco6PaVcXRy0ADPa",
    "1WeE0THvDXg6fUPVyClZ8XUgrKqlDSoMu",
    "1XldEAnJBH9lxj1t-ZpAGvIQ90VBvjQvc",
    "1ZW1xN4WZzMsJTpJ5qut0iU3CnXPbsUPn",
    "1_Jchk6Ucb2yU_QEoWO_ipDJ5gXQ79q1P",
    "1afIcua6hJCw2N1WpaCp1GWONaGgl-Vga",
    "1bBlsJiGH-cG0IKVOPck_brVxwj_h2JOX",
    "1blMfAVuBAbMO9n2GxXXk_HK_fTrXDgrt",
    "1cViSnC8ec3y2Gmik_CqsrlOAtbO6DpSp",
    "1dbOnjjmCQByO7NC8iqR6vUczKEm1c0_v",
    "1fIAs5wMI1nsir6XCMn7cTTi_D7bIUNUG",
    "1hADRNvi3gkL5NRBH-mVlzXD5CGI9-ENv",
    "1kKIvWbmbRJZMcKLbkY-uJER73d0a2w5O",
    "1p8fQ2bmgeLX7OV6bAktGxBVooUx0RyJP",
    "1ppWQyLZAwpeRq4iJYp0nA22ndiAyI0E2",
    "1r2moFRR17ulV7MYe8nUNVgLyBAUg5K0B",
    "1sLrsR8TUbY2yZ6PuS_eDBjJpHmG51Pze",
    "1u9InBqqKJZzFNejNRVozb8m_jTYcaSGe",
    "1v1PvdFXce8IyO5qSeZ1g2zI8HEv_cKrP",
    "1wCxppRk8sqCfTY7BxKzwFB2VIG40mTLT",
    "1wOxn7ch-FsAIEa7Ez3QlKxMVlRPGw309",
    "1wZiRHa-zNGnLHC5EwKs9s5-qIbbZ0A-B",
    "1xbjiSdiONe3vx5xUVzI4Zz_ND1nnGWNu",
    "1yy_04jL6ECXugazNxCP8AJmGdzwyOAC5",
    "1zV2qzQERzPgUU_UY-_FTUFVQwLLHuh3v"
]


# URL pour télécharger un fichier depuis GitHub (brutes)
def get_github_raw_url(repo_url: str, file_path: str) -> str:
    """Génère l'URL de téléchargement brut pour un fichier GitHub"""
    return f"https://raw.githubusercontent.com/{repo_url}/main/{file_path}"

@st.cache_data
def load_data(use_processed=True, file_index=0):
    """Charge les données depuis Google Drive ou GitHub"""
    try:
        # ID des fichiers Google Drive (traitées)
        if use_processed:
            file_id = processed_file_ids[file_index]  # Utiliser l'index pour choisir le fichier
            url = get_gdrive_download_url(file_id)
        else:
            # Fichier brut depuis GitHub
            raw_github_file_path = "chemin/vers/le/fichier.csv"  # Modifiez avec le chemin réel du fichier brut sur GitHub
            repo_url = "AJEANEUDES/PED"  # Repos GitHub
            url = get_github_raw_url(repo_url, raw_github_file_path)
        
        # Télécharger le fichier
        response = requests.get(url)
        
        # Afficher des informations pour déboguer
        st.write(f"Statut de la réponse : {response.status_code}")
        if response.status_code != 200:
            st.write(f"Réponse du serveur : {response.text}")
        
        response.raise_for_status()
        
        # Vérifier le contenu du fichier et afficher les 500 premiers caractères pour débogage
        st.write(response.text[:500])  # Affiche les premiers caractères du fichier pour inspecter son format
        
        # Lire le CSV depuis la réponse (spécifier un délimiteur si nécessaire et ignorer les lignes malformées)
        df = pd.read_csv(io.StringIO(response.text), delimiter=',', on_bad_lines='skip')  # Modifiez le délimiteur si nécessaire
        
        # Afficher les colonnes pour vérifier l'existence de la colonne 'difficulty'
        st.write("Colonnes dans le DataFrame :", df.columns)
        
        return df
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        return None
