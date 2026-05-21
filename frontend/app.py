import os

import httpx
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Olist — Prédiction livraison", page_icon="📦")
st.title("📦 Prédiction du temps de livraison")
st.markdown("Renseignez les informations de la commande pour obtenir une estimation.")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        price = st.number_input("Prix (€)", min_value=0.0, value=150.0)
        freight_value = st.number_input("Frais de port (€)", min_value=0.0, value=15.0)
        payment_value = st.number_input("Montant payé (€)", min_value=0.0, value=165.0)
        payment_installments = st.number_input("Nb versements", min_value=1, value=3)

    with col2:
        order_item_id = st.number_input("Nb articles", min_value=1, value=1)
        seller_state = st.selectbox(
            "État vendeur", ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "GO", "ES", "PE"]
        )
        customer_state = st.selectbox(
            "État client", ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "GO", "ES", "PE"]
        )
        purchase_date = st.date_input("Date d'achat")

    submitted = st.form_submit_button("Prédire")

if submitted:
    payload = {
        "price": price,
        "freight_value": freight_value,
        "payment_installments": payment_installments,
        "payment_value": payment_value,
        "order_item_id": order_item_id,
        "order_purchase_timestamp": f"{purchase_date}T10:00:00",
        "seller_state": seller_state,
        "customer_state": customer_state,
    }
    try:
        response = httpx.post(f"{BACKEND_URL}/predict", json=payload, timeout=10)
        response.raise_for_status()
        days = response.json()["delivery_time_days"]
        st.success(f"⏱️ Temps de livraison estimé : **{days:.1f} jours**")
    except Exception as e:
        st.error(f"Erreur : {e}")
