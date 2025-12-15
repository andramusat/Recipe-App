import streamlit as st
import pandas as pd

from db import get_db
from crud import (
    get_ingrediente,
    adauga_ingredient,
    update_ingredient,
    sterge_ingredient,
    get_retete,
    adauga_reteta,
    update_reteta,
    sterge_reteta
)

from aggregations import (
    total_calorii_per_reteta,
    top_retete_dupa_nr_ingrediente,
    nr_retete_per_categorie,
    frecventa_ingrediente,
    statistici_dupa_dificultate,
    retete_cu_alergeni,
    top_densitate_calorica,
    bucket_timp_preparare,
    calorii_medii_pe_categorie
)

st.set_page_config(page_title="Carte de rețete", layout="wide")

try:
    get_db()
except:
    pass

st.markdown("""
<style>

/* ===== ASCUNDE COMPLET SĂGEATA SIDEBAR ===== */
button[data-testid="collapsedControl"] {
    display: none !important;
}

/* PREVINE ORICE MIȘCARE LA HOVER */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"]:hover {
    margin-left: 0 !important;
    transform: none !important;
}

/* SIDEBAR STIL */
section[data-testid="stSidebar"] {
    padding-top: 30px;
    text-align: center;
}

/* TITLU SIDEBAR */
.sidebar-title {
    color: #b71c1c;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 40px;
}

/* BUTOANE MENIU */
section[data-testid="stSidebar"] button {
    width: 150px;
    padding: 0.4rem 1rem;
    margin: 4px auto;
    border-radius: 6px;
    font-weight: 500;
    display: block;
}

/* TITLURI APLICAȚIE */
h1, h2, h3 {
    color: #b71c1c !important;
    font-weight: 700;
}

/* BUTOANE APLICAȚIE */
div[data-testid="stButton"] button,
div[data-testid="stFormSubmitButton"] button {
    padding: 0.35rem 1rem;
    border-radius: 6px;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-title'>Meniu</div>", unsafe_allow_html=True)

if "menu" not in st.session_state:
    st.session_state.menu = "Ingrediente"

if st.sidebar.button("Ingrediente"):
    st.session_state.menu = "Ingrediente"
if st.sidebar.button("Rețete"):
    st.session_state.menu = "Rețete"
if st.sidebar.button("Agregări"):
    st.session_state.menu = "Agregări"

menu = st.session_state.menu

if menu == "Ingrediente":
    st.header("Ingrediente")

    df_ing = pd.DataFrame(get_ingrediente())
    st.subheader("Lista ingredientelor")
    st.dataframe(df_ing, use_container_width=True)

    st.subheader("Adaugă ingredient")

    if "ing_adaugat" not in st.session_state:
        st.session_state.ing_adaugat = False

    with st.form("adauga_ing", clear_on_submit=True):
        nume = st.text_input("Nume")
        unitate = st.selectbox("Unitate", ["g", "kg", "ml", "l", "buc"])
        categorie = st.text_input("Categorie")
        calorii = st.number_input("Calorii", min_value=0)
        alergeni = st.text_input("Alergeni (separați prin virgulă)")
        submitted = st.form_submit_button("Adaugă")

        if submitted and not st.session_state.ing_adaugat:
            adauga_ingredient({
                "nume": nume,
                "unitate": unitate,
                "categorie": categorie,
                "calorii": calorii,
                "alergeni": [a.strip() for a in alergeni.split(",") if a.strip()]
            })
            st.success(f"Ingredientul '{nume}' a fost adăugat!")
            st.session_state.ing_adaugat = True
            df_ing = pd.DataFrame(get_ingrediente())


    st.subheader("Modifică ingredient")
    if not df_ing.empty:
        ing_select = st.selectbox("Selectează ingredient", df_ing["nume"], key="mod_ing")
        ing_data = df_ing[df_ing["nume"] == ing_select].iloc[0]

        with st.form("modifica_ing"):
            nume_nou = st.text_input("Nume", value=ing_data.get("nume", ""))
            unitate_noua = st.selectbox(
                "Unitate", 
                ["g", "kg", "ml", "l", "buc"], 
                index=["g", "kg", "ml", "l", "buc"].index(ing_data.get("unitate", "g"))
            )
            categorie_noua = st.text_input("Categorie", value=ing_data.get("categorie", ""))
            calorii_noi = st.number_input(
                "Calorii", 
                min_value=0, 
                value=int(ing_data.get("calorii", 0))
            )

            alergeni_list = ing_data.get("alergeni")
            if not isinstance(alergeni_list, list):
                alergeni_list = []

            alergeni_noi = st.text_input(
                "Alergeni (separați prin virgulă)",
                value=",".join(alergeni_list)
            )

            submitted_mod = st.form_submit_button("Modifică")

            if submitted_mod:
                update_ingredient(
                    {"nume": ing_select},
                    {
                        "nume": nume_nou,
                        "unitate": unitate_noua,
                        "categorie": categorie_noua,
                        "calorii": calorii_noi,
                        "alergeni": [a.strip() for a in alergeni_noi.split(",") if a.strip()]
                    }
                )
                st.success(f"Ingredientul '{ing_select}' a fost modificat!")
                df_ing = pd.DataFrame(get_ingrediente())  

    st.subheader("Șterge ingredient")
    if not df_ing.empty:
        ing_de_sters = st.selectbox("Selectează ingredient", df_ing["nume"], key="del_ing")
        if st.button("Șterge"):
            sterge_ingredient({"nume": ing_de_sters})
            st.success(f"Ingredientul '{ing_de_sters}' a fost șters!")
            df_ing = pd.DataFrame(get_ingrediente())  

elif menu == "Rețete":
    st.header("Rețete")

    retete = get_retete()

    for r in retete:
        r["ingrediente"] = "; ".join(
            [f"ID: {i['idIng']}, cant: {i['cantitate']}" for i in r["ingrediente"]]
        )

    df_ret = pd.DataFrame(retete)

    st.subheader("Lista rețetelor")
    st.dataframe(df_ret, use_container_width=True)

    st.subheader("Adaugă rețetă")
    with st.form("adauga_reteta"):
        nume = st.text_input("Nume rețetă")
        timp = st.number_input("Timp de preparare (minute)", min_value=1)
        dificultate = st.selectbox("Dificultate", ["ușor", "mediu", "greu"])
        categorie = st.text_input("Categorie")

        ingrediente_ret = []
        nr = st.number_input("Număr ingrediente", min_value=1, step=1)
        for i in range(nr):
            id_ing = st.number_input(f"ID ingredient {i+1}", step=1, key=f"id{i}")
            cant = st.number_input(f"Cantitate {i+1}", min_value=0.0, key=f"cant{i}")
            ingrediente_ret.append({
                "idIng": int(id_ing),
                "cantitate": float(cant)
            })

        submitted = st.form_submit_button("Adaugă")
        if submitted:
            adauga_reteta({
                "nume": nume,
                "timpPreparare": timp,
                "dificultate": dificultate.replace("ș", "s"),
                "categorie": categorie,
                "ingrediente": ingrediente_ret
            })
            st.success(f"Rețeta '{nume}' a fost adăugată!")
            df_ret = pd.DataFrame(get_retete())  

    st.subheader("Șterge rețetă")
    if not df_ret.empty:
        reteta_de_sters = st.selectbox("Selectează rețeta", df_ret["nume"], key="del_ret")
        if st.button("Șterge"):
            sterge_reteta({"nume": reteta_de_sters})
            st.success(f"Rețeta '{reteta_de_sters}' a fost ștearsă!")
            df_ret = pd.DataFrame(get_retete())  

elif menu == "Agregări":
    st.header("Agregări")

    opt = st.selectbox(
        "Selectează agregarea",
        [
            "Total calorii per rețetă",
            "Top rețete după număr de ingrediente",
            "Număr rețete per categorie",
            "Frecvența ingredientelor",
            "Statistici după dificultate",
            "Rețete cu alergeni",
            "Top densitate calorică",
            "Încadrare rețete după timp",
            "Calorii medii per categorie"
        ]
    )

    if opt == "Total calorii per rețetă":
        st.dataframe(pd.DataFrame(total_calorii_per_reteta()))

    elif opt == "Top rețete după număr de ingrediente":
        st.dataframe(pd.DataFrame(top_retete_dupa_nr_ingrediente()))

    elif opt == "Număr rețete per categorie":
        st.dataframe(pd.DataFrame(nr_retete_per_categorie()))

    elif opt == "Frecvența ingredientelor":
        st.dataframe(pd.DataFrame(frecventa_ingrediente()))

    elif opt == "Statistici după dificultate":
        st.dataframe(pd.DataFrame(statistici_dupa_dificultate()))

    elif opt == "Rețete cu alergeni":
        st.dataframe(pd.DataFrame(retete_cu_alergeni()))

    elif opt == "Top densitate calorică":
        st.dataframe(pd.DataFrame(top_densitate_calorica()))

    elif opt == "Încadrare rețete după timp":
        st.dataframe(pd.DataFrame(bucket_timp_preparare()))

    elif opt == "Calorii medii per categorie":
        st.dataframe(pd.DataFrame(calorii_medii_pe_categorie()))
