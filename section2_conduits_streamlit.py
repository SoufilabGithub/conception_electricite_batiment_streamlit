import streamlit as st

def main():

    import streamlit as st
    import pandas as pd


    st.markdown("## II. Choix, Dimensionnement et Implantation des Conducteurs, Conduits, Rayons, Saignées et Goulottes")
    st.markdown("### 1. Section totale des conducteurs, Section totale des conduits et leurs rayons max de courbure")

    # === Données ===
    df_tableau_3 = pd.DataFrame({
        'Section âme (mm²)': [1.5, 2.5, 4, 6, 10, 16, 25],
        'H07V-U ou R': [8.55, 11.90, 15.20, 22.90, 36.30, 50.30, 75.40],
        'H07V-K': [9.60, 13.85, 18.10, 31.20, 45.40, 60.80, 95.00]
    })

    df_tableau_4 = pd.DataFrame({
        'Diamètre ext. (mm)': [16, 20, 25, 32, 40, 50, 63],
        'ICA, ICTA, ICTL': [30, 52, 88, 155, 255, 411, 724],
        'IRO, IRL': [44, 75, 120, 202, 328, 514, 860]
    })

    df_tableau_5 = pd.DataFrame({
        'Diamètre ext. (mm)': [16, 20, 25, 32, 40, 50, 63],
        'ISO (ICTL, ICD)': [96, 120, 150, 192, 300, 480, 600],
        'ICO (ICTA)': [48, 60, 75, 96, 160, 200, 252]
    })

    # Interface utilisateur dynamique pour les circuits
    st.markdown("### ➕ Saisie des circuits électriques")

    if "circuits" not in st.session_state:
        st.session_state.circuits = []

    def ajouter_circuit():
        st.session_state.circuits.append({"section": 1.5, "type": "H07V-U ou R", "nb_ames": 2})

    def supprimer_dernier():
        if st.session_state.circuits:
            st.session_state.circuits.pop()

    col1, col2 = st.columns(2)
    with col1:
        st.button("➕ Ajouter un circuit", on_click=ajouter_circuit)
    with col2:
        st.button("➖ Supprimer le dernier", on_click=supprimer_dernier)

    total_section = 0
    details = []

    for idx, circuit in enumerate(st.session_state.circuits):
        st.markdown(f"#### Circuit #{idx+1}")
        cols = st.columns(3)
        section = cols[0].selectbox(f"Section âme (mm²) #{idx+1}", df_tableau_3["Section âme (mm²)"], key=f"section_{idx}")
        type_conducteur = cols[1].selectbox(f"Type conducteur #{idx+1}", ["H07V-U ou R", "H07V-K"], key=f"type_{idx}")
        nb_ames = cols[2].number_input(f"Nombre d’âmes #{idx+1}", min_value=1, max_value=20, value=2, key=f"nb_{idx}")

        section_utile = df_tableau_3[df_tableau_3["Section âme (mm²)"] == section][type_conducteur].values[0]
        section_totale = section_utile * nb_ames
        total_section += section_totale
        details.append((section, type_conducteur, nb_ames, section_utile, section_totale))

    if details:
        df_resultat = pd.DataFrame(details, columns=["Section âme", "Type", "Nb âmes", "Section conducteur", "Section totale"])
        st.markdown("### 📌 Détail des circuits saisis")
        st.dataframe(df_resultat)

        st.markdown(f"✅ **Section totale cumulée des conducteurs (isolant compris)** : `{total_section:.2f} mm²`")

        seuil = total_section
        seuil_tiers = total_section * 3

        df1 = df_tableau_4.copy()
        df1["Valide ICA"] = df1["ICA, ICTA, ICTL"] >= seuil
        df1["Valide IRO"] = df1["IRO, IRL"] >= seuil
        st.markdown("### 🔎 Étape 1 : Section utile conduit ≥ Section cumulée conducteur")
        st.dataframe(df1)

        df2 = df_tableau_4.copy()
        df2["Valide ICA"] = df2["ICA, ICTA, ICTL"] >= seuil_tiers
        df2["Valide IRO"] = df2["IRO, IRL"] >= seuil_tiers
        st.markdown("### 📐 Étape 2 : Règle du tiers")
        st.dataframe(df2)

        diametres_valides = df2[(df2["Valide ICA"]) | (df2["Valide IRO"])]["Diamètre ext. (mm)"]
        df3 = df_tableau_5.copy()
        df3["Valide"] = df3["Diamètre ext. (mm)"].isin(diametres_valides)
        st.markdown("### 🔁 Étape 3 : Rayon de courbure selon les diamètres")
        st.dataframe(df3)

    # Texte explicatif : points 2 à 5
    st.markdown("""### 2. Types de conducteurs et câbles électriques
    - **Conducteur isolé** : âme conductrice (cuivre ou aluminium) + enveloppe isolante.
    - **Câble unipolaire** : un seul conducteur isolé.
    - **Câble multipolaire** : plusieurs conducteurs dans une même gaine.
    - **Types courants** :
      - H07V-U ou R : rigide, pose encastrée
      - H07V-K : souple, pose mobile ou apparente
    - **Code couleur normalisé** :
      - Vert/Jaune : Terre
      - Bleu clair : Neutre
      - Rouge, Noir, Marron : Phase
    """)

    st.markdown("""### 3. Désignation et emploi des conduits
    - IRL : rigide lisse (apparent)
    - ICTA : annelé souple (encastré/apparent)
    - ICTL : cintrable lisse (encastré)
    - Un conduit peut contenir des circuits différents si :
      - même tension nominale,
      - chaque circuit est protégé contre les surintensités,
      - tous proviennent d’un même disjoncteur.
    """)

    st.markdown("""### 4. Règles de pose des saignées
    - Interdites : au-dessus des ouvertures, sur toute la cloison, en oblique
    - Distances à respecter :
      - Max 1.5 m entre 2 saignées >1.2 m de haut
      - Min 0.20 m des angles/cloisons
      - Max 0.80 m à partir du plafond
      - Max 0.50 m en partie horizontale
    """)

    st.markdown("""### 5. Règles de remplissage des goulottes
    - ≤ 3/4 de la section utile
    - Circuits différents si :
      - même tension nominale,
      - chaque circuit protégé individuellement,
      - tous du même disjoncteur de branchement.
    """)

