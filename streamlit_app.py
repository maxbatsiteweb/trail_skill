import streamlit as st
from streamlit_echarts import st_echarts  # Pour le donut
import pandas as pd
import plotly.graph_objects as go

st.set_option('server.headless', True)  # Assurez-vous que l'application est en mode headless (utile en cloud)
st.set_option('server.enableCORS', False)  # Si vous avez des problèmes avec les CORS


st.image("logo_esc.png", width=150)

# CSS personnalisé
st.markdown(
    """
    <style>


    /* Masquer complètement le bandeau si nécessaire */
    header {
        visibility: hidden;
    }
    header > div {
        display: none;
    }



    /* Personnaliser les autres éléments si nécessaire */
    /* Applique le style pour centrer le texte globalement */
        .center-text {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            text-align: center;
            font-size: 20px;
        }

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
   

    </style>
    """,
    unsafe_allow_html=True
)

# Création de la jauge avec Plotly
def create_gauge(value):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            gauge={
                "axis": {"range": [0, 100]},  # Plage des valeurs de la jauge
                "bar": {"color": "#04A484"},     # Couleur de l'aiguille
                "threshold": {
                    "line": {"color": "lightgray", "width": 4},
                    "thickness": 0.75,
                    "value": value,
                },
                "axis_ticks":"",
                "axis_showticklabels": False
            },
        )
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),  # Réduire les marges en haut, bas, gauche et droite
        height=150,  # Réduire la hauteur de la jauge (ajuster selon besoin)
        width=150,   # Réduire la largeur de la jauge (ajuster selon besoin)
)
    return fig


# 1️⃣ Premier panneau : Titre
st.title("Trail skill by ESC") 

# Séparation visuelle
st.divider()

# 2️⃣ Second panneau : Filtres avec liste déroulante (2 colonnes)
st.header("Retrouve tes résultats")

# Colonnes pour les filtres
col1, col2 = st.columns(2)

df = pd.read_csv('segment_esc.csv')

athletes = df["Athlete"].unique()
zones = []
dates = []
parcours = []

# Initialisation des choix
selected_filter1 = None
selected_filter2 = None
selected_filter3 = None
selected_filter4 = None


# Filtre 1 : Athlete
selected_filter1 = col1.selectbox("Athlete", ["-- Sélectionnez --"] + list(athletes))

# Filtre 2 : Zone - Coach (apparaît uniquement après choix d'un Athlete)
if selected_filter1 and selected_filter1 != "-- Sélectionnez --":
    zones = df[df["Athlete"] == selected_filter1]["Zone"].unique()
    selected_filter2 = col1.selectbox("Zone - Coach", ["-- Sélectionnez --"] + list(zones))

# Filtre 3 : Date (apparaît uniquement après choix de la zone-coach)
if selected_filter2 and selected_filter2 != "-- Sélectionnez --":
    dates = df[
        (df["Athlete"] == selected_filter1) & (df["Zone"] == selected_filter2)
    ]["Date"].unique()
    selected_filter3 = col2.selectbox("Date", ["-- Sélectionnez --"] + list(dates))

# Filtre 4 : Parcours (apparaît uniquement après choix de la date)
if selected_filter3 and selected_filter3 != "-- Sélectionnez --":
    parcours = df[
        (df["Athlete"] == selected_filter1) &
        (df["Zone"] == selected_filter2) &
        (df["Date"] == selected_filter3)
    ]["Parcours"].unique()
    selected_filter4 = col2.selectbox("Parcours", ["-- Sélectionnez --"] + list(parcours))




