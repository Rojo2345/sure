import streamlit as st
import pandas as pd
import os

# 🖼️ Configuración de la página
st.set_page_config(page_title="Calculadora Betmastian.p", layout="centered")

# 💅 Estilos personalizados tipo LudoBets
st.markdown("""
    <style>
    body {
        background-color: #0f1117;
        color: white;
    }
    .main {
        background-color: #0f1117;
        color: white;
    }
    .result-box {
        background-color: #2c2f36;
        padding: 1.2em;
        border-radius: 10px;
        color: white;
        margin-top: 1em;
        border: 1px solid #444;
    }
    .highlight {
        font-size: 1.2em;
        font-weight: bold;
        color: #00ffae;
    }
    .tag {
        background-color: #00c17d;
        color: white;
        padding: 0.4em 0.8em;
        border-radius: 5px;
        display: inline-block;
        margin: 0.3em 0;
    }
    .profit-box {
        background-color: #1e442f;
        color: white;
        padding: 0.5em;
        border-radius: 8px;
        text-align: center;
        margin-top: 0.4em;
    }
    .stButton>button {
        background-color: #2e64fe;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 🧮 Interfaz de cálculo
st.markdown("## 🧮 Calculadora Betmastian.p")
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

    # Estilo visual de resultados
    st.markdown(f"""
    <div class="result-box">
        <h4>📊 <strong>Resultados:</strong></h4>
        <p>Apostar: <span class="highlight">${monto_B:,.2f}</span> a cuota B</p>
        <p>💰 Inversión total: <span class="highlight">${inversion_total:,.2f}</span></p>
        <p class="tag">% Rentabilidad: +{rentabilidad:.2f}%</p>
        <div class="profit-box">✅ Si gana A: ${gA:,.2f}</div>
        <div class="profit-box">✅ Si gana B: ${gB:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)
