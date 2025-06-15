import streamlit as st

def main():

    import streamlit as st
    import math

    st.markdown("## III. Méthodes de protection contre les chocs électriques")

    # === 1. Texte théorique ===
    st.markdown("""
    ### 1. Quelques pratiques de protection des personnes contre les chocs électriques
    Les protections contre les chocs électriques visent à éviter que le courant traverse le corps humain. Elles incluent :
    - **L'isolation des parties actives** (gaine, revêtement isolant),
    - **La mise hors tension automatique** par disjoncteur ou différentiel en cas de défaut,
    - **La double isolation** pour les appareils de classe II,
    - **L’utilisation de très basse tension de sécurité (TBTS)** pour les lieux à risques,
    - **La séparation des circuits** par transformateur de séparation,
    - **La mise à la terre des masses** et **liaisons équipotentielles**,
    - **Les dispositifs différentiels** qui coupent automatiquement le circuit en cas de fuite de courant.
    """)

    # === 2. Calcul résistance de prise de terre ===
    st.markdown("### 2. Calcul de la résistance de prise de terre")

    terrains = {
        "Sol sableux sec, roches": 1000,
        "Sable sec, roches imperméables, sols pierreux nus": 3000,
        "Gravier, remblais grossiers, terrains arables maigres": 500,
        "Remblais compacts humides, terrains argileux gras": 50
    }

    choix_terrain = st.selectbox("Nature du sol :", ["Choix manuel de la Résistivité ρ(Ω·m)"] + list(terrains.keys()))
    if choix_terrain != "Choix manuel de la Résistivité ρ(Ω·m)":
        resistivite = terrains[choix_terrain]
    else:
        resistivite = st.number_input("Résistivité ρ (Ω·m)", value=100.0, min_value=1.0)

    longueur = st.number_input("Longueur L (m)", value=20.0, min_value=0.1)
    methode = st.selectbox("Méthode :", ["Boucle à fond de fouille", "Piquet de terre", "Conducteur en tranchée"])

    if st.button("🔍 Calculer R"):
        if methode == "Boucle à fond de fouille" or methode == "Conducteur en tranchée":
            R = (2 * resistivite) / longueur
            formule = "R = 2ρ / L"
        elif methode == "Piquet de terre":
            R = resistivite / longueur
            formule = "R = ρ / L"

        st.markdown(f"### 🔎 Résistance de prise de terre R = **{R:.2f} Ω**")
        st.markdown(f"*Formule utilisée :* `{formule}`")

    # === 3. Dispositif différentiel ===
    st.markdown("### 3. Principe de fonctionnement d’un dispositif différentiel")

    r_diff = st.number_input("Rp (Ω)", value=100.0, min_value=0.0)
    i_diff = st.selectbox("IΔ (A)", [0.01, 0.03, 0.3, 0.5, 1.0, 3.0])
    u_contact = st.selectbox("Uc (V)", [25, 50])

    if st.button("✅ Vérifier sécurité"):
        produit = r_diff * i_diff
        if produit <= u_contact:
            st.success(f"✅ Protection conforme : Rp × IΔ = {produit:.2f} V ≤ Uc = {u_contact} V")
        else:
            st.error(f"⚠️ Protection NON conforme : Rp × IΔ = {produit:.2f} V > Uc = {u_contact} V")