# Si tous les filtres sont sélectionnés, on récupère le score
if selected_filter4 is not None and selected_filter4 != "-- Sélectionnez --":

    # Séparation visuelle
    st.divider()

    # Colonnes pour le score et le picto
    score_col, picto_col = st.columns([2, 1])

    # 4️⃣ Quatrième panneau : Donut + Picto montagne
    score_col.header(f"Ton Score Coureur")
    picto_col.header(f"Ton Profil")

    # Filtrer le DataFrame en fonction des filtres sélectionnés
    filtered_row = df[
        (df["Athlete"] == selected_filter1) &
        (df["Zone"] == selected_filter2) &
        (df["Date"] == selected_filter3) &
        (df["Parcours"] == selected_filter4)
    ]

    # Si une ligne est trouvée, on récupère le score
    if not filtered_row.empty:
        selected_score = filtered_row["Score"].values[0]
        score_col.plotly_chart(create_gauge(selected_score), use_container_width=True, key="gauge_generale")

        # Récupérer les temps pour chaque typologie
        score_montee = filtered_row["Score_montee"].values[0]
        score_descente = filtered_row["Score_descente"].values[0]
        score_plat = filtered_row["Score_plat"].values[0]

        best_score = max(score_montee, score_descente, score_plat)
        profile = ""

        if best_score == score_montee:
            profile = "Grimpeur"
        elif best_score == score_descente:
            if profile != "":
                profile = "Descendeur" + "/" + profile
            else:
                profile = "Descendeur"
        else:
            if profile != "":
                profile = "Coureur" + "/" + profile
            else:
                profile = "Coureur"

        picto_col.markdown(f"<h3 style='color: #04A484;'>{profile}</h2>", unsafe_allow_html=True)
        picto_col.markdown("<p style='font-size: 13px;'>Parmi grimpeur, descendeur et coureur<p>", unsafe_allow_html=True)





        # Séparation visuelle
        st.divider()

        # 5️⃣ Cinquième panneau : 3 colonnes avec pictos + texte
        st.header("Ton score par segment")

        # Colonnes pour les pictos
        col_montee, space, col_descente, space, col_plat = st.columns([3, 0.5, 3, 0.5, 3])



        # Texte sous chaque picto
        with col_montee:

            st.subheader("Montée :mountain:")

            st.plotly_chart(create_gauge(score_montee), use_container_width=True, key="gauge_montee")

            col_pace, col_vap = st.columns([5, 5])

            col_pace.markdown(f'<div class="center-text">Allure</div>', unsafe_allow_html=True)
            col_pace.markdown(f'<div class="center-text" style="color: #04A484;">{filtered_row["allure_montee"].values[0]}</div>', unsafe_allow_html=True)

            col_vap.markdown(f'<div class="center-text">VAP</div>', unsafe_allow_html=True)
            col_vap.markdown(f'<div class="center-text" style="color: #04A484;">{filtered_row["vap_montee"].values[0]}</div>', unsafe_allow_html=True)


        with col_descente:
            
            st.subheader("Descente :mountain:")

            st.plotly_chart(create_gauge(score_descente), use_container_width=True, key="gauge_descente")

            col_pace, col_vap = st.columns([5, 5])

            col_pace.markdown(f'<div class="center-text">Allure</div>', unsafe_allow_html=True)
            col_pace.markdown(f'<div class="center-text" style="color: #04A484;">{filtered_row["allure_descente"].values[0]}</div>', unsafe_allow_html=True)

            col_vap.markdown(f'<div class="center-text">VAP</div>', unsafe_allow_html=True)
            col_vap.markdown(f'<div class="center-text" style="color: #04A484;">{filtered_row["vap_descente"].values[0]}</div>', unsafe_allow_html=True)

        with col_plat:
            
            st.subheader("Plat :woman-running: :man-running:")

            st.plotly_chart(create_gauge(score_plat), use_container_width=True, key="gauge_plat")

            col_pace, col_vap = st.columns([5, 5])

            col_pace.markdown(f'<div class="center-text">Allure</div>', unsafe_allow_html=True)
            col_pace.markdown(f'<div class="center-text" style="color: #04A484;">{filtered_row["allure_plat"].values[0]}</div>', unsafe_allow_html=True)

            col_vap.markdown(f'<div class="center-text">VAP</div>', unsafe_allow_html=True)
            col_vap.markdown(f'<div class="center-text" style="color: #04A484;">{filtered_row["vap_plat"].values[0]}</div>', unsafe_allow_html=True)


        st.divider()

        st.header("Ton profil parmi les traileuses et traileurs")

        st.markdown("<br>", unsafe_allow_html=True)


        col_radar, = st.columns([1])
        
        #radar charts
        
        option = {
        "legend": {"data":  ["Ton profil","Moyenne des coureurs", "Athlète Elite Hugo Deck"],
                    "textStyle": {
                        "color": "white",
                        "fontSize": 16,
                        "fontFamily": "'Inter', sans-serif",
                    },
                    "padding": [0, 0, 0, 0]

                    
                },
        "radar": {
            "indicator": [
                {"name": "Descendeur", "max": 100},
                {"name": "Coureur", "max": 100},
                {"name": "Grimpeur", "max": 100},
            ],
            "axisName": {
                "show": True,
                "color": "white",
                "fontSize":16,
                "fontFamily": "'Inter', sans-serif",
            },
            "splitNumber": 2,
        },
        "series": [
            {
                "name": "",
                "type": "radar",
                "data": [

                    {
                        "value": [60, 50, 70],
                        "name": "Ton profil",
                        "itemStyle": {
                            "color": "#04A484",  # Couleur spécifique pour le premier set de données (rouge)
                        },
                        "lineStyle": {
                            "width": 3,  # Augmenter la largeur de la ligne
                        },
                    },
                    {
                        "value": [50, 60, 80],
                        "name": "Moyenne des coureurs",
                        "itemStyle": {
                            "color": "#8e44ad",  # Couleur spécifique pour le premier set de données (rouge)
                        },
                        "lineStyle": {
                            "width": 3,  # Augmenter la largeur de la ligne
                        },
                    },
                    
                    {
                        "value": [90, 92, 95],
                        "name": "Athlète Elite Hugo Deck",
                        "itemStyle": {
                            "color": "#f1c40f",  # Couleur spécifique pour le premier set de données (rouge)
                        },
                        "lineStyle": {
                            "width": 3,  # Augmenter la largeur de la ligne
                        },
                    },
                ],
            }
        ],
        
    }
        with col_radar:
            st_echarts(option, height="500px")



    
    


    




