import streamlit as st

def main():

    import streamlit as st
    import pandas as pd
    import numpy as np
    import math
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches


    st.markdown("## I. Simulation de l'Énergie Électrique")
    st.markdown("### 1. Calcul des puissances, Intensités, Énergies et Factures")

    # === Données des appareils ===
    appareils = {
        "Ampoule type 1": {"P": 40, "Q": 0, "Cosφ": 1.0},
        "Ampoule type 2": {"P": 36, "Q": 0, "Cosφ": 1.0},
        "Ampoule type 3": {"P": 25, "Q": 0, "Cosφ": 1.0},
        "Ampoule type 4": {"P": 20, "Q": 12, "Cosφ": 0.85},
        "Ampoule type 5": {"P": 15, "Q": 5, "Cosφ": 0.70},
        "Télévision": {"P": 100, "Q": 10, "Cosφ": 0.95},
        "Fer à repasser": {"P": 1000, "Q": 0, "Cosφ": 1.0},
        "Chauffe-eau": {"P": 300, "Q": 0, "Cosφ": 1.0},
        "Réchaud électrique": {"P": 1000, "Q": 0, "Cosφ": 1.0},
        "Téléphone ": {"P": 5, "Q": 0, "Cosφ": 1.0},
        "Interphone": {"P": 8, "Q": 0, "Cosφ": 1.0},
        "Vidéophone": {"P": 15, "Q": 0, "Cosφ": 1.0},
        "Prises (appareils simples)": {"P": 500, "Q": 100, "Cosφ": 0.9},
        "Autres charges": {"P": 1500, "Q": 900, "Cosφ": 1.0},
        "Climatiseur (moteur spécialisé)": {"Pméc": 750, "Cosφ": 0.82, "η": 0.68},
        "Ventilateur (moteur spécialisé)": {"Pméc": 60, "Cosφ": 0.80, "η": 0.48},
        "Réfrigérateur (moteur spécialisé)": {"Pméc": 180, "Cosφ": 0.88, "η": 0.78},
        "Lave-linge (moteur spécialisé)": {"Pméc": 370, "Cosφ": 0.77, "η": 0.66},
        "cuisinière (moteur spécialisé)": {"Pméc": 1000, "Cosφ": 0.8, "η": 0.85},
        "Prises (moteur spécialisé)": {"Pméc": 3000, "Cosφ": 0.8, "η": 0.85}
    }

    # === Paramètres généraux ===
    st.sidebar.header("🔧 Paramètres généraux")
    duree_utilisation = st.sidebar.number_input("Durée d'utilisation (h/j)", 0.0, 24.0, 4.0)
    tarif_kwh = st.sidebar.number_input("Tarif (F/kWh)", 0.0, 1000.0, 90.0)
    tension_mono = st.sidebar.number_input("Tension monophasée (V)", 0.0, 300.0, 220.0)
    tension_tri = st.sidebar.number_input("Tension triphasée (V)", 0.0, 600.0, 380.0)
    choix_methode = st.sidebar.selectbox("Méthode", ["Monophasée", "Triphasée"])

    # === Interface appareils ===
    st.markdown("### 🔧 Paramétrage des appareils")
    donnees_appareils = []
    for nom, spec in appareils.items():
        with st.expander(nom):
            n = st.number_input(f"Quantité - {nom}", min_value=0, step=1, key=nom)
            params = {}
            for param in spec:
                valeur = st.number_input(f"{param} - {nom}", value=float(spec[param]), format="%.4f", key=nom+param)
                params[param] = valeur
            donnees_appareils.append((nom, n, params))

    if st.button("🔍 Lancer l’analyse"):
        P_total = Q_total = 0
        tableau = []
        tableau_courant = []
        appareils_speciaux = False
        appareils_simples = False

        for nom, n, params in donnees_appareils:
            if n == 0:
                continue
            if "Pméc" in params:
                P = (params["Pméc"] / params["η"]) * n
                Q = math.sqrt((P / params["Cosφ"])**2 - P**2)
                Pm = params["Pméc"] * n
                appareils_speciaux = True
            else:
                P = params["P"] * n
                Q = params["Q"] * n
                Pm = 0
                appareils_simples = True

            S = math.sqrt(P**2 + Q**2)
            Cosφ = P / S if S != 0 else 1.0
            U = tension_tri if choix_methode == "Triphasée" and "Pméc" in params else tension_mono
            k = math.sqrt(3) if choix_methode == "Triphasée" else 1
            I = round(S / (k * U), 2)
            calibre = math.ceil(I / 5) * 5
            section = "1.5 mm²" if calibre <= 16 else "2.5 mm²" if calibre <= 25 else "6 mm²" if calibre <= 38 else "> 6 mm²"
            P_total += P
            Q_total += Q

            tableau.append([nom, n, round(P,2), round(Q,2), round(S,2), round(Pm,2), round(params.get('η', 1.0),2), round(params["Cosφ"], 2)])
            tableau_courant.append([nom, I, calibre, section])

        S_total = math.sqrt(P_total**2 + Q_total**2)
        Cosφ_total = P_total / S_total if S_total != 0 else 1.0
        k = math.sqrt(3) if choix_methode == "Triphasée" else 1
        U_global = tension_tri if choix_methode == "Triphasée" else tension_mono
        I_total = round(S_total / (k * U_global), 2)
        Energie = round(P_total * duree_utilisation / 1000, 3)
        Facture = round(Energie * tarif_kwh, 2)
        calibre_total = math.ceil(I_total / 5) * 5

        df = pd.DataFrame(tableau, columns=["Appareil", "Quantité", "P (W)", "Q (VAr)", "S (VA)", "Pméc total (W)", "η", "Cosφ"])
        st.dataframe(df, use_container_width=True)

        df2 = pd.DataFrame(tableau_courant, columns=["Appareil", "I (A)", "Calibre (A)", "Section (mm²)"])
        st.dataframe(df2, use_container_width=True)

        df_global = pd.DataFrame({
            "Paramètre": [
                "Pt: puissance active totale (kW)",
                "Qt: puissance réactive totale (kVAr)",
                "St: puissance apparente totale (kVA)",
                "Cosφg: Facteur de puissance global",
                "Ig: Intensité du circuit global (A)",
                "Cg: Calibre général (A)",
                "Énergie simulée (kWh)",
                "Facture (F)"
            ],
            "Valeur": [
                round(P_total/1000, 2), round(Q_total/1000, 2), round(S_total/1000, 2),
                round(Cosφ_total, 3), I_total, calibre_total, Energie, Facture
            ]
        })
        st.dataframe(df_global)

        recommandation = "Triphasé (appareils spéciaux détectés)" if appareils_speciaux else "Monophasé (appareils simples uniquement)"
        st.success(f"✅ Alimentation recommandée : {recommandation}")
        st.info(f"Méthode : {choix_methode} | Tension U = {U_global} V | Coefficient k = {round(k,3)}")

        st.markdown("### 2. Dimensionnement du Groupe Électrogène")
        pourcentage_utilisation = st.slider("% utilisé de Pt", 10, 150, 100)
        cosphi_groupe = st.number_input("Cosφ groupe", 0.5, 1.0, 0.8)
        P_utilisee = round(P_total / 1000 * pourcentage_utilisation / 100, 2)
        S_groupe = round(P_utilisee / cosphi_groupe, 2)
        st.success(f"🔋 Groupe électrogène requis : {S_groupe} kVA (pour P utilisée = {P_utilisee} kW)")

