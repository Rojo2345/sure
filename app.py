import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Calculadora Betmastian.p", layout="centered")

# 🧮 Interfaz de cálculo
st.markdown("### 🧮 Calculadora Betmastian.p")
st.caption("Calcula el monto para cubrir la apuesta")

with st.form("form_apuesta"):
    col1, col2 = st.columns(2)
    with col1:
        monto_A = st.number_input("Monto (A)", min_value=0.0, format="%.2f", value=0.0)
        cuota_B = st.number_input("Cuota B", min_value=1.01, format="%.2f", value=3.0)
    with col2:
        cuota_A = st.number_input("Cuota A", min_value=1.01, format="%.2f", value=1.5)
        dolar_casino = st.text_input("💲 Precio Dólar Casino (opcional)", placeholder="Ej: 1200")

    calcular = st.form_submit_button("Calcular")

# 🧠 Lógica de cálculo
def calcular_apuesta_opuesta(cuota_A, monto_A, cuota_B):
    monto_B = (cuota_A * monto_A) / cuota_B
    inversion_total = monto_A + monto_B
    ganancia_A = cuota_A * monto_A
    ganancia_neta_A = ganancia_A - inversion_total
    ganancia_B = cuota_B * monto_B
    ganancia_neta_B = ganancia_B - inversion_total
    ganancia_neta = min(ganancia_neta_A, ganancia_neta_B)
    porcentaje_ganancia = (ganancia_neta / inversion_total) * 100
    return monto_B, inversion_total, ganancia_neta, ganancia_neta_A, ganancia_neta_B, porcentaje_ganancia

# 🎯 Mostrar resultados
if calcular:
    monto_B, inversion_total, ganancia_neta, gA, gB, rentabilidad = calcular_apuesta_opuesta(cuota_A, monto_A, cuota_B)

    st.markdown("### 🎯 Resultados:")
    with st.container():
        st.markdown(f"**Apostar:** `${monto_B:,.2f}` a cuota B")
        st.markdown(f"💰 **Inversión total:** `${inversion_total:,.2f}`")
        st.markdown(f"📈 **Rentabilidad:** `{rentabilidad:.2f}%`")
        colA, colB = st.columns(2)
        with colA:
            st.success(f"✅ **Si gana A:** `${gA:,.2f}`")
        with colB:
            st.success(f"✅ **Si gana B:** `${gB:,.2f}`")



